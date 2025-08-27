import datetime
import uuid

# Conversion factor from kPa to mmHg
KPA_TO_MMHG_FACTOR = 7.50062
# Conversion factor from kPa to PSI
KPA_TO_PSI_FACTOR = 0.145038

def kpa_to_mmhg(kpa: float) -> float:
    """Converts kilopascals (kPa) to millimeters of mercury (mmHg)."""
    return kpa * KPA_TO_MMHG_FACTOR

def kpa_to_psi(kpa: float) -> float:
    """Converts kilopascals (kPa) to pounds per square inch (psi)."""
    return kpa * KPA_TO_PSI_FACTOR

def get_day_of_year() -> int:
    """Gets the current day of the year (1-366)."""
    return datetime.datetime.now().timetuple().tm_yday

def get_time_string() -> str:
    """Gets the current time as a formatted string (HH:MM:SS)."""
    return datetime.datetime.now().strftime('%H:%M:%S')

def generate_id(name: str) -> str:
    """Generates a consistent UUID from a given name string."""
    # Using UUIDv5 to create a deterministic ID based on the name
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))