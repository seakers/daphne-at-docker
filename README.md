# Daphne AT Docker

## Prerequisites

- Docker Desktop ([Download](https://www.docker.com/products/docker-desktop))
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/seakers/daphne-at-docker.git
cd daphne-at-docker
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

