# run_logger.py
# Author: Joshua Elston
# Last Edited: 06/07/2026

# Script appends per-run scenario data in a single .json file to compute
# the entropy and hits@1 (reflecting confidence and accuracy, respectively)
# of the Bayesian Network

import json
import os
import math
from datetime import datetime, timezone
from pathlib import Path
_SCRIPT_DIR = Path(__file__).resolve().parent
_DEFAULT_RESULTS_DIR = _SCRIPT_DIR / 'results'

def _hits_at_k(probabilities: dict[str, float], true_anomaly: str, k: int = 1) -> int:
    # Return 1 if the true anomaly is in the top-k ranked anomalies, else return 0
    if true_anomaly is None:
        return None
    ranked = sorted(probabilities.keys(), key=lambda k: probabilities[k], reverse=True)
    return int(true_anomaly in ranked[:k])

# Main API
def log_run(
        probabilities: dict[str, float],
        scenario_id: str=None,
        true_anomaly: str=None,
        initial_entropy: float=None,
        best_evidence: str=None,
        telemetry_snapshot: dict=None,
        results_dir: Path=_DEFAULT_RESULTS_DIR,
        filename: str='run_results.jsonl',
) -> dict:
    
    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)
    filepath = results_path / filename

    # Derived accuracy metrics
    top1 = _hits_at_k(probabilities, true_anomaly, k=1)
    top3 = _hits_at_k(probabilities, true_anomaly, k=3)
    ranked_anomalies = sorted(probabilities.keys(), key=lambda k: probabilities[k], reverse=True)

    record = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'scenario_id': scenario_id,
        'true_anomaly': true_anomaly,
        'initial_entropy': initial_entropy,
        'hits@1': top1,
        'hits@3': top3,
        'top_predicted_anomaly': ranked_anomalies[0] if ranked_anomalies else None,
        'probabilities': probabilities,
        'best_evidence': best_evidence,
        'telemetry_snapshot': telemetry_snapshot
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