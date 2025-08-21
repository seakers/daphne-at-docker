import requests
import json
import logging
from typing import Dict, List, Any, Optional
from django.conf import settings
import os

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
            sensor_values = self._extract_sensor_values_from_log(log_data, sensor_name)
            
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
    
    def _extract_sensor_values_from_log(self, log_data: Dict[str, Any], sensor_name: str) -> List[float]:
        """
        Extract sensor values from simulation log data.
        
        Args:
            log_data: The simulation log data
            sensor_name: Name of the sensor to extract
            
        Returns:
            List of sensor values
        """
        try:
            logger.info(f"🔍 BioSim Client: Parsing log data structure for sensor '{sensor_name}'")
            logger.info(f"📊 BioSim Client: Log data top-level keys: {list(log_data.keys()) if isinstance(log_data, dict) else 'Not a dict'}")
            
            sensor_values = []
            
            # Navigate through the log structure to find sensor data
            # This will depend on the actual structure of BioSim log data
            if 'data' in log_data and isinstance(log_data['data'], list):
                logger.info(f"🔍 BioSim Client: Found 'data' array with {len(log_data['data'])} entries")
                for i, entry in enumerate(log_data['data']):
                    if isinstance(entry, dict) and 'sensors' in entry:
                        if sensor_name in entry['sensors']:
                            value = entry['sensors'][sensor_name].get('value')
                            if value is not None:
                                try:
                                    sensor_values.append(float(value))
                                    logger.debug(f"✅ BioSim Client: Found value {value} in data[{i}].sensors.{sensor_name}")
                                except (ValueError, TypeError):
                                    logger.warning(f"⚠️ BioSim Client: Invalid sensor value for {sensor_name}: {value}")
                                    continue
            
            # If no data found in expected structure, try alternative paths
            if not sensor_values and 'telemetry' in log_data and isinstance(log_data['telemetry'], list):
                logger.info(f"🔍 BioSim Client: Trying 'telemetry' array with {len(log_data['telemetry'])} entries")
                for i, entry in enumerate(log_data['telemetry']):
                    if isinstance(entry, dict) and sensor_name in entry:
                        value = entry[sensor_name]
                        if value is not None:
                            try:
                                sensor_values.append(float(value))
                                logger.debug(f"✅ BioSim Client: Found value {value} in telemetry[{i}].{sensor_name}")
                            except (ValueError, TypeError):
                                logger.warning(f"⚠️ BioSim Client: Invalid telemetry value for {sensor_name}: {value}")
                                continue
            
            # Try other possible structures
            if not sensor_values:
                logger.info(f"🔍 BioSim Client: Trying alternative log data structures...")
                for key, value in log_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        logger.info(f"🔍 BioSim Client: Checking key '{key}' with {len(value)} entries")
                        # Look for sensor data in this array
                        for i, entry in enumerate(value):
                            if isinstance(entry, dict):
                                if sensor_name in entry:
                                    value = entry[sensor_name]
                                    if value is not None:
                                        try:
                                            sensor_values.append(float(value))
                                            logger.debug(f"✅ BioSim Client: Found value {value} in {key}[{i}].{sensor_name}")
                                        except (ValueError, TypeError):
                                            logger.warning(f"⚠️ BioSim Client: Invalid value for {sensor_name}: {value}")
                                            continue
            
            logger.info(f"📊 BioSim Client: Extracted {len(sensor_values)} values for sensor '{sensor_name}'")
            return sensor_values
            
        except Exception as e:
            logger.error(f"❌ BioSim Client: Error parsing sensor values from log data: {e}")
            logger.error(f"   Error type: {type(e).__name__}")
            return []
    
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
