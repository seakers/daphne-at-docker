from typing import Dict, List, Optional, Tuple
import math
import random

# Compact CDRA simulator suitable for API usage (no plotting, no globals)

# Constants (kept lightweight; adjust as needed)
AIR_FLOW_RATE_NOMINAL = 1.0  # kg/s nominal
VALVE_SWITCH_INTERVAL = 200   # s
SATURATION_TIME_CONSTANT = 600.0
BASE_ADSORPTION_EFF = 0.05
MAX_ADSORPTION_EFF_INCREMENT = 0.15
DESORPTION_MULTIPLIER = 1.05
M_CABIN = 100.0
CO2_INPUT_MEAN = 0.00002 * 30

# Unit conversion constants for CO2
# Standard atmospheric pressure: 760 mmHg
# Molar mass of CO2: 44.01 g/mol
# Molar mass of air: 28.97 g/mol
# Ideal gas law: PV = nRT
STANDARD_PRESSURE_MMHG = 760.0
MOLAR_MASS_CO2 = 44.01  # g/mol
MOLAR_MASS_AIR = 28.97  # g/mol
GAS_CONSTANT_R = 8.314  # J/(mol·K)
STANDARD_TEMPERATURE_K = 298.15  # 25°C in Kelvin

def mmhg_to_kg_per_kg_air(co2_mmhg: float) -> float:
    """
    Convert CO2 partial pressure from mmHg to kg/kg air.
    
    Args:
        co2_mmhg: CO2 partial pressure in mmHg
        
    Returns:
        CO2 concentration in kg/kg air
    """
    # Convert mmHg to Pa (1 mmHg = 133.322 Pa)
    co2_pa = co2_mmhg * 133.322
    
    # Use ideal gas law: n/V = P/(RT)
    # Then convert to mass ratio: (n_CO2 * M_CO2) / (n_air * M_air)
    # Since we're working with ratios, we can simplify
    co2_mol_per_mol_air = co2_pa / (STANDARD_PRESSURE_MMHG * 133.322)
    
    # Convert to mass ratio
    co2_kg_per_kg_air = co2_mol_per_mol_air * (MOLAR_MASS_CO2 / MOLAR_MASS_AIR)
    
    return co2_kg_per_kg_air

def kg_per_kg_air_to_mmhg(co2_kg_per_kg_air: float) -> float:
    """
    Convert CO2 concentration from kg/kg air to mmHg.
    
    Args:
        co2_kg_per_kg_air: CO2 concentration in kg/kg air
        
    Returns:
        CO2 partial pressure in mmHg
    """
    # Convert mass ratio to molar ratio
    co2_mol_per_mol_air = co2_kg_per_kg_air * (MOLAR_MASS_AIR / MOLAR_MASS_CO2)
    
    # Convert to partial pressure in Pa
    co2_pa = co2_mol_per_mol_air * (STANDARD_PRESSURE_MMHG * 133.322)
    
    # Convert Pa to mmHg
    co2_mmhg = co2_pa / 133.322
    
    return co2_mmhg

