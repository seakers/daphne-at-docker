from datetime import datetime
from typing import Optional
from django.core.cache import cache
from django.utils import timezone
from dateutil import parser as date_parser


class SimulationTimeService:
    """
    Manages simulation time with 360x speed factor.
    T+0 = when first telemetry received from BioSim
    
    Time format: T+DD:HH:MM (after T+0) or T-DD:HH:MM (before T+0)
    - DD: Days (00-99)
    - HH: Hours (00-23)
    - MM: Minutes (00-59)
    
    Note: T- times occur when physics diagnosis requires historical data
    that extends before the T+0 reference point (e.g., when supplementing
    insufficient telemetry with generated timestamps).
    """
    
    SIMULATION_SPEED_FACTOR = 360  # 360x faster than real-time
    T_ZERO_CACHE_KEY = 'simulation_t_zero_timestamp'
    
    @classmethod
    def set_t_zero(cls, real_time: datetime) -> None:
        """
        Set T+0 reference point (first telemetry received from BioSim)
        
        Args:
            real_time: The real-world datetime when first telemetry was received
        """
        cache.set(cls.T_ZERO_CACHE_KEY, real_time.isoformat(), timeout=None)
        print(f"🕐 T+0 SET: First BioSim telemetry received at {real_time.isoformat()}")
    
    @classmethod
    def get_t_zero(cls) -> Optional[datetime]:
        """
        Get T+0 reference point
        
        Returns:
            datetime object of T+0 or None if not set
        """
        t_zero_str = cache.get(cls.T_ZERO_CACHE_KEY)
        if t_zero_str:
            return datetime.fromisoformat(t_zero_str)
        return None
    
    @classmethod
    def reset_t_zero(cls) -> None:
        """Reset T+0 (for new simulation runs)"""
        cache.delete(cls.T_ZERO_CACHE_KEY)
        print("🔄 T+0 RESET: Simulation time cleared")
    
    @classmethod
    def get_absolute_simulation_time(cls, real_time: datetime) -> Optional[str]:
        """
        Convert real-time to absolute simulation time (T+DD:HH:MM or T-DD:HH:MM)
        
        Args:
            real_time: Current real-world datetime
            
        Returns:
            String in format "T+DD:HH:MM" (after T+0) or "T-DD:HH:MM" (before T+0)
            or None if T+0 not set
            
        Example:
            If 4 real minutes elapsed since T+0, returns "T+01:00:00" (1 day simulation time)
            If timestamp is 2 minutes before T+0, returns "T-00:12:00" (12 hours before T+0)
        """
        t_zero = cls.get_t_zero()
        if not t_zero:
            return None
        
        # Make sure both datetimes are timezone-aware
        if timezone.is_naive(real_time):
            real_time = timezone.make_aware(real_time)
        if timezone.is_naive(t_zero):
            t_zero = timezone.make_aware(t_zero)
        
        # Calculate real-time elapsed since T+0 (can be negative if before T+0)
        real_elapsed = (real_time - t_zero).total_seconds()
        
        # Apply 360x speed factor
        sim_elapsed_seconds = int(real_elapsed * cls.SIMULATION_SPEED_FACTOR)
        
        # Determine if we're before or after T+0
        if sim_elapsed_seconds < 0:
            # Before T+0 - use T- format
            sim_elapsed_seconds = abs(sim_elapsed_seconds)
            prefix = "T-"
        else:
            # After T+0 - use T+ format
            prefix = "T+"
        
        # Convert to DD:HH:MM format
        days = sim_elapsed_seconds // 86400
        hours = (sim_elapsed_seconds % 86400) // 3600
        minutes = (sim_elapsed_seconds % 3600) // 60
        
        # Cap days at 99
        days = min(days, 99)
        
        return f"{prefix}{days:02d}:{hours:02d}:{minutes:02d}"
    
    @classmethod
    def convert_timestamp_to_sim_time(cls, timestamp) -> Optional[str]:
        """
        Convert any timestamp to simulation time.
        Handles both datetime objects and ISO format strings.
        
        Args:
            timestamp: The datetime object or ISO format string to convert
            
        Returns:
            String in format "T+DD:HH:MM" or None if T+0 not set
        """
        # If timestamp is a string, parse it to datetime
        if isinstance(timestamp, str):
            try:
                timestamp = date_parser.isoparse(timestamp)
            except (ValueError, AttributeError) as e:
                print(f"[SimTime] Error parsing timestamp string '{timestamp}': {e}")
                return "Unknown"
        
        return cls.get_absolute_simulation_time(timestamp)
    
    @classmethod
    def is_simulation_running(cls) -> bool:
        """
        Check if simulation is running (T+0 has been set)
        
        Returns:
            True if T+0 is set, False otherwise
        """
        return cls.get_t_zero() is not None
