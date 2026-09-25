# run_logger.py
# Author: Joshua Elston
# Last Edited: 09/25/2026

# Script appends per-run scenario data in a single .json file to compute
# the entropy and hits@1 (reflecting confidence and accuracy, respectively)
# of the Bayesian Network

import json
from typing import Union
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_DEFAULT_RESULTS_DIR = _SCRIPT_DIR / 'results'

def _hits_at_k(probabilities: dict[str, float], true_anomaly: str, k: int = 1) -> int:
    # Return 1 if the true anomaly is in the top-k ranked anomalies, else return 0
    if true_anomaly is None:
        return None
    # Normalize to a list so check is always the same
    # candidates = true_anomaly

    ranked = sorted(probabilities.keys(), key=lambda k: probabilities[k], reverse=True)
    return int(true_anomaly in ranked[:k])

# Main API
def log_run(
        probabilities: dict[str, float],
        scenario_id: str=None,
        true_anomaly: str=None,
        initial_entropy: float=None,
        updated_entropy: float=None,
        initial_top_anomaly: str=None,
        updated_top_anomaly: str=None,
        initial_best_evidence: str=None,
        updated_best_evidence: str=None,
        initial_best_evidence_runtime: float=None,
        updated_best_evidence_runtime: float=None,
        initial_hits1: int=None,
        updated_hits1: int=None,
        initial_hits3: int=None,
        updated_hits3: int=None,
        initial_inference_runtime: float=None,
        updated_inference_runtime: float=None,
        telemetry_snapshot: dict=None,
        is_followup: bool =False,
        results_dir: Path=_DEFAULT_RESULTS_DIR,
        filename: str='run_results.jsonl',
) -> dict:
    
    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)
    filepath = results_path / filename

    record = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'scenario_id': scenario_id,
        'true_anomaly': true_anomaly,
        'inference_type': 'follow_up' if is_followup else 'initial',
        'initial_entropy': initial_entropy,
        'updated_entropy': updated_entropy,
        'delta_entropy': (round(initial_entropy-updated_entropy, 4)
                         if initial_entropy is not None and updated_entropy is not None
                         else None),
        'initial_top_anomaly': initial_top_anomaly,
        'updated_top_anomaly': updated_top_anomaly,
        'initial_hits@1': initial_hits1,
        'initial_hits@3': initial_hits3,
        'updated_hits@1': updated_hits1,
        'updated_hits@3': updated_hits3,
        'initial_best_evidence': initial_best_evidence,
        'updated_best_evidence': updated_best_evidence,
        'initial_best_evidence_runtime': initial_best_evidence_runtime,
        'updated_best_evidence_runtime': updated_best_evidence_runtime,
        'initial_inference_runtime': initial_inference_runtime,
        'updated_inference_runtime': updated_inference_runtime,
        'probabilities': (
            {k: round(v * 100, 2) for k, v in probabilities.items()}
            if probabilities else None
        ),
        'telemetry_snapshot': (
            {k: round(v, 2) if isinstance(v, float) else v
             for k, v in telemetry_snapshot.items()}
            if telemetry_snapshot else None
        )
    }

    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record) + '\n')

    print(f'[run_logger] Run logged -> {filepath} (scenario: {scenario_id}')
    return record

# Analysis helpers
def load_all_runs(
        results_dir: Path=_DEFAULT_RESULTS_DIR,
        filename: str='run_results.jsonl',
) -> list[dict]:
    
    # Load every previously logged run as a list of dicts
    filepath = Path(results_dir) / filename
    if not filepath.exists():
        print(f'[run_logger] No results file found at {filepath}')
        return []
    with open(filepath, encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]
    
def compute_aggregate_metrics(
    results_dir: Path=_DEFAULT_RESULTS_DIR,
    filename: str='run_results.jsonl',
) -> dict:
    # Compute aggregate metrics over all logged runs
    # Specifically, hits@1, hits@3, mean entropy values,
    # and per-anomlay breakdowns are stored in a dict
    runs = load_all_runs(results_dir, filename)
    if not runs:
        return {}
    
    evaluated = [r for r in runs if r.get('hits@1') is not None]
    n_total = len(runs)
    n_eval = len(evaluated)

    hits1 = [r['hits@1'] for r in evaluated]
    hits3 = [r['hits@3'] for r in evaluated]
    initial_entropies = [r['initial_entropy'] for r in runs if r.get('initial_entropy') is not None]
    
    # Per-anomaly hits@k
    per_anomaly: dict[str, dict] = {}
    for r in evaluated:
        ta = r['true_anomaly']
        per_anomaly.setdefault (ta, {'runs': 0, 'hits@1': 0, 'hits@3': 0})
        per_anomaly[ta]['runs'] += 1
        per_anomaly[ta]['hits@1'] += r['hits@1']
        per_anomaly[ta]['hits@3'] += r['hits@3']

    for ta, stats in per_anomaly.items():
        n = stats['runs']
        stats['hits@1_rate'] = round(stats['hits@1']/n, 4)
        stats['hits@3_rate'] = round(stats['hits@3']/n, 4)

    summary ={
        'total_runs': n_total,
        'evaluated_runs': n_eval,
        'hits@1': sum(hits1),
        'hits@1_rate': round(sum(hits1) / n_eval, 4) if n_eval else None,
        'hits@3': sum(hits3),
        'hits@3_rate': round(sum(hits3) / n_eval, 4) if n_eval else None,
        'mean_initial_entropy': round(sum(initial_entropies) / len(initial_entropies), 6) if initial_entropies else None,
        'per_anomaly': per_anomaly,
    }
    return summary