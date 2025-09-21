import requests
import json
import logging
from typing import Dict, List, Any, Optional
from django.conf import settings
import os
from .biosim_utils import kpa_to_mmhg, kpa_to_psi, get_day_of_year, get_time_string, generate_id

logger = logging.getLogger(__name__)

class BioSimClient:
    """
    Client for communicating with BioSim server to retrieve simulation data
    for physics-based diagnosis.
    """
    
    def __init__(self, base_url: str = None):
        """
        Initialize BioSim client.
        
        Args:
            base_url: Base URL of BioSim server. Defaults to Django settings if not provided.
        """
        if base_url is None:
            # Use Django settings for BioSim configuration
            try:
                from django.conf import settings
                self.base_url = getattr(settings, 'BIOSIM_CONFIG', {}).get('BASE_URL', "http://10.5.0.7:8009")
                self.request_timeout = getattr(settings, 'BIOSIM_CONFIG', {}).get('REQUEST_TIMEOUT', 30)
                self.health_check_timeout = getattr(settings, 'BIOSIM_CONFIG', {}).get('HEALTH_CHECK_TIMEOUT', 5)
                self.enable_biosim = getattr(settings, 'BIOSIM_CONFIG', {}).get('ENABLE_BIOSIM', True)
            except ImportError:
                # Fallback if Django is not available
                self.base_url = "http://10.5.0.7:8009"
                self.request_timeout = 30
                self.health_check_timeout = 5
                self.enable_biosim = True
        else:
            self.base_url = base_url.rstrip('/')
            self.request_timeout = 30
            self.health_check_timeout = 5
            self.enable_biosim = True
        
        self.session = requests.Session()
        self.session.timeout = self.request_timeout
        
        logger.info(f"🚀 BioSim Client: Initialized with base URL: {self.base_url}")
        logger.info(f"🔧 BioSim Client: Request timeout set to {self.session.timeout} seconds")
        logger.info(f"🔧 BioSim Client: Health check timeout set to {self.health_check_timeout} seconds")
        logger.info(f"🔧 BioSim Client: BioSim integration enabled: {self.enable_biosim}")
        
        # Check if BioSim should be enabled
        if not self.enable_biosim:
            logger.warning(f"⚠️ BioSim Client: BioSim integration is disabled in settings")
    
    def start_simulation(self, config_file_path: str) -> Optional[int]:
        """
        Start a BioSim simulation and return simulation ID.
        
        Args:
            config_file_path: Path to the BioSim configuration XML file
            
        Returns:
            Simulation ID if successful, None otherwise
        """
        try:
            logger.info(f"🔄 BioSim Client: Starting simulation with config: {config_file_path}")
            
            # Check if config file exists
            if not os.path.exists(config_file_path):
                logger.error(f"❌ BioSim Client: Configuration file not found: {config_file_path}")
                return None
            
            with open(config_file_path, 'r') as f:
                config_data = f.read()
            
            logger.info(f"📄 BioSim Client: Read config file, size: {len(config_data)} characters")
            
            # Make the API call
            api_url = f"{self.base_url}/api/simulation/start"
            logger.info(f"🌐 BioSim Client: Making POST request to: {api_url}")
            
            response = self.session.post(
                api_url,
                headers={'Content-Type': 'application/xml'},
                data=config_data
            )
            
            logger.info(f"📡 BioSim Client: Response received - Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                sim_id = data.get('simId')
                logger.info(f"✅ BioSim Client: Simulation started successfully! ID: {sim_id}")
                logger.info(f"📊 BioSim Client: Full response data: {json.dumps(data, indent=2)}")
                return sim_id
            else:
                logger.error(f"❌ BioSim Client: Failed to start simulation")
                logger.error(f"   Status Code: {response.status_code}")
                logger.error(f"   Response Text: {response.text}")
                logger.error(f"   Response Headers: {dict(response.headers)}")
                return None
                
        except FileNotFoundError:
            logger.error(f"❌ BioSim Client: Configuration file not found: {config_file_path}")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ BioSim Client: Connection error - BioSim server may not be running")
            logger.error(f"   Error details: {e}")
            return None
        except requests.exceptions.Timeout as e:
            logger.error(f"❌ BioSim Client: Request timeout after {self.session.timeout} seconds")
            logger.error(f"   Error details: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ BioSim Client: Request failed with error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ BioSim Client: Unexpected error starting simulation: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            return None
    
    def get_simulation_log(self, sim_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve simulation log/history for a specific simulation ID.
        
        Args:
            sim_id: The simulation ID to retrieve logs for
            
        Returns:
            Simulation log data if successful, None otherwise
        """
        try:
            logger.info(f"📋 BioSim Client: Retrieving simulation log for ID: {sim_id}")
            
            api_url = f"{self.base_url}/api/simulation/{sim_id}/log"
            logger.info(f"🌐 BioSim Client: Making GET request to: {api_url}")
            
            response = self.session.get(api_url)
            
            logger.info(f"📡 BioSim Client: Log response received - Status: {response.status_code}")
            
            if response.status_code == 200:
                log_data = response.json()
                logger.info(f"✅ BioSim Client: Successfully retrieved simulation log for ID {sim_id}")
                logger.info(f"📊 BioSim Client: Log data keys: {list(log_data.keys()) if isinstance(log_data, dict) else 'Not a dict'}")
                logger.info(f"📊 BioSim Client: Log data size: {len(str(log_data))} characters")
                return log_data
            else:
                logger.error(f"❌ BioSim Client: Failed to get simulation log")
                logger.error(f"   Status Code: {response.status_code}")
                logger.error(f"   Response Text: {response.text}")
                logger.error(f"   Response Headers: {dict(response.headers)}")
                return None
                
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ BioSim Client: Connection error getting log for simulation {sim_id}")
            logger.error(f"   Error details: {e}")
            return None
        except requests.exceptions.Timeout as e:
            logger.error(f"❌ BioSim Client: Timeout getting log for simulation {sim_id}")
            logger.error(f"   Error details: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ BioSim Client: Request failed getting log for simulation {sim_id}")
            logger.error(f"   Error details: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ BioSim Client: Unexpected error getting log for simulation {sim_id}: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            return None
    
    def get_sensor_data_from_log(self, sim_id: int, sensor_name: str, duration_seconds: int = None) -> Optional[List[float]]:
        """
        Extract sensor data from simulation log for physics diagnosis.
        
        Args:
            sim_id: The simulation ID
            sensor_name: Name of the sensor to extract data for
            duration_seconds: Optional duration limit for data extraction
            
        Returns:
            List of sensor values if successful, None otherwise
        """
        try:
            logger.info(f"🔍 BioSim Client: Extracting sensor data for '{sensor_name}' from simulation {sim_id}")
            
            # Get the simulation log
            log_data = self.get_simulation_log(sim_id)
            if not log_data:
                logger.error(f"❌ BioSim Client: No log data available for simulation {sim_id}")
                return None
            
            # Extract sensor data from the log
            sensor_values, _ = self._extract_sensor_values_from_log(log_data, sensor_name)
            
            if sensor_values:
                logger.info(f"✅ BioSim Client: Successfully extracted {len(sensor_values)} values for sensor '{sensor_name}'")
                logger.info(f"📊 BioSim Client: Sensor values range: [{min(sensor_values):.4f}, {max(sensor_values):.4f}]")
                
                # Apply duration limit if specified
                if duration_seconds and len(sensor_values) > duration_seconds:
                    original_length = len(sensor_values)
                    sensor_values = sensor_values[-duration_seconds:]
                    logger.info(f"🔧 BioSim Client: Limited sensor data from {original_length} to {len(sensor_values)} values (last {duration_seconds} seconds)")
                
                return sensor_values
            else:
                logger.warning(f"⚠️ BioSim Client: No data found for sensor '{sensor_name}' in simulation {sim_id}")
                logger.info(f"🔍 BioSim Client: Available data structure: {json.dumps(log_data, indent=2)[:500]}...")
                return None
                
        except Exception as e:
            logger.error(f"❌ BioSim Client: Error extracting sensor data for sensor '{sensor_name}' from simulation {sim_id}: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            return None
    
    def _extract_sensor_values_from_log(self, log_data: Dict[str, Any], sensor_name: str) -> tuple[List[float], List[str]]:
        """
        Extract sensor values and units from simulation log data.
        
        Args:
            log_data: The simulation log data
            sensor_name: Name of the sensor to extract
            
        Returns:
            Tuple of (sensor_values, sensor_units)
        """
        try:
            logger.info(f"🔍 BioSim Client: Parsing log data structure for sensor '{sensor_name}'")
            logger.info(f"📊 BioSim Client: Log data top-level keys: {list(log_data.keys()) if isinstance(log_data, dict) else 'Not a dict'}")
            
            sensor_values = []
            sensor_units = []  # Track units for each value
            
            # BioSim log data structure: {'ticks': [{'modules': {sensor_name: {...}}}, ...]}
            if 'ticks' in log_data and isinstance(log_data['ticks'], list):
                logger.info(f"🔍 BioSim Client: Found 'ticks' array with {len(log_data['ticks'])} entries")
                
                for tick_index, tick in enumerate(log_data['ticks']):
                    if isinstance(tick, dict) and 'modules' in tick:
                        modules = tick['modules']
                        if sensor_name in modules:
                            sensor_module = modules[sensor_name]
                            if isinstance(sensor_module, dict) and 'properties' in sensor_module:
                                properties = sensor_module['properties']
                                if 'value' in properties:
                                    value = properties['value']
                                    unit = properties.get('unit', 'unknown')  # Extract unit information
                                    
                                    if value is not None:
                                        try:
                                            sensor_values.append(float(value))
                                            sensor_units.append(unit)  # Store unit with each value
                                            logger.debug(f"✅ BioSim Client: Found value {value} ({unit}) in tick[{tick_index}].modules.{sensor_name}.properties.value")
                                        except (ValueError, TypeError):
                                            logger.warning(f"⚠️ BioSim Client: Invalid sensor value for {sensor_name}: {value}")
                                            continue
                                    else:
                                        logger.debug(f"🔍 BioSim Client: No value found in tick[{tick_index}].modules.{sensor_name}.properties")
                                else:
                                    logger.debug(f"🔍 BioSim Client: No 'properties' found in tick[{tick_index}].modules.{sensor_name}")
                            else:
                                logger.debug(f"🔍 BioSim Client: No 'properties' found in tick[{tick_index}].modules.{sensor_name}")
                        else:
                            logger.debug(f"🔍 BioSim Client: Sensor '{sensor_name}' not found in tick[{tick_index}].modules")
                    else:
                        logger.debug(f"🔍 BioSim Client: No 'modules' found in tick[{tick_index}]")
            
            # If no data found in expected structure, try alternative paths for backward compatibility
            if not sensor_values:
                logger.info(f"🔍 BioSim Client: No data found in 'ticks' structure, trying alternative paths...")
                
                # Try the old structure that was in the original code
                if 'data' in log_data and isinstance(log_data['data'], list):
                    logger.info(f"🔍 BioSim Client: Trying 'data' array with {len(log_data['data'])} entries")
                    for i, entry in enumerate(log_data['data']):
                        if isinstance(entry, dict) and 'sensors' in entry:
                            if sensor_name in entry['sensors']:
                                value = entry['sensors'][sensor_name].get('value')
                                unit = entry['sensors'][sensor_name].get('unit', 'unknown')  # Extract unit
                                if value is not None:
                                    try:
                                        sensor_values.append(float(value))
                                        sensor_units.append(unit)  # Store unit
                                        logger.debug(f"✅ BioSim Client: Found value {value} ({unit}) in data[{i}].sensors.{sensor_name}")
                                    except (ValueError, TypeError):
                                        logger.warning(f"⚠️ BioSim Client: Invalid sensor value for {sensor_name}: {value}")
                                        continue
                
                # Try telemetry structure
                if not sensor_values and 'telemetry' in log_data and isinstance(log_data['telemetry'], list):
                    logger.info(f"🔍 BioSim Client: Trying 'telemetry' array with {len(log_data['telemetry'])} entries")
                    for i, entry in enumerate(log_data['telemetry']):
                        if isinstance(entry, dict) and sensor_name in entry:
                            value = entry[sensor_name]
                            unit = entry.get('unit', 'unknown')  # Extract unit
                            if value is not None:
                                try:
                                    sensor_values.append(float(value))
                                    sensor_units.append(unit)  # Store unit
                                    logger.debug(f"✅ BioSim Client: Found value {value} ({unit}) in telemetry[{i}].{sensor_name}")
                                except (ValueError, TypeError):
                                    logger.warning(f"⚠️ BioSim Client: Invalid telemetry value for {sensor_name}: {value}")
                                    continue
            
            # Log unit information summary
            if sensor_values and sensor_units:
                unique_units = list(set(sensor_units))
                logger.info(f"📊 BioSim Client: Extracted {len(sensor_values)} values for sensor '{sensor_name}' with units: {unique_units}")
                
                # Check if we have consistent units
                if len(unique_units) == 1:
                    logger.info(f"✅ BioSim Client: All values have consistent unit: {unique_units[0]}")
                else:
                    logger.warning(f"⚠️ BioSim Client: Inconsistent units detected: {unique_units}")
            
            return sensor_values, sensor_units
            
        except Exception as e:
            logger.error(f"❌ BioSim Client: Error parsing sensor values from log data: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            return [], []
    
    def check_server_status(self) -> bool:
        """
        Check if BioSim server is accessible using an existing endpoint.
        
        Returns:
            True if server is accessible, False otherwise
        """
        if not self.enable_biosim:
            logger.info(f"🏥 BioSim Client: Skipping health check - BioSim integration disabled")
            return False
            
        try:
            # Use the /api/simulation endpoint which we know exists
            logger.info(f"🏥 BioSim Client: Checking server availability at {self.base_url}/api/simulation")
            
            response = self.session.get(f"{self.base_url}/api/simulation", timeout=self.health_check_timeout)
            
            # Any response means the server is running
            logger.info(f"✅ BioSim Client: Server is responding (status: {response.status_code})")
            
            if response.status_code == 200:
                # Try to parse the response to see if it's valid
                try:
                    simulations = response.json()
                    logger.info(f"📊 BioSim Client: Found {len(simulations) if isinstance(simulations, list) else 'unknown'} simulations")
                except Exception as e:
                    logger.warning(f"⚠️ BioSim Client: Could not parse simulation list response: {e}")
                
                return True
            else:
                logger.warning(f"⚠️ BioSim Client: Server responded with status {response.status_code}")
                # Still return True if server is responding (even with error)
                return True
                
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"⚠️ BioSim Client: Cannot connect to BioSim server - connection refused")
            logger.debug(f"   Connection error details: {e}")
            return False
        except requests.exceptions.Timeout as e:
            logger.warning(f"⚠️ BioSim Client: BioSim server health check timed out after {self.health_check_timeout} seconds")
            logger.debug(f"   Timeout error details: {e}")
            return False
        except Exception as e:
            logger.warning(f"⚠️ BioSim Client: BioSim server health check failed: {e}")
            logger.debug(f"   Error type: {type(e).__name__}")
            return False
    
    def get_available_sensors(self, sim_id: int) -> Optional[List[str]]:
        """
        Get list of available sensors for a simulation.
        
        Args:
            sim_id: The simulation ID
            
        Returns:
            List of available sensor names if successful, None otherwise
        """
        try:
            logger.info(f"🔍 BioSim Client: Getting available sensors for simulation {sim_id}")
            
            log_data = self.get_simulation_log(sim_id)
            if not log_data:
                logger.warning(f"⚠️ BioSim Client: No log data available to extract sensors from simulation {sim_id}")
                return None
            
            # Extract sensor names from log data
            sensors = set()
            
            if 'data' in log_data and isinstance(log_data['data'], list):
                for entry in log_data['data']:
                    if isinstance(entry, dict) and 'sensors' in entry:
                        sensors.update(entry['sensors'].keys())
            
            if 'telemetry' in log_data and isinstance(log_data['telemetry'], list):
                for entry in log_data['telemetry']:
                    if isinstance(entry, dict):
                        sensors.update(entry.keys())
            
            if sensors:
                sensor_list = list(sensors)
                logger.info(f"✅ BioSim Client: Found {len(sensor_list)} available sensors: {sensor_list}")
                return sensor_list
            else:
                logger.warning(f"⚠️ BioSim Client: No sensors found in simulation {sim_id}")
                return None
            
        except Exception as e:
            logger.error(f"❌ BioSim Client: Error getting available sensors for simulation {sim_id}: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            return None

    def _create_anomaly_config(self, anomaly_name: str, duration_seconds: int) -> Optional[str]:
        """
        Create a BioSim configuration file for a specific anomaly.
        
        Args:
            anomaly_name: Name of the anomaly to simulate
            duration_seconds: Duration of the simulation in seconds
            
        Returns:
            Path to the created configuration file, or None if failed
        """
        try:
            logger.info(f"📄 BioSim Client: Creating configuration for anomaly: '{anomaly_name}'")
            
            # Import the template module
            try:
                from .biosim_templates import generate_config
                logger.info(f"✅ BioSim Client: Successfully imported configuration templates")
            except ImportError as e:
                logger.error(f"❌ BioSim Client: Failed to import configuration templates: {e}")
                return None
            
            # Create a temporary configuration file
            import tempfile
            import os
            
            # Create a unique filename based on anomaly name and timestamp
            import time
            timestamp = int(time.time())
            safe_anomaly_name = anomaly_name.replace(' ', '_').replace('(', '').replace(')', '').replace('²', '2')
            filename = f"biosim_config_{safe_anomaly_name}_{timestamp}.biosim"
            
            config_path = os.path.join(tempfile.gettempdir(), filename)
            
            # Generate configuration content using the template
            config_content = generate_config(anomaly_name, duration_seconds)
            
            if not config_content:
                logger.error(f"❌ BioSim Client: Could not generate configuration content for anomaly: '{anomaly_name}'")
                return None
            
            # Write configuration to file
            with open(config_path, 'w') as f:
                f.write(config_content)
            
            logger.info(f"✅ BioSim Client: Created configuration file: {config_path}")
            logger.info(f"📄 BioSim Client: Configuration file size: {len(config_content)} characters")
            
            return config_path
            
        except Exception as e:
            logger.error(f"❌ BioSim Client: Error creating anomaly configuration: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            return None

    def cleanup_temp_config(self, config_file_path: str) -> bool:
        """
        Clean up temporary configuration file.
        
        Args:
            config_file_path: Path to the configuration file to remove
            
        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            if config_file_path and os.path.exists(config_file_path):
                os.remove(config_file_path)
                logger.info(f"🧹 BioSim Client: Cleaned up temporary config file: {config_file_path}")
                return True
            return False
        except Exception as e:
            logger.warning(f"⚠️ BioSim Client: Could not clean up config file {config_file_path}: {e}")
            return False

    def get_sensor_data_with_units(self, sim_id: int, sensor_name: str, duration_seconds: int = None, target_unit: str = 'mmHg') -> Optional[Dict[str, Any]]:
        """
        Get sensor data from BioSim simulation with unit conversion support.
        
        Args:
            sim_id: The simulation ID
            sensor_name: Name of the sensor to extract
            duration_seconds: Optional duration limit for the data
            target_unit: Target unit for conversion (default: mmHg)
            
        Returns:
            Dictionary containing:
            - values: List of converted sensor values
            - original_units: List of original units
            - target_unit: Target unit after conversion
            - conversion_applied: Boolean indicating if conversion was performed
        """
        try:
            logger.info(f"🔍 BioSim Client: Getting sensor data with units for '{sensor_name}' from simulation {sim_id}")
            logger.info(f"🎯 BioSim Client: Target unit: {target_unit}")
            
            # Get the simulation log
            log_data = self.get_simulation_log(sim_id)
            if not log_data:
                logger.warning(f"⚠️ BioSim Client: No log data available for simulation {sim_id}")
                return None
            
            # Extract sensor values and units
            sensor_values, sensor_units = self._extract_sensor_values_from_log(log_data, sensor_name)
            
            if not sensor_values:
                logger.warning(f"⚠️ BioSim Client: No data found for sensor '{sensor_name}' in simulation {sim_id}")
                return None
            
            # Check if we have consistent units
            unique_units = list(set(sensor_units))
            
            # Handle case where no units are found or all units are 'unknown'
            if len(unique_units) == 0 or (len(unique_units) == 1 and unique_units[0] == 'unknown'):
                logger.info(f"🔧 BioSim Client: No unit information found, assuming kPa as default for BioSim data")
                logger.info(f"🔧 BioSim Client: This is typical for BioSim simulations where units are not explicitly specified")
                source_unit = 'kPa'
                # Fill the units list with assumed units
                sensor_units = ['kPa'] * len(sensor_values)
                logger.info(f"🔧 BioSim Client: Applied 'kPa' unit to all {len(sensor_values)} sensor values")
            elif len(unique_units) != 1:
                logger.warning(f"⚠️ BioSim Client: Inconsistent units detected: {unique_units}")
                # Use the most common unit
                from collections import Counter
                most_common_unit = Counter(sensor_units).most_common(1)[0][0]
                if most_common_unit == 'unknown':
                    logger.info(f"🔧 BioSim Client: Most common unit is 'unknown', assuming kPa as default")
                    logger.info(f"🔧 BioSim Client: This is typical for BioSim simulations where units are not explicitly specified")
                    source_unit = 'kPa'
                    # Fill the units list with assumed units
                    sensor_units = ['kPa'] * len(sensor_values)
                    logger.info(f"🔧 BioSim Client: Applied 'kPa' unit to all {len(sensor_values)} sensor values")
                else:
                    logger.info(f"🔧 BioSim Client: Using most common unit: {most_common_unit}")
                    source_unit = most_common_unit
            else:
                source_unit = unique_units[0]
                if source_unit == 'unknown':
                    logger.info(f"🔧 BioSim Client: Unit is 'unknown', assuming kPa as default for BioSim data")
                    logger.info(f"🔧 BioSim Client: This is typical for BioSim simulations where units are not explicitly specified")
                    source_unit = 'kPa'
                    # Fill the units list with assumed units
                    sensor_units = ['kPa'] * len(sensor_values)
                    logger.info(f"🔧 BioSim Client: Applied 'kPa' unit to all {len(sensor_values)} sensor values")
            
            logger.info(f"📊 BioSim Client: Source unit: {source_unit}, Target unit: {target_unit}")
            
            # Apply unit conversion if needed
            converted_values = sensor_values.copy()
            conversion_applied = False
            
            if source_unit.lower() != target_unit.lower():
                logger.info(f"🔄 BioSim Client: Converting from {source_unit} to {target_unit}")
                
                try:
                    if source_unit.lower() == 'kpa' and target_unit.lower() == 'mmhg':
                        # Convert kPa to mmHg using biosim_utils
                        converted_values = [self.kpa_to_mmhg(value) for value in sensor_values]
                        conversion_applied = True
                        logger.info(f"✅ BioSim Client: Successfully converted {len(converted_values)} values from kPa to mmHg")
                    elif source_unit.lower() == 'kpa' and target_unit.lower() == 'psi':
                        # Convert kPa to PSI using biosim_utils
                        converted_values = [self.kpa_to_psi(value) for value in sensor_values]
                        conversion_applied = True
                        logger.info(f"✅ BioSim Client: Successfully converted {len(converted_values)} values from kPa to PSI")
                    else:
                        logger.warning(f"⚠️ BioSim Client: Unit conversion from {source_unit} to {target_unit} not supported")
                        # Keep original values
                        converted_values = sensor_values
                except Exception as e:
                    logger.error(f"❌ BioSim Client: Error during unit conversion: {e}")
                    # Keep original values on conversion error
                    converted_values = sensor_values
            else:
                logger.info(f"✅ BioSim Client: No unit conversion needed (already in {target_unit})")
            
            # Apply duration limit if specified
            if duration_seconds and len(converted_values) > duration_seconds:
                original_length = len(converted_values)
                converted_values = converted_values[-duration_seconds:]
                sensor_units = sensor_units[-duration_seconds:]  # Keep units in sync
                logger.info(f"🔧 BioSim Client: Limited sensor data from {original_length} to {len(converted_values)} values (last {duration_seconds} seconds)")
            
            # Log final summary
            logger.info(f"📊 BioSim Client: Final result summary:")
            logger.info(f"   - Sensor: {sensor_name}")
            logger.info(f"   - Values extracted: {len(converted_values)}")
            logger.info(f"   - Source unit: {source_unit}")
            logger.info(f"   - Target unit: {target_unit}")
            logger.info(f"   - Conversion applied: {conversion_applied}")
            if conversion_applied:
                logger.info(f"   - Sample values: {converted_values[:3]}... (converted from {source_unit} to {target_unit})")
            else:
                logger.info(f"   - Sample values: {converted_values[:3]}... (no conversion needed)")
            
            return {
                'values': converted_values,
                'original_units': sensor_units,
                'target_unit': target_unit,
                'conversion_applied': conversion_applied,
                'source_unit': source_unit
            }
                
        except Exception as e:
            logger.error(f"❌ BioSim Client: Error getting sensor data with units for sensor '{sensor_name}' from simulation {sim_id}: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            return None

    def kpa_to_mmhg(self, kpa_value: float) -> float:
        """Convert kPa to mmHg using biosim_utils function."""
        try:
            from .biosim_utils import kpa_to_mmhg
            return kpa_to_mmhg(kpa_value)
        except ImportError:
            logger.warning(f"⚠️ BioSim Client: Could not import kpa_to_mmhg from biosim_utils")
            # Fallback conversion: 1 kPa ≈ 7.50062 mmHg
            return kpa_value * 7.50062

    def kpa_to_psi(self, kpa_value: float) -> float:
        """Convert kPa to PSI using biosim_utils function."""
        try:
            from .biosim_utils import kpa_to_psi
            return kpa_to_psi(kpa_value)
        except ImportError:
            logger.warning(f"⚠️ BioSim Client: Could not import kpa_to_psi from biosim_utils")
            # Fallback conversion: 1 kPa ≈ 0.145038 PSI
            return kpa_value * 0.145038

    def check_simulation_status(self, sim_id: int) -> Optional[Dict[str, Any]]:
        """
        Check the current status of a simulation.
        
        Args:
            sim_id: The simulation ID to check
            
        Returns:
            Simulation status data if successful, None otherwise
        """
        try:
            logger.info(f"🔍 BioSim Client: Checking status for simulation {sim_id}")
            
            api_url = f"{self.base_url}/api/simulation/{sim_id}"
            logger.debug(f"🌐 BioSim Client: Making GET request to: {api_url}")
            
            response = self.session.get(api_url)
            
            if response.status_code == 200:
                status_data = response.json()
                simulation_ended = status_data.get('globals', {}).get('simulationEnded', False)
                logger.info(f"✅ BioSim Client: Simulation {sim_id} status - ended: {simulation_ended}")
                return status_data
            else:
                logger.warning(f"⚠️ BioSim Client: Failed to get simulation status - Status: {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError as e:
            logger.error(f"❌ BioSim Client: Connection error checking simulation {sim_id} status: {e}")
            return None
        except requests.exceptions.Timeout as e:
            logger.error(f"❌ BioSim Client: Timeout checking simulation {sim_id} status: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ BioSim Client: Error checking simulation {sim_id} status: {e}")
            return None

    def wait_for_simulation_completion(self, sim_id: int, max_wait_seconds: int = 300, poll_interval: float = 0.5) -> bool:
        """
        Wait for a simulation to complete by polling its status.
        
        Args:
            sim_id: The simulation ID to wait for
            max_wait_seconds: Maximum time to wait in seconds (default: 300)
            poll_interval: How often to check status in seconds (default: 0.5)
            
        Returns:
            True if simulation completed, False if timeout exceeded
        """
        import time
        
        logger.info(f"⏳ BioSim Client: Waiting for simulation {sim_id} to complete (max {max_wait_seconds}s)")
        
        start_time = time.time()
        last_log_time = 0
        
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            # Check if we've exceeded the maximum wait time
            if elapsed_time >= max_wait_seconds:
                logger.warning(f"⏰ BioSim Client: Timeout waiting for simulation {sim_id} after {elapsed_time:.1f}s")
                return False
            
            # Check simulation status
            status_data = self.check_simulation_status(sim_id)
            
            if status_data is None:
                # If we can't get status, wait a bit and retry
                logger.debug(f"🔄 BioSim Client: Could not get status for simulation {sim_id}, retrying...")
                time.sleep(poll_interval)
                continue
            
            # Check if simulation has ended
            simulation_ended = status_data.get('globals', {}).get('simulationEnded', False)
            
            if simulation_ended:
                completion_time = current_time - start_time
                logger.info(f"✅ BioSim Client: Simulation {sim_id} completed after {completion_time:.1f}s")
                return True
            
            # Log progress every 5 seconds
            if current_time - last_log_time >= 5.0:
                logger.info(f"⏳ BioSim Client: Simulation {sim_id} still running... ({elapsed_time:.1f}s elapsed)")
                last_log_time = current_time
            
            # Wait before next poll
            time.sleep(poll_interval)
