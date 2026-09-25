import json
import matplotlib.pyplot as plt
import numpy as np

## Inference Runtime Distribution
# Load data
records = []
with open("expanded_hera_results.jsonl") as f:
    for line in f:
        records.append(json.loads(line))

scenarios   = [r["scenario_id"] for r in records]
entropy     = [r["initial_entropy"] for r in records]
hits1       = [r["hits@1"] for r in records]
runtime     = [r["inference_runtime"] for r in records]

# Sort by entropy descending
order = np.argsort(entropy)[::-1]
scenarios_s = [scenarios[i] for i in order]
entropy_s   = [entropy[i]   for i in order]
hits1_s     = [hits1[i]     for i in order]
runtime_s = [runtime[i] for i in order]

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(runtime, bins=20, color="#1E88E5", edgecolor="white", alpha=0.85)

# Mean and median
mean_runtime = np.mean(runtime)
median_runtime = np.median(runtime)

# ax.axvline(mean_runtime, linestyle="--", linewidth=2, color="black",
#            label=f"Mean = {mean_runtime:.3f} s")
ax.axvline(median_runtime, linestyle="--", linewidth=2, color="black",
           label=f"Median = {median_runtime:.3f} s")

ax.set_xlabel("Inference Runtime (s)", fontsize=20)
ax.set_ylabel("Count", fontsize=20)
ax.set_xlim(1.3, 2.7)
ax.set_ylim(0,10)
ax.set_title("Distribution of Initial Inference Runtimes for Expanded HERA Model", fontsize=20, fontweight="bold")
ax.tick_params(axis="both", labelsize=20)

ax.legend(fontsize=20)

plt.tight_layout()
plt.savefig("inference_runtime_distribution.png", dpi=150)
plt.show()