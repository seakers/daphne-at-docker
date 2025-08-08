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
    # Filter saturation window
    filt_on = bool(cfg.get('filter_saturation', False))
    fs_start = cfg.get('filter_saturation_start')
    fs_end = cfg.get('filter_saturation_end')
    if fs_start is not None and fs_end is not None:
        filt_on = fs_start <= t <= fs_end

    if filt_on:
        for comp in state.saturation:
            state.saturation[comp] = 1.0
            state.adsorption_eff[comp] = BASE_ADSORPTION_EFF + MAX_ADSORPTION_EFF_INCREMENT * 1.0

    # Valve stuck window
    stuck_on = bool(cfg.get('valve_stuck', False))
    vs_start = cfg.get('valve_stuck_start')
    vs_end = cfg.get('valve_stuck_end')
    if vs_start is not None and vs_end is not None:
        stuck_on = vs_start <= t <= vs_end
    if stuck_on:
        state.valve_state['path_1_active'] = state.valve_state['path_1_active']

    # Heater failures
    for h in cfg.get('heater_failure', []) or []:
        state.heater_on[h] = False

    # Fan degraded window
    fan_on = bool(cfg.get('fan_degraded', False))
    fd_start = cfg.get('fan_degraded_start')
    fd_end = cfg.get('fan_degraded_end')
    if fd_start is not None and fd_end is not None:
        fan_on = fd_start <= t <= fd_end
    state.air_flow_rate = cfg.get('degraded_flow_rate', AIR_FLOW_RATE_NOMINAL) if fan_on else AIR_FLOW_RATE_NOMINAL


def _update_filter(state: CDRAState, component: str, dt: int) -> None:
    if state.heater_on[component]:
        state.saturation[component] = max(state.saturation[component] - (2.0 * dt) / SATURATION_TIME_CONSTANT, 0.0)
    else:
        state.saturation[component] = min(state.saturation[component] + dt / SATURATION_TIME_CONSTANT, 1.0)
    state.adsorption_eff[component] = BASE_ADSORPTION_EFF + MAX_ADSORPTION_EFF_INCREMENT * (1 - state.saturation[component])


def _timestep(state: CDRAState, dt: int) -> Tuple[float, float]:
    # Update both paths
    _update_filter(state, 'desiccant_1', dt)
    _update_filter(state, 'sorbent_2', dt)
    _update_filter(state, 'desiccant_3', dt)
    _update_filter(state, 'sorbent_4', dt)

    # Choose path efficiency
    if state.valve_state['path_1_active']:
        eta_co2 = state.adsorption_eff['sorbent_2'] if not state.heater_on['sorbent_2'] else -DESORPTION_MULTIPLIER
    else:
        eta_co2 = state.adsorption_eff['sorbent_4'] if not state.heater_on['sorbent_4'] else -DESORPTION_MULTIPLIER

    C_in = state.co2_content
    C_out = C_in * (1 - eta_co2) if eta_co2 >= 0 else C_in * eta_co2
    return C_out, state.air_flow_rate


def _update_cabin_concentration(state: CDRAState, C_out: float, flow: float) -> None:
    state.co2_content = ((1 - flow / M_CABIN) * state.co2_content + (flow / M_CABIN) * C_out + CO2_INPUT_MEAN / M_CABIN)


def _control(state: CDRAState) -> None:
    if state.time % VALVE_SWITCH_INTERVAL == 0 and state.time != 0:
        state.valve_state['path_1_active'] = not state.valve_state['path_1_active']
    state.heater_on['desiccant_1'] = not state.valve_state['path_1_active']
    state.heater_on['desiccant_3'] = state.valve_state['path_1_active']
    state.heater_on['sorbent_2'] = not state.valve_state['path_1_active']
    state.heater_on['sorbent_4'] = state.valve_state['path_1_active']


def run_cdra_simulation(
    failure_config: Dict,
    duration_seconds: int,
    baseline_co2_mass_ratio: float,
    onset_time_sec: int = 3,
    seed: Optional[int] = None,
) -> List[float]:
    """Run CDRA simulation and return CO2 mass ratio time series.
    duration_seconds: total sim time. Integration step is fixed at 1s.
    baseline_co2_mass_ratio: starting cabin CO2 concentration (kg/kg dry air).
    onset_time_sec: when to activate provided failure_config.
    """
    if seed is not None:
        random.seed(seed)
    dt = 1
    steps = max(1, int(duration_seconds // dt))

    state = CDRAState(baseline_co2=baseline_co2_mass_ratio)
    series: List[float] = []

    try:
        print(f"[CDRA_SIM] start: duration={duration_seconds}s, dt={dt}s, steps={steps}, baseline={baseline_co2_mass_ratio:.6f}, onset={onset_time_sec}")
        print(f"[CDRA_SIM] failure_cfg: {failure_config}")
    except Exception:
        pass

    for step in range(steps):
        # Basic control
        _control(state)
        # Activate failures after onset
        active_cfg = dict(failure_config)
        if state.time < onset_time_sec:
            # Disable windows before onset
            active_cfg['filter_saturation'] = False
            active_cfg['valve_stuck'] = False
            active_cfg['fan_degraded'] = False
            active_cfg['heater_failure'] = []
        _apply_failures(state, state.time, active_cfg)
        C_out, flow = _timestep(state, dt)
        _update_cabin_concentration(state, C_out, flow)
        series.append(state.co2_content)
        state.time += dt

    try:
        print(f"[CDRA_SIM] done: produced={len(series)} points, first_last={(series[0] if series else None, series[-1] if series else None)}")
    except Exception:
        pass
    return series


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


def scale_to_actual_units(sim_series: List[float], actual_values: List[float]) -> List[float]:
    if not sim_series or not actual_values:
        return sim_series
    try:
        actual_avg = sum(float(v) for v in actual_values) / len(actual_values)
        sim_avg = sum(float(v) for v in sim_series) / len(sim_series)
        if sim_avg == 0:
            return sim_series
        scale = actual_avg / sim_avg
        return [v * scale for v in sim_series]
    except Exception:
        return sim_series


def anomaly_to_failure_config(anomaly_name: str, severity: float) -> Dict:
    # Map common CDRA anomaly names to failure config
    name = anomaly_name.lower()
    cfg: Dict = {
        'filter_saturation': False,
        'filter_saturation_start': 0,
        'filter_saturation_end': 10**9,
        'valve_stuck': False,
        'valve_stuck_start': 0,
        'valve_stuck_end': 10**9,
        'heater_failure': [],
        'fan_degraded': False,
        'fan_degraded_start': 0,
        'fan_degraded_end': 10**9,
        'degraded_flow_rate': max(0.1, AIR_FLOW_RATE_NOMINAL * (1 - 0.6 * severity)),
    }
    if 'saturat' in name or 'absorption bed' in name:
        cfg['filter_saturation'] = True
    if 'valve' in name or 'leak' in name:
        cfg['valve_stuck'] = True
    if 'heater' in name:
        cfg['heater_failure'] = ['desiccant_1', 'sorbent_2']
    if 'fan' in name or 'bearing' in name:
        cfg['fan_degraded'] = True
    if 'sensor drift' in name or 'drift' in name:
        # handled in caller by post-process drift
        pass
    return cfg
