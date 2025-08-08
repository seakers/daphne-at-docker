# CDRA Simulation Framework in Python
import numpy as np
import matplotlib.pyplot as plt

# Constants and initial setup

# Simulation parameters
SIM_DURATION_SEC = 10000
TIME_STEP_SEC = 1
TIME_END = SIM_DURATION_SEC  # Total simulation time in seconds
DT = TIME_STEP_SEC           # Time step size in seconds

# Environmental input levels
M_CABIN = 100.0             # kg, dry air mass in the cabin
MOISTURE_CONTENT_INIT = 0.015  # kg H2O/kg dry air (initial value)  # kg H2O/kg dry air
CO2_CONTENT_INIT = 0.004  # kg CO2/kg dry air (initial value)  # kg CO2/kg dry air
MOISTURE_INPUT_MEAN = 0.00005 * 30 
CO2_INPUT_MEAN = 0.00002 * 30
MOISTURE_MAX = 0.03
CO2_MAX = 0.01
NOISE_SCALE = 0.0002 * 0   # Magnitude of noise for air composition generation

# CDRA operational constants
INITIAL_SATURATION_LEVEL = 0.0
REGENERATION_RATE_MULTIPLIER = 2.0
AIR_FLOW_RATE = 1.0  # kg/s, nominal air flow rate  # kg/s, nominal air flow rate
VALVE_SWITCH_INTERVAL = 200
SATURATION_TIME_CONSTANT = 600  # time for saturation to reach 1.0
BASE_ADSORPTION_EFF = 0.05
MAX_ADSORPTION_EFF_INCREMENT = 0.15
DESORPTION_MULTIPLIER = 1.05

# Failure scenarios with activation flags and timing
FAILURE_SCENARIO = {
    'filter_saturation': False,
    'filter_saturation_start': TIME_END,
    'filter_saturation_end': TIME_END,
    'heater_failure': [],
    'sensor_failure': [],
    'valve_stuck': False,
    'valve_stuck_start': TIME_END,
    'valve_stuck_end': TIME_END,
    'fan_degraded': False,              # NEW: Whether fan degradation is active
    'fan_degraded_start': 1000,           # NEW: When fan degradation starts
    'fan_degraded_end': TIME_END,        # NEW: When fan degradation ends
    'degraded_flow_rate': 0.5            # NEW: Degraded flow rate (kg/s)
}

# System state class
class CDRAState:
    def __init__(self):
        self.saturation = {k: INITIAL_SATURATION_LEVEL for k in ['desiccant_1', 'desiccant_3', 'sorbent_2', 'sorbent_4']}
        self.adsorption_eff = {k: BASE_ADSORPTION_EFF for k in ['desiccant_1', 'desiccant_3', 'sorbent_2', 'sorbent_4']}
        self.time = 0
        self.air_flow_rate = AIR_FLOW_RATE  
        self.moisture_content = MOISTURE_CONTENT_INIT  
        self.co2_content = CO2_CONTENT_INIT  
        self.co2_removed_total = 0.0
        self.heater_on = {'desiccant_1': False, 'desiccant_3': False, 'sorbent_2': False, 'sorbent_4': False}
        self.valve_state = {'path_1_active': True}  # alternate paths for redundancy

        # For plotting
        self.history = {
            'saturation': {k: [] for k in ['desiccant_1', 'desiccant_3', 'sorbent_2', 'sorbent_4']},
            'adsorption_eff': {k: [] for k in ['desiccant_1', 'desiccant_3', 'sorbent_2', 'sorbent_4']},
            'time': [],
            'moisture_content': [],
            'co2_content': [],
            'co2_removed': [],
            'air_flow_rate': [],
            'desiccant_heaters': [],
            'sorbent_heaters': [],
            'active_path': [],
            'desiccant_1_heater': [],
            'desiccant_3_heater': [],
            'sorbent_2_heater': [],
            'sorbent_4_heater': []
        }

