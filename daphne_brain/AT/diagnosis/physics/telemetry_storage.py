import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from django.utils import timezone

from AT.models import TelemetryHistory


class TelemetryStorageService:
    """Service for storing and retrieving historical telemetry data"""
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize the telemetry storage service
        
        Args:
            session_id: Optional session identifier for grouping telemetry data
        """
        self.session_id = session_id or str(uuid.uuid4())
    
    def store_telemetry(self, telemetry_data: Dict[str, Any], source: str = 'Hera', 
                       user_information=None, metadata: Dict[str, Any] = None,
                       tick_number: Optional[int] = None) -> TelemetryHistory:
        """
        Store telemetry data in the database
        
        Args:
            telemetry_data: Dictionary containing telemetry readings
            source: Source of the telemetry data (default: 'Hera')
            user_information: Optional user information object
            metadata: Optional metadata dictionary
            tick_number: Optional tick number from BioSim (each tick = 0.1 hour)
            
        Returns:
            TelemetryHistory object that was created
        """
        # Create metadata if not provided
        if metadata is None:
            metadata = {}
        
        # Add timestamp to metadata
        metadata['stored_at'] = timezone.now().isoformat()
        
        # Set T+0 if this is first BioSim telemetry
        if source == 'BioSim':
            from AT.diagnosis.physics.simulation_time_service import SimulationTimeService
            if not SimulationTimeService.get_t_zero():
                # Set T+0 to current server time
                t_zero_time = timezone.now()
                SimulationTimeService.set_t_zero(t_zero_time)
                print(f"🕐 T+0 SET at server time: {t_zero_time.isoformat()}")
        
        # Create and save the telemetry history record
        telemetry_record = TelemetryHistory.objects.create(
            telemetry_data=telemetry_data,
            source=source,
            session_id=self.session_id,
            user_information=user_information,
            metadata=metadata
        )
        
        return telemetry_record
    
    def get_recent_telemetry(self, source: str = 'Hera', limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent telemetry data for physics diagnosis
        
        Args:
            source: Source of telemetry data (default: 'Hera')
            limit: Number of recent readings to retrieve (default: 100)
            
        Returns:
            List of telemetry data dictionaries
        """
        print(f"🔍 TelemetryStorage: Querying database for source='{source}', limit={limit}, session_id={self.session_id}")
        
        telemetry_records = TelemetryHistory.get_recent_telemetry(
            source=source, 
            limit=limit, 
            session_id=self.session_id
        )
        
        print(f"📊 TelemetryStorage: Found {len(telemetry_records)} telemetry records in database")
        
        result = [
            {
                'timestamp': record.timestamp.isoformat(),
                'data': record.telemetry_data,
                'metadata': record.metadata
            }
            for record in telemetry_records
        ]
        
        print(f"✅ TelemetryStorage: Returning {len(result)} telemetry records")
        return result
    
    def get_telemetry_for_physics_diagnosis(self, source: str = 'Hera', 
                                          time_window_seconds: int = 1) -> List[Dict[str, Any]]:
        """
        Get telemetry data within a time window for physics diagnosis
        
        Args:
            source: Source of telemetry data (default: 'Hera')
            time_window_seconds: Time window in seconds (default: 60)
            
        Returns:
            List of telemetry data dictionaries within the time window
        """
        telemetry_records = TelemetryHistory.get_telemetry_for_physics_diagnosis(
            source=source,
            time_window_seconds=time_window_seconds
        )
        
        return [
            {
                'timestamp': record.timestamp.isoformat(),
                'data': record.telemetry_data,
                'metadata': record.metadata
            }
            for record in telemetry_records
        ]
    
    def get_telemetry_timeseries(self, source: str = 'Hera', 
                               time_window_seconds: int = 1,
                               sensor_keys: Optional[List[str]] = None) -> Dict[str, List[float]]:
        """
        Get telemetry data as a time series for physics diagnosis
        
        Args:
            source: Source of telemetry data (default: 'Hera')
            time_window_seconds: Time window in seconds (default: 60)
            sensor_keys: Optional list of sensor keys to extract (if None, uses all)
            
        Returns:
            Dictionary with sensor names as keys and lists of values as values
        """
        telemetry_records = self.get_telemetry_for_physics_diagnosis(source, time_window_seconds)
        
        if not telemetry_records:
            return {}
        
        # Initialize timeseries data structure
        timeseries_data = {}
        
        # Process each telemetry record
        for record in telemetry_records:
            telemetry_data = record['data']
            
            # Extract sensor data
            if isinstance(telemetry_data, dict):
                for sensor_name, sensor_value in telemetry_data.items():
                    # Filter by sensor keys if specified
                    if sensor_keys is None or sensor_name in sensor_keys:
                        if sensor_name not in timeseries_data:
                            timeseries_data[sensor_name] = []
                        
                        # Convert to float if possible
                        try:
                            float_value = float(sensor_value)
                            timeseries_data[sensor_name].append(float_value)
                        except (ValueError, TypeError):
                            # Skip non-numeric values
                            continue
        
        return timeseries_data
    
    def get_latest_telemetry_values(self, source: str = 'Hera') -> Dict[str, float]:
        """
        Get the most recent telemetry values
        
        Args:
            source: Source of telemetry data (default: 'Hera')
            
        Returns:
            Dictionary of latest sensor values
        """
        latest_record = TelemetryHistory.objects.filter(
            source=source,
            session_id=self.session_id
        ).order_by('-timestamp').first()
        
        if latest_record and isinstance(latest_record.telemetry_data, dict):
            # Convert all values to float where possible
            latest_values = {}
            for sensor_name, sensor_value in latest_record.telemetry_data.items():
                try:
                    latest_values[sensor_name] = float(sensor_value)
                except (ValueError, TypeError):
                    # Skip non-numeric values
                    continue
            return latest_values
        
        return {}
    
    def cleanup_old_telemetry(self, days_to_keep: int = 7) -> int:
        """
        Clean up old telemetry data to prevent database bloat
        
        Args:
            days_to_keep: Number of days of data to keep (default: 7)
            
        Returns:
            Number of records deleted
        """
        cutoff_date = timezone.now() - timedelta(days=days_to_keep)
        deleted_count, _ = TelemetryHistory.objects.filter(
            timestamp__lt=cutoff_date
        ).delete()
        
        return deleted_count


# Global telemetry storage service instance
telemetry_storage = TelemetryStorageService()
