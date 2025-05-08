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
git clone https://github.com/seakers/ECLSS.git
cd ECLSS
```

2. Create a virtual env
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the simulation
```bash
python simulation.py
```

# Modify the simulation

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
2. Add simulation values to the cabin variable so they appear in the telemetry feed. Ensure variable names match those defined in PARAMETER_INFO.
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