# Failure injection function
def apply_failures(state: CDRAState):
    # Existing failures
    if FAILURE_SCENARIO['filter_saturation_start'] is not None and \
       FAILURE_SCENARIO['filter_saturation_end'] is not None and \
       FAILURE_SCENARIO['filter_saturation_start'] <= state.time <= FAILURE_SCENARIO['filter_saturation_end']:
        FAILURE_SCENARIO['filter_saturation'] = True
    else:
        FAILURE_SCENARIO['filter_saturation'] = False
    
    if FAILURE_SCENARIO['filter_saturation']:
        # Force saturation to full (1.0) for all filters
        for component in state.saturation:
            state.saturation[component] = 1.0
            state.adsorption_eff[component] = BASE_ADSORPTION_EFF + MAX_ADSORPTION_EFF_INCREMENT * 1.0

    if FAILURE_SCENARIO['valve_stuck_start'] <= state.time <= FAILURE_SCENARIO['valve_stuck_end']:
        FAILURE_SCENARIO['valve_stuck'] = True
    else:
        FAILURE_SCENARIO['valve_stuck'] = False
    
    # --- Valve Stcuk Handling ---
    if FAILURE_SCENARIO['valve_stuck']:
        state.valve_state['path_1_active'] = state.valve_state['path_1_active']  # freeze valve

    for heater in FAILURE_SCENARIO['heater_failure']:
        state.heater_on[heater] = False

    # --- NEW Fan Degradation Handling ---
    if FAILURE_SCENARIO['fan_degraded_start'] <= state.time <= FAILURE_SCENARIO['fan_degraded_end']:
        FAILURE_SCENARIO['fan_degraded'] = True
    else:
        FAILURE_SCENARIO['fan_degraded'] = False

    if FAILURE_SCENARIO['fan_degraded']:
        state.air_flow_rate = FAILURE_SCENARIO['degraded_flow_rate']
    else:
        state.air_flow_rate = AIR_FLOW_RATE  # restore nominal if no failure

# Time step physics function
def timestep(state: CDRAState):
    #co2_before = state.co2_content

    def update_filter(component):
        if state.heater_on[component]:
            state.saturation[component] = max(state.saturation[component] - REGENERATION_RATE_MULTIPLIER * DT / SATURATION_TIME_CONSTANT, 0.0)
        else:
            state.saturation[component] = min(state.saturation[component] + DT / SATURATION_TIME_CONSTANT, 1.0)
        state.adsorption_eff[component] = BASE_ADSORPTION_EFF + MAX_ADSORPTION_EFF_INCREMENT * (1 - state.saturation[component])
    # Apply generation to cabin first
    #state.moisture_content += MOISTURE_INPUT_MEAN + np.random.normal(0, NOISE_SCALE)
    #state.co2_content += CO2_INPUT_MEAN + np.random.normal(0, NOISE_SCALE)
    apply_failures(state)

    # Update filters
    update_filter('desiccant_1')
    update_filter('sorbent_2')
    update_filter('desiccant_3')
    update_filter('sorbent_4')
 
    # Get current efficiency
    # Determine which path is active
    if state.valve_state['path_1_active']:
        eta_co2 = state.adsorption_eff['sorbent_2'] if not state.heater_on['sorbent_2'] else -DESORPTION_MULTIPLIER
    else:
        eta_co2 = state.adsorption_eff['sorbent_4'] if not state.heater_on['sorbent_4'] else -DESORPTION_MULTIPLIER

    # Apply efficiency to compute outlet CO2 concentration
    C_in = state.co2_content
    C_out = C_in * (1 - eta_co2) if eta_co2 >= 0 else C_in * eta_co2

    for k in state.saturation:
        state.history['saturation'][k].append(state.saturation[k])
        state.history['adsorption_eff'][k].append(state.adsorption_eff[k])

    return C_out, state.air_flow_rate

    # Similar treatment can be done for moisture if needed

    # calculate the co2 removal
    # co2_after = state.co2_content
    # removed = max(co2_before - co2_after, 0)
    # state.co2_removed_total += removed

    # for k in state.saturation:
    #     state.history['saturation'][k].append(state.saturation[k])
    #     state.history['adsorption_eff'][k].append(state.adsorption_eff[k])
    # state.history['co2_removed'].append(state.co2_removed_total)

  
    #state.moisture_content = max(0, min(state.moisture_content, MOISTURE_MAX))
    #state.co2_content = max(0, min(state.co2_content, CO2_MAX))

# New function to handle cabin concentration update
def update_cabin_concentration(state: CDRAState, C_out: float, flow: float):
    """
    Updates the cabin CO2 concentration using two-space mixing model.
    """
    state.co2_content = ((1 - flow / M_CABIN) * state.co2_content +
                         (flow / M_CABIN) * C_out +
                         CO2_INPUT_MEAN / M_CABIN)
# Control function
def control(state: CDRAState):
    if not FAILURE_SCENARIO['valve_stuck'] and state.time % VALVE_SWITCH_INTERVAL == 0 and state.time != 0:
        state.valve_state['path_1_active'] = not state.valve_state['path_1_active']

    state.heater_on['desiccant_1'] = not state.valve_state['path_1_active']
    state.heater_on['desiccant_3'] = state.valve_state['path_1_active']
    state.heater_on['sorbent_2'] = not state.valve_state['path_1_active']
    state.heater_on['sorbent_4'] = state.valve_state['path_1_active']

