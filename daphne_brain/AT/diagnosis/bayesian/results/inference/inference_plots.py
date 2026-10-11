import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import seaborn as sns
import pandas as pd

# Load data from results files
def load_runtimes(filepath):
    records = []
    with open(filepath) as f:
        for line in f:
            records.append(json.loads(line))
    return [r["initial_inference_runtime"] for r in records]

reduced_runtime  = load_runtimes("reduced_results.jsonl")
default_runtime  = load_runtimes("default_results.jsonl")
expanded_runtime = load_runtimes("expanded_results.jsonl")

re_median = np.median(reduced_runtime)
de_median = np.median(default_runtime)
ex_median = np.median(expanded_runtime)
print(f"Median Runtimes:\nReduced: {re_median}s\nBaseline: {de_median}s\nExpanded: {ex_median}s\n")

# Summary statistics
labels = ["Reduced", "Baseline", "Expanded"]
data   = [reduced_runtime, default_runtime, expanded_runtime]
colors = ["#CC6677", "#88CCEE", "#DDCC77"]

# Restructure into long-format DataFrame, respecting label order
df = pd.DataFrame({
    "Runtime": default_runtime + expanded_runtime + reduced_runtime,
    "Configuration": (["Baseline"] * len(default_runtime) +
                      ["Expanded"] * len(expanded_runtime) +
                      ["Reduced"] * len(reduced_runtime))
})

# Create plot
fig, ax = plt.subplots(figsize=(10, 7))

# Create violin plot (using seaborn library)
sns.violinplot(
    data=df,
    x="Configuration",
    y="Runtime",
    order=labels, # enforce label order
    palette=dict(zip(labels, colors)), # per-violin coloring
    inner="box",
    inner_kws=dict(box_width=6, whis_width=2, color="grey", zorder=5),
    alpha=0.4,
    ax=ax
)

# After plotting, update each violin's edge color to match its fill color
for violin, color in zip(ax.collections, colors):
    r, g, b, _ = mcolors.to_rgba(color) # extract RGB from hex color
    violin.set_edgecolor((r, g, b, 0.6)) # set edge color with custom alpha (0.0-1.0)

# Overlay individual data points (jittered)
for i, (d, color) in enumerate(zip(data, colors)):
    x = np.random.normal(i, 0.04, size=len(d))
    ax.scatter(x, d, alpha=0.5, s=45, color=color, edgecolor="white", linewidth=0.5, zorder=3)

# Formatting
ax.set_xlabel("")
ax.set_ylabel("Initial Inference Runtime (s)", fontsize=20)
ax.set_title(
    "Distribution of Initial Inference Runtimes by Model Size",
    fontsize=20, fontweight="bold"
)
ax.tick_params(axis="both", labelsize=20)

plt.tight_layout()
plt.savefig("inference_runtime_violin_comparison.png", dpi=150)
plt.show()


## Best Diagnostic Action Calculation Runtime Distribution
# Load data
records = []
with open("default_results.jsonl") as f:
    for line in f:
        records.append(json.loads(line))

initial_best_evidence_runtime = [r["initial_best_evidence_runtime"] for r in records]

fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(
    initial_best_evidence_runtime,
    bins=7,
    color="#88CCEE",
    edgecolor="black",
    alpha=0.85
)

# Median
median_best_evidence_runtime = np.median(initial_best_evidence_runtime)

# ax.axvline(
#     median_best_evidence_runtime,
#     linestyle="--",
#     linewidth=2,
#     color="black",
#     alpha=0.6,
#     label=f"Median = {median_best_evidence_runtime:.3f} s"
# )

# Formatting
ax.set_xlabel("Time to Suggest Optimal Diagnostic Action (s)", fontsize=20)
ax.set_ylabel("Count", fontsize=20)
ax.set_xlim([62, 78])
ax.set_title(
    "Runtime Distribution to Compute Optimal Diagnostic Action (Baseline Model)",
    fontsize=20,
    fontweight="bold"
)

ax.tick_params(axis="both", labelsize=20)

plt.tight_layout()
plt.savefig("best_evidence_runtime_histogram.png", dpi=150)
plt.show()