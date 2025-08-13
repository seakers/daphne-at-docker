from django.db import models
from rest_framework import serializers

from daphne_context.models import UserInformation, DialogueContext


# Context for AT Users
class ATContext(models.Model):
    user_information = models.OneToOneField(UserInformation, on_delete=models.CASCADE)

    # In order to support object types, some of the following context variables are defined as TextFields. The variables
    # are then stored as a json string and parsed when required. Not optimal, could be done better in the future.

    # For the anomalies, measurements and procedures, a "selected" and "recent" context variable is defined. This allows
    # to ask questions such as "What are the risks of THIS anomaly?" from the chat box. A proper method is then defined
    # to retrieve the meaning of the "THIS" pointer.
    selected_anomalies = models.TextField(default='')
    selected_measurements = models.TextField(default='')
    selected_procedures = models.TextField(default='')

    # Current telemetry values context variable
    current_telemetry_values = models.TextField(default='')

    # Thread deployment status bool
    are_at_threads_deployed = models.BooleanField(default=False)

    # Thread deployment status bool
    seen_tutorial = models.BooleanField(default=False)


class ATContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ATContext
        fields = '__all__'


# Context for Active Parts of Daphne
class ActiveATContext(models.Model):
    atcontext = models.OneToOneField(ATContext, on_delete=models.CASCADE)


class ActiveContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveATContext
        fields = '__all__'


class ATDialogueContext(models.Model):
    dialoguecontext = models.OneToOneField(DialogueContext, on_delete=models.CASCADE)

    # All, Current, Next and Previous procedural steps
    all_steps_from_procedure = models.TextField(default='')
    next_step_pointer = models.IntegerField(default=-1)
    previous_step_pointer = models.IntegerField(default=-1)
    current_step_pointer = models.IntegerField(default=-1)


class ATDialogueContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ATDialogueContext
        fields = '__all__'


# Historical Telemetry Storage
class TelemetryHistory(models.Model):
    """Model for storing historical telemetry data for physics diagnosis"""
    
    # Timestamp when the telemetry data was recorded
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # User session information (optional, for multi-user scenarios)
    user_information = models.ForeignKey(UserInformation, on_delete=models.CASCADE, null=True, blank=True)
    
    # Telemetry data stored as JSON
    telemetry_data = models.JSONField()
    
    # Source of telemetry (Hera, sEclss, etc.)
    source = models.CharField(max_length=50, default='Hera')
    
    # Session identifier to group related telemetry readings
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    # Optional metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        # Index for efficient querying by timestamp
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['source', 'timestamp']),
            models.Index(fields=['session_id', 'timestamp']),
        ]
        # Order by timestamp descending for efficient retrieval
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Telemetry from {self.source} at {self.timestamp}"
    
    @classmethod
    def get_recent_telemetry(cls, source='Hera', limit=100, session_id=None):
        """
        Get recent telemetry data for physics diagnosis
        
        Args:
            source: Source of telemetry data (default: 'Hera')
            limit: Number of recent readings to retrieve (default: 100)
            session_id: Optional session identifier to filter by
            
        Returns:
            QuerySet of recent telemetry data
        """
        print(f"🗄️ Database: Querying TelemetryHistory for source='{source}', limit={limit}, session_id={session_id}")
        
        queryset = cls.objects.filter(source=source)
        print(f"🗄️ Database: Base query returned {queryset.count()} records")
        
        if session_id:
            queryset = queryset.filter(session_id=session_id)
            print(f"🗄️ Database: After session filter: {queryset.count()} records")
        
        result = queryset[:limit]
        print(f"🗄️ Database: Final result: {len(result)} records")
        
        # Print some sample data for debugging
        if result:
            first_record = result[0]
            print(f"🗄️ Database: Sample record - ID: {first_record.id}, Timestamp: {first_record.timestamp}")
            print(f"🗄️ Database: Sample record keys: {list(first_record.telemetry_data.keys()) if isinstance(first_record.telemetry_data, dict) else 'Not a dict'}")
        
        return result
    
    @classmethod
    def get_telemetry_for_physics_diagnosis(cls, source='Hera', time_window_seconds=1):
        """
        Get telemetry data within a time window for physics diagnosis
        
        Args:
            source: Source of telemetry data (default: 'Hera')
            time_window_seconds: Time window in seconds (default: 1)
            
        Returns:
            QuerySet of telemetry data within the time window
        """
        from django.utils import timezone
        from datetime import timedelta
        
        # Convert seconds to minutes for database query
        time_window_minutes = max(1, time_window_seconds // 60)
        #cutoff_time = timezone.now() - timedelta(minutes=time_window_minutes)
        cutoff_time = timezone.now() - timedelta(seconds=time_window_seconds)
        return cls.objects.filter(
            source=source,
            timestamp__gte=cutoff_time
        ).order_by('timestamp')
