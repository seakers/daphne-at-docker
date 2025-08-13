# Daphne AT Docker

## Prerequisites

- Docker Desktop ([Download](https://www.docker.com/products/docker-desktop))
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/seakers/daphne-at-docker.git
cd daphne-at-docker
git switch bayesian
```

2. Create a .env file in the daphne_brain folder and the open ai api key
```bash
api_key=APIKEY
```

3.Setup the docker container 
```bash
docker-compose up
```

## Access
Frontend: http://localhost
<br>
API: http://localhost:8002

# To run a simulation

1. Clone the repository:
```bash
git clone https://github.com/seakers/daphne-at-habitat.git
```

2. Create a virtual env
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the simulation
```bash
cd DaphneATsim
python simulation.py
```

# Modify the simulation
1. Open DaphneATsim/simulation_config.py and confirm REAL_TIME_MODE is True and TELEMETRY_FREQUENCY_HZ = 1.0. You can adjust  the simulation speed by changing SIMULATION_SPEED. Make sure TIME_STEPS is long enough for your demonstration.

```bash
REAL_TIME_MODE = True  # Set to False to run as fast as possible (no delays, for testing)
SIMULATION_SPEED = 10  # How many simulation steps to generate per real second
TELEMETRY_FREQUENCY_HZ = 1.0  # How many telemetry posts per real second (e.g., 1.0 = every 1 second)
TIME_STEPS = 100000  # Total number of simulation steps
ENABLE_PLOTTING = False # Whether to show matplotlib plots after simulation
```
1. Modify CDRA_FAILURES constants to set failure scenarios. By setting True for 'filter_saturation', 'valve_stuck', 'fan_degraded', or setting the list of failed heaters to 'heater_failure', the anomaly scenario is simulated.

```bash
CDRA_FAILURES = {
    'filter_saturation': False,
    'filter_saturation_start': 0,  # When filter saturation failure starts
    'filter_saturation_end': TIME_STEPS,    # When filter saturation failure ends
    
    'valve_stuck': True,
    'valve_stuck_start': 0,       # When valve stuck failure starts
    'valve_stuck_end': TIME_STEPS,         # When valve stuck failure ends
    
    'heater_failure': [],             # List of failed heaters (e.g., ['desiccant_1', 'sorbent_2'])
    
    'fan_degraded': False,
    'fan_degraded_start': 0,      # When fan degradation starts
    'fan_degraded_end': TIME_STEPS,        # When fan degradation ends
    'degraded_flow_rate': 0.38        # Degraded flow rate (kg/s)
}
```
# Configuration of telemetry feed
1. Modify the PARAMETER_INFO variable by updating or adding values to include upper and lower caution and warning limits. 
```bash
 PARAMETER_INFO = {
    "ppO2": {"DisplayName": "Cabin_ppO2", "Id": 43, "ParameterGroup": "L1", "NominalValue": 163.81,
             "UpperCautionLimit": 175.0, "UpperWarningLimit": 185.0, "LowerCautionLimit": 155.0,
             "LowerWarningLimit": 145.0, "Divisor": 100, "Name": "ppO2", "Unit":"mmHg"},
    "ppCO2": {"DisplayName": "Cabin_ppCO2", "Id": 44, "ParameterGroup": "L1", "NominalValue": 0.4,
              "UpperCautionLimit": 4.5, "UpperWarningLimit": 6.0, "LowerCautionLimit": -1.0,
              "LowerWarningLimit": -2.0, "Divisor": 100, "Name": "ppCO2", "Unit":"mmHg"},
    "humidity": {"DisplayName": "Humidity", "Id": 45, "ParameterGroup": "L1", "NominalValue": 52,
              "UpperCautionLimit": 61, "UpperWarningLimit": 70, "LowerCautionLimit": 50,
              "LowerWarningLimit": 40, "Divisor": 1, "Name": "Humidity", "Unit":"L"},
    "ppO21": {"DisplayName": "Cabin_ppO2", "Id": 43, "ParameterGroup": "L2", "NominalValue": 163.81,
             "UpperCautionLimit": 175.0, "UpperWarningLimit": 185.0, "LowerCautionLimit": 155.0,
             "LowerWarningLimit": 145.0, "Divisor": 100, "Name": "ppO2", "Unit":"mmHg"},
    "ppCO21": {"DisplayName": "Cabin_ppCO2", "Id": 44, "ParameterGroup": "L2", "NominalValue": 0.4,
              "UpperCautionLimit": 4.5, "UpperWarningLimit": 6.0, "LowerCautionLimit": -1.0,
              "LowerWarningLimit": -2.0, "Divisor": 100, "Name": "ppCO2", "Unit":"mmHg"},
}
```
1. Add simulation values to the cabin variable so they appear in the telemetry feed. Ensure variable names match those defined in PARAMETER_INFO. ppCO2/ppCO21 values are updated by the simulation, but other parameters can be modified manually (and the values are kept static).
```bash
cabin = {
    "ppO2": 150, 
    "ppCO2": 5, 
    "humidity": 65, 
     "ppO21": 155, 
    "ppCO21": 0.5, 
    "humidity1": 65, 
}
```
-->