def convert_co2_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert CO2 concentration between different units.
    
    Args:
        value: CO2 concentration value
        from_unit: Source unit ('mmHg', 'kg/kg_air', 'ppm', 'percent')
        to_unit: Target unit ('mmHg', 'kg/kg_air', 'ppm', 'percent')
        
    Returns:
        Converted CO2 concentration value
        
    Raises:
        ValueError: If unsupported units are provided
    """
    # First convert to kg/kg_air as intermediate unit
    if from_unit == 'mmHg':
        intermediate = mmhg_to_kg_per_kg_air(value)
    elif from_unit == 'kg/kg_air':
        intermediate = value
    elif from_unit == 'ppm':
        # ppm is parts per million by volume, convert to mass ratio
        intermediate = value * 1e-6 * (MOLAR_MASS_CO2 / MOLAR_MASS_AIR)
    elif from_unit == 'percent':
        # percent by volume, convert to mass ratio
        intermediate = value * 0.01 * (MOLAR_MASS_CO2 / MOLAR_MASS_AIR)
    else:
        raise ValueError(f"Unsupported source unit: {from_unit}")
    
    # Then convert from kg/kg_air to target unit
    if to_unit == 'mmHg':
        return kg_per_kg_air_to_mmhg(intermediate)
    elif to_unit == 'kg/kg_air':
        return intermediate
    elif to_unit == 'ppm':
        # Convert mass ratio to volume ratio (ppm)
        volume_ratio = intermediate * (MOLAR_MASS_AIR / MOLAR_MASS_CO2)
        return volume_ratio * 1e6
    elif to_unit == 'percent':
        # Convert mass ratio to volume ratio (percent)
        volume_ratio = intermediate * (MOLAR_MASS_AIR / MOLAR_MASS_CO2)
        return volume_ratio * 100
    else:
        raise ValueError(f"Unsupported target unit: {to_unit}")

class CDRAState:
    def __init__(self, baseline_co2: float):
        self.saturation = {k: 0.0 for k in ['desiccant_1', 'desiccant_3', 'sorbent_2', 'sorbent_4']}
        self.adsorption_eff = {k: BASE_ADSORPTION_EFF for k in ['desiccant_1', 'desiccant_3', 'sorbent_2', 'sorbent_4']}
        self.time = 0
        self.air_flow_rate = AIR_FLOW_RATE_NOMINAL
        self.co2_content = baseline_co2
        self.heater_on = {'desiccant_1': False, 'desiccant_3': False, 'sorbent_2': False, 'sorbent_4': False}
        self.valve_state = {'path_1_active': True}

# Failure config is passed in at runtime
# Keys supported:
# - filter_saturation: bool with start/end
# - valve_stuck: bool with start/end
# - heater_failure: List[str] of failed heaters
# - fan_degraded: bool with start/end and degraded_flow_rate


def _apply_failures(state: CDRAState, t: int, cfg: Dict) -> None:
    """Apply failures to the CDRA state with detailed debugging."""
    # if t % 100 == 0:  # Only print every 100 timesteps to reduce spam
        # print(f"[FAILURES] Time {t}: Applying failures from config: {cfg}")
    
    # Filter saturation window
    filt_on = bool(cfg.get('filter_saturation', False))
    fs_start = cfg.get('filter_saturation_start')
    fs_end = cfg.get('filter_saturation_end')
    if fs_start is not None and fs_end is not None:
        filt_on = fs_start <= t <= fs_end

    if filt_on and t % 50 == 0:
        # print(f"[FAILURES] APPLYING: Filter saturation at t={t}")
        for comp in state.saturation:
            state.saturation[comp] = 1.0
            state.adsorption_eff[comp] = BASE_ADSORPTION_EFF + MAX_ADSORPTION_EFF_INCREMENT * 1.0
    elif filt_on:
        # Apply the failure but don't print
        for comp in state.saturation:
            state.saturation[comp] = 1.0
            state.adsorption_eff[comp] = BASE_ADSORPTION_EFF + MAX_ADSORPTION_EFF_INCREMENT * 1.0

    # Valve stuck window
    stuck_on = bool(cfg.get('valve_stuck', False))
    vs_start = cfg.get('valve_stuck_start')
    vs_end = cfg.get('valve_stuck_end')
    if vs_start is not None and vs_end is not None:
        stuck_on = vs_start <= t <= vs_end
    
    # if stuck_on and t % 50 == 0:
    #     print(f"[FAILURES] APPLYING: Valve stuck at t={t}")

    # Heater failures
    heater_failures = cfg.get('heater_failure', []) or []
    # if heater_failures and t % 50 == 0:
    #     print(f"[FAILURES] APPLYING: Heater failures at t={t}: {heater_failures}")
    #     print(f"[FAILURES]   Heater states BEFORE: {state.heater_on}")
    for h in heater_failures:
        state.heater_on[h] = False
    # if heater_failures and t % 50 == 0:
    #     print(f"[FAILURES]   Heater states AFTER: {state.heater_on}")

    # Fan degraded window
    fan_on = bool(cfg.get('fan_degraded', False))
    fd_start = cfg.get('fan_degraded_start')
    fd_end = cfg.get('fan_degraded_end')
    if fd_start is not None and fd_end is not None:
        fan_on = fd_start <= t <= fd_end
    
    if fan_on:
        old_flow_rate = state.air_flow_rate
        state.air_flow_rate = cfg.get('degraded_flow_rate', AIR_FLOW_RATE_NOMINAL)
        # if t % 50 == 0:
        #     print(f"[FAILURES] APPLYING: Fan degraded at t={t} - flow rate {old_flow_rate:.3f} -> {state.air_flow_rate:.3f}")
    else:
        state.air_flow_rate = AIR_FLOW_RATE_NOMINAL


def _update_filter(state: CDRAState, component: str, dt: int) -> None:
    if state.heater_on[component]:
        state.saturation[component] = max(state.saturation[component] - (2.0 * dt) / SATURATION_TIME_CONSTANT, 0.0)
    else:
        state.saturation[component] = min(state.saturation[component] + dt / SATURATION_TIME_CONSTANT, 1.0)
    state.adsorption_eff[component] = BASE_ADSORPTION_EFF + MAX_ADSORPTION_EFF_INCREMENT * (1 - state.saturation[component])


def _timestep(state: CDRAState, dt: int) -> Tuple[float, float]:
    """Calculate one simulation timestep with detailed debugging."""
    # Update both paths
    _update_filter(state, 'desiccant_1', dt)
    _update_filter(state, 'sorbent_2', dt)
    _update_filter(state, 'desiccant_3', dt)
    _update_filter(state, 'sorbent_4', dt)

    # Choose path efficiency
    active_path = state.valve_state['path_1_active']
    if active_path:
        comp_used = 'sorbent_2'
        eta_co2 = state.adsorption_eff['sorbent_2'] if not state.heater_on['sorbent_2'] else -DESORPTION_MULTIPLIER
    else:
        comp_used = 'sorbent_4'
        eta_co2 = state.adsorption_eff['sorbent_4'] if not state.heater_on['sorbent_4'] else -DESORPTION_MULTIPLIER

    # if state.time % 200 == 0:  # Print every 200 timesteps to avoid spam
        # print(f"[TIMESTEP] Time {state.time}: Active path={active_path}, using {comp_used}")
        # print(f"[TIMESTEP]   {comp_used}: saturation={state.saturation[comp_used]:.3f}, eff={state.adsorption_eff[comp_used]:.4f}, heater={state.heater_on[comp_used]}")
        # print(f"[TIMESTEP]   CO2 efficiency (eta_co2): {eta_co2:.4f}")
        
        # Show all component states for debugging
        # print(f"[TIMESTEP]   All components:")
        # for comp in ['sorbent_2', 'sorbent_4']:
        #     heater_state = "ON" if state.heater_on[comp] else "OFF"
        #     print(f"[TIMESTEP]     {comp}: saturation={state.saturation[comp]:.3f}, eff={state.adsorption_eff[comp]:.4f}, heater={heater_state}")

    C_in = state.co2_content
    C_out = C_in * (1 - eta_co2) if eta_co2 >= 0 else C_in * eta_co2
    
    return C_out, state.air_flow_rate


def _update_cabin_concentration(state: CDRAState, C_out: float, flow: float) -> None:
    state.co2_content = ((1 - flow / M_CABIN) * state.co2_content + (flow / M_CABIN) * C_out + CO2_INPUT_MEAN / M_CABIN)


def _control(state: CDRAState, failure_config: Dict = None) -> None:
    """Control the CDRA system with failure awareness."""
    # Check if valve is stuck
    valve_stuck = False
    if failure_config:
        valve_stuck = bool(failure_config.get('valve_stuck', False))
        vs_start = failure_config.get('valve_stuck_start')
        vs_end = failure_config.get('valve_stuck_end')
        if vs_start is not None and vs_end is not None:
            valve_stuck = vs_start <= state.time <= vs_end
    
    if not valve_stuck and state.time % VALVE_SWITCH_INTERVAL == 0 and state.time != 0:
        state.valve_state['path_1_active'] = not state.valve_state['path_1_active']
        # if state.time % 200 == 0:  # Debug valve switching
        #     print(f"[CONTROL] Time {state.time}: Valve switched to path_1_active={state.valve_state['path_1_active']}")
    # elif valve_stuck and state.time % VALVE_SWITCH_INTERVAL == 0 and state.time != 0:
    #     if state.time % 200 == 0:  # Debug valve stuck
    #         print(f"[CONTROL] Time {state.time}: Valve switching PREVENTED (valve stuck)")
    
    # Get list of failed heaters from failure config
    failed_heaters = set()
    if failure_config:
        failed_heaters = set(failure_config.get('heater_failure', []))
    
    # Only set heater states for heaters that are not failed
    if 'desiccant_1' not in failed_heaters:
        state.heater_on['desiccant_1'] = not state.valve_state['path_1_active']
    if 'desiccant_3' not in failed_heaters:
        state.heater_on['desiccant_3'] = state.valve_state['path_1_active']
    if 'sorbent_2' not in failed_heaters:
        state.heater_on['sorbent_2'] = not state.valve_state['path_1_active']
    if 'sorbent_4' not in failed_heaters:
        state.heater_on['sorbent_4'] = state.valve_state['path_1_active']


def run_cdra_simulation(
    failure_config: Dict,
    duration_seconds: int,
    baseline_co2_mmHg: float,
    onset_time_sec: int = 3,
) -> List[float]:
    """Run CDRA simulation and return CO2 partial pressure time series in mmHg.
    duration_seconds: total sim time. Integration step is fixed at 1s.
    baseline_co2_mmHg: starting cabin CO2 concentration in mmHg.
    onset_time_sec: when to activate provided failure_config.
    """
    dt = 1
    steps = max(1, int(duration_seconds // dt))

    # Convert input from mmHg to kg/kg air for internal simulation
    baseline_co2_kg_per_kg = mmhg_to_kg_per_kg_air(baseline_co2_mmHg)
    
    state = CDRAState(baseline_co2=baseline_co2_kg_per_kg)
    series_kg_per_kg: List[float] = []

    
    # print(f"[CDRA_SIM] start: duration={duration_seconds}s, dt={dt}s, steps={steps}, baseline={baseline_co2_mmHg:.6f} mmHg ({baseline_co2_kg_per_kg:.6f} kg/kg), onset={onset_time_sec}")
    # print(f"[CDRA_SIM] failure_cfg: {failure_config}")

    for step in range(steps):
        # Activate failures after onset
        active_cfg = dict(failure_config)
        if state.time < onset_time_sec:
            # Disable windows before onset
            active_cfg['filter_saturation'] = False
            active_cfg['valve_stuck'] = False
            active_cfg['fan_degraded'] = False
            active_cfg['heater_failure'] = []  # Disable heater failures before onset
            # if state.time % 100 == 0:  # Print every 100 timesteps to avoid spam
            #     print(f"[SIM_LOOP] Time {state.time}: Pre-onset phase - all failures disabled")
        # else:
            # if state.time % 100 == 0:
                # print(f"[SIM_LOOP] Time {state.time}: Post-onset phase - applying failures")
        
        # Basic control (now with failure awareness)
        _control(state, active_cfg)
        _apply_failures(state, state.time, active_cfg)
        C_out, flow = _timestep(state, dt)
        _update_cabin_concentration(state, C_out, flow)
        series_kg_per_kg.append(state.co2_content)
        state.time += dt
        
        # if state.time % 200 == 0:  # Print every 200 timesteps
        #     co2_mmhg = kg_per_kg_air_to_mmhg(state.co2_content)
        #     print(f"[SIM_LOOP] Time {state.time}: CO2={state.co2_content:.6f} kg/kg ({co2_mmhg:.4f} mmHg), flow={flow:.3f}")

    # Convert output from kg/kg air back to mmHg
    series_mmhg = [kg_per_kg_air_to_mmhg(co2_kg_per_kg) for co2_kg_per_kg in series_kg_per_kg]

    try:
        print(f"[CDRA_SIM] done: produced={len(series_mmhg)} points, first_last={(series_mmhg[0] if series_mmhg else None, series_mmhg[-1] if series_mmhg else None)} mmHg")
    except Exception:
        pass
    return series_mmhg


def resample_series(values: List[float], target_len: int) -> List[float]:
    if target_len <= 0:
        return []
    if len(values) == target_len:
        return list(values)
    if len(values) == 0:
        return [0.0] * target_len
    # Linear resample
    result: List[float] = []
    for i in range(target_len):
        pos = i * (len(values) - 1) / (target_len - 1)
        lo = int(math.floor(pos))
        hi = min(lo + 1, len(values) - 1)
        frac = pos - lo
        v = values[lo] * (1 - frac) + values[hi] * frac
        result.append(v)
    return result


def anomaly_to_failure_config(anomaly_name: str, severity: float) -> Dict:
    """Map common CDRA anomaly names to failure config with debugging."""
    print(f"[ANOMALY_CFG] Converting anomaly '{anomaly_name}' with severity {severity:.3f}")
    
    # Map common CDRA anomaly names to failure config
    name = anomaly_name.lower()
    cfg: Dict = {
        'filter_saturation': False,
        'filter_saturation_start': 10**9,  # Default to never
        'filter_saturation_end': 10**9,
        'valve_stuck': False,
        'valve_stuck_start': 10**9,  # Default to never
        'valve_stuck_end': 10**9,
        'heater_failure': [],
        'fan_degraded': False,
        'fan_degraded_start': 10**9,  # Default to never
        'fan_degraded_end': 10**9,
        'degraded_flow_rate': max(0.1, AIR_FLOW_RATE_NOMINAL * (1 - 0.6 * severity)),
    }
    
    print(f"[ANOMALY_CFG] Checking name '{name}' against patterns...")
    
    # Base onset time (failures will activate after this)
    base_onset = 3  # seconds
    
    if 'saturat' in name or 'absorption bed' in name:
        cfg['filter_saturation'] = True
        # Severity affects how quickly saturation occurs after onset
        cfg['filter_saturation_start'] = base_onset + int(10 * (1 - severity))  # Higher severity = earlier onset after base
        print(f"[ANOMALY_CFG] MATCH: 'saturat' or 'absorption bed' -> filter_saturation=True, onset={cfg['filter_saturation_start']}")
    if 'valve' in name or 'leak' in name:
        cfg['valve_stuck'] = True
        # Severity affects when valve gets stuck after onset
        cfg['valve_stuck_start'] = base_onset + int(15 * (1 - severity))
        print(f"[ANOMALY_CFG] MATCH: 'valve' or 'leak' -> valve_stuck=True, onset={cfg['valve_stuck_start']}")
    if 'heater' in name:
        cfg['heater_failure'] = ['desiccant_1', 'sorbent_2']
        print(f"[ANOMALY_CFG] MATCH: 'heater' -> heater_failure={cfg['heater_failure']}")
    if 'fan' in name or 'bearing' in name:
        cfg['fan_degraded'] = True
        # Severity affects flow rate reduction after onset
        cfg['fan_degraded_start'] = base_onset + int(5 * (1 - severity))
        print(f"[ANOMALY_CFG] MATCH: 'fan' or 'bearing' -> fan_degraded=True, onset={cfg['fan_degraded_start']}, flow_rate={cfg['degraded_flow_rate']:.3f}")
    if 'sensor drift' in name or 'drift' in name:
        print(f"[ANOMALY_CFG] MATCH: 'sensor drift' or 'drift' -> handled in caller by post-process drift")
        # handled in caller by post-process drift
        pass
    
    print(f"[ANOMALY_CFG] Final config: {cfg}")
    print(f"[ANOMALY_CFG] ---")
    return cfg