# Plotting function
def plot_results(state: CDRAState):
    plt.figure(figsize=(14, 10))

    plt.subplot(4, 1, 1)
    plt.plot(state.history['time'], state.history['moisture_content'], label='Moisture Content')
    plt.plot(state.history['time'], state.history['co2_content'], label='CO2 Content')
    plt.ylabel('kg/kg dry air')
    plt.title('Gas Concentration Over Time')
    plt.legend()
    plt.grid()

    plt.subplot(4, 1, 2)
    plt.plot(state.history['time'], state.history['air_flow_rate'], label='Air Flow Rate')
    plt.ylabel('kg/s')
    plt.title('Air Flow Rate Over Time')
    plt.grid()

    plt.subplot(4, 1, 3)
    plt.plot(state.history['time'], state.history['desiccant_1_heater'], label='Desiccant 1 Heater')
    plt.plot(state.history['time'], state.history['desiccant_3_heater'], label='Desiccant 3 Heater')
    plt.plot(state.history['time'], state.history['sorbent_2_heater'], label='Sorbent 2 Heater')
    plt.plot(state.history['time'], state.history['sorbent_4_heater'], label='Sorbent 4 Heater')
    plt.ylabel('Heater Status')
    plt.title('Heater Status Over Time')
    plt.legend()
    plt.grid()

    plt.subplot(4, 1, 4)
    path_states = [1 if active else 2 for active in state.history['active_path']]
    plt.step(state.history['time'], path_states, label='Active Path')
    plt.ylabel('Path #')
    plt.title('Active Path Over Time')
    plt.xlabel('Time (s)')
    plt.grid()

    plt.tight_layout()

    # Additional plot for saturation and efficiency
    components = ['desiccant_1', 'desiccant_3', 'sorbent_2', 'sorbent_4']
    plt.figure(figsize=(14, 6))
    for k in components:
        plt.plot(state.history['time'], state.history['saturation'][k], label=f'{k} Saturation')
    plt.title('Saturation Levels by Component')
    plt.xlabel('Time (s)')
    plt.ylabel('Saturation')
    plt.legend()
    plt.grid()

    plt.figure(figsize=(14, 6))
    for k in components:
        plt.plot(state.history['time'], state.history['adsorption_eff'][k], label=f'{k} Adsorption Eff.')
    plt.title('Adsorption Efficiency by Component')
    plt.xlabel('Time (s)')
    plt.ylabel('Efficiency')
    plt.legend()
    plt.grid()

    plt.figure(figsize=(14, 4))
    plt.plot(state.history['time'], state.history['co2_removed'], label='Accumulated CO₂ Removed', color='green')
    plt.title('Cumulative CO₂ Removal Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('CO₂ Removed (kg/kg dry air)')
    plt.grid()
    plt.legend()
    
    plt.show()

# Main simulation function
def main():
    state = CDRAState()
    while state.time <= TIME_END:
        control(state)
        

        co2_before = state.co2_content # Warning! Is this concentration(kg/kg) or content(kg)?
        C_out, flow = timestep(state)
        update_cabin_concentration(state, C_out, flow)

        co2_after = state.co2_content # Warning! Is this concentration(kg/kg) or content(kg)?
        removed = max(co2_before - co2_after, 0) # Warning! Is this concentration(kg/kg) or content(kg)?
        state.co2_removed_total += removed # Warning! Is this concentration(kg/kg) or content(kg)?


        state.history['time'].append(state.time)
        state.history['moisture_content'].append(state.moisture_content)
        state.history['co2_content'].append(state.co2_content)
        state.history['co2_removed'].append(state.co2_removed_total)
        state.history['air_flow_rate'].append(state.air_flow_rate)
        state.history['desiccant_heaters'].append((state.heater_on['desiccant_1'], state.heater_on['desiccant_3']))
        state.history['sorbent_heaters'].append((state.heater_on['sorbent_2'], state.heater_on['sorbent_4']))
        state.history['active_path'].append(state.valve_state['path_1_active'])
        state.history['desiccant_1_heater'].append(int(state.heater_on['desiccant_1']))
        state.history['desiccant_3_heater'].append(int(state.heater_on['desiccant_3']))
        state.history['sorbent_2_heater'].append(int(state.heater_on['sorbent_2']))
        state.history['sorbent_4_heater'].append(int(state.heater_on['sorbent_4']))

        state.time += DT
    np.save("trend_ppCO2_fan_t=1000_0.5.npy", np.array(state.history['co2_content']))
    plot_results(state)

if __name__ == '__main__':
    main()
