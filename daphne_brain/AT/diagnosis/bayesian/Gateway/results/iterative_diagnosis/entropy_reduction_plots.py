# entropy_reduction_plots.py
# Author: Joshua Elston
# Last Edited: 09/20/2026

# Visualize examples of entropy reduction resulting from collecting
# additional evidence via diagnostic actions

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from collections import defaultdict

records = []
with open("entropy_reduction_example.jsonl") as f:
    for line in f:
        line = line.strip()
        if line: # skip blank lines between scenarios
            records.append(json.loads(line))

# Group and sort by scenario
scenarios = defaultdict(list)
for r in records:
    scenarios[r["scenario_id"]].append(r)
for sid in scenarios:
    scenarios[sid].sort(key=lambda x: x["timestamp"])

# Scenario display name mapping
scenario_labels = {
    "decompression.biosim": "Module Decompression (IHab)",
    "oga_ihab.biosim": "OGA Failure",
}

# Compute entropy threshold for 90% confidence
# Assuming that the top anomaly must have a probability of at least 0.90,
# assume the most conservative entropy case where remaining 0.10 shared
# evenly amongst remaining anomalies (8 total anomalies in Gateway network,
# so 7-way split)
p_top = 0.90
p_rest = (1 - p_top) / 7 # per remaining class
H_threshold = -(p_top*np.log(p_top) + 7 *p_rest*np.log(p_rest))
print(f"Entropy threshold (90% confidence): {H_threshold:.4f} nats")

# Plot entropy reduction through collection of additional evidence
colors = {"decompression.biosim": "#1E88E5", "oga_ihab.biosim": "#D81B60"}
markers = {"decompression.biosim": "o", "oga_ihab.biosim": "s"}

fig, ax = plt.subplots(figsize=(10, 5))

for sid, runs in scenarios.items():
    steps = range(0, len(runs))
    entropy = [r["initial_entropy"] for r in runs]
    label   = scenario_labels.get(sid, sid)
    color = colors[sid]

    ax.plot(steps, entropy, marker=markers[sid], color=color,
            linewidth=2.5, markersize=10, label=label, zorder=3)

    # Annotate only steps that have NOT yet crossed the threshold
    for i, r in enumerate(runs):
        is_last_step = (i == len(runs) - 1)
        if entropy[i] > H_threshold and not is_last_step:
            evidence = r["best_evidence"].replace("[HIDDEN] ", "")
            
            # If annotation lands on the last step, flip offset to the left
            is_last_annotation = (i + 1 == len(runs) - 1)
            x_offset  =  -40 if is_last_annotation else 10
            y_offset = 2 if is_last_annotation else 8
            alignment = "right" if is_last_annotation else "left"

            ax.annotate(
                f"+ {evidence}",
                xy=(i + 1, entropy[i + 1]),
                xytext=(x_offset, y_offset),
                textcoords="offset points",
                fontsize=12,
                color=color,
                ha=alignment, # align text anchor accordingly
                arrowprops=dict(arrowstyle="-", color=color, alpha=0.5),
            )

# Add threshold line
ax.axhline(H_threshold, color="black", linestyle="--", linewidth=1.8, zorder=2),
# Add text just inside right x limit above the line
ax.text(2.01, H_threshold + 0.005, f"90% confidence threshold", #\n({H_threshold:.3f} nats)",
    ha="right", va="bottom", fontsize=11, color="black")

# Shade the region below the threshold (the "certain" region)
ax.axhspan(0, H_threshold, alpha=0.05, color="green")

ax.set_xlabel("Diagnostic Step", fontsize=14)
ax.set_ylabel("Entropy (nats)", fontsize=14)
ax.set_title("Entropy Reduction Through Iterative Diagnosis", fontsize=18, fontweight="bold")
ax.tick_params(axis="both", labelsize=12)
ax.set_xticks([0, 1, 2])
ax.set_xlim(-0.015, 2.015)
ax.set_ylim(0, 1)
ax.legend(fontsize=12)
# ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("entropy_reduction.png", dpi=150)
plt.show()


## Entropy evolution stacked bar chart
col_rename = {
    "Module Decompression (HALO)": "Module Decompression\n(HALO)",
    "Module Decompression (IHab)": "Module Decompression\n(IHab)",
    "O2 Delivery System Malfunction (HALO)": "O\u2082 Delivery\nMalfunction (HALO)",
    "O2 Delivery System Malfunction (IHab)": "O\u2082 Delivery\nMalfunction (IHab)",
    "OGA Failure": "OGA Failure",
    "VCCR Sorbent Bed Saturation": "VCCR Sorbent\nBed Saturation",
    "VCCR Particulate Filter Saturation": "VCCR Particulate\nFilter Saturation",
    "Unknown Anomaly": "Unknown Anomaly",
}

# Color per anomaly class
class_colors = {
    "Module Decompression\n(HALO)": "#332288",
    "Module Decompression\n(IHab)": "#1E88E5",
    "OGA Failure": "#D81B60",
    "O\u2082 Delivery\nMalfunction (HALO)": "#DDCC77",
    "O\u2082 Delivery\nMalfunction (IHab)": "#44AA99",
    "VCCR Sorbent\nBed Saturation": "#117733",
    "VCCR Particulate\nFilter Saturation": "#AA4499",
    "Unknown Anomaly": "#882255",
}

fig, axes = plt.subplots(1, len(scenarios), figsize=(14, 5.5), sharey=True, layout="constrained")

for ax, (sid, runs) in zip(axes, scenarios.items()):
    runs = sorted(runs, key=lambda x: x["timestamp"])
    n_steps = len(runs)
    step_labels = []
    for i, r in enumerate(runs):
        if i == 0:
            label = f"Initial Diagnosis"
        else:
            # Show evidence collected to reach this step
            prev_evidence = runs[i - 1]["best_evidence"].replace("[HIDDEN] ", "").replace("Pressure","\nPressure").replace("Panel", "\nPanel")
            label = f"Assess {prev_evidence}"
        step_labels.append(label)

    # Build matrix: rows = anomaly classes, cols = steps
    all_classes = list(col_rename.values())
    prob_matrix = np.zeros((len(all_classes), n_steps))

    for j, r in enumerate(runs):
        for orig, short in col_rename.items():
            prob_matrix[all_classes.index(short), j] = r["probabilities"].get(orig, 0.0)

    # Stacked bar, each bar sorted independently (largest segment at the bottom)
    x = np.arange(n_steps)

    for j in range(n_steps):
        col = prob_matrix[:, j]
        order = np.argsort(-col, kind="stable")   # indices of classes, largest first
        bottom = 0.0

        for k in order:
            v = col[k]
            if v <= 0:
                continue  # skip classes with no probability at this step
            cls = all_classes[k]

            ax.bar(x[j], v, bottom=bottom,
                color=class_colors.get(cls, "#bdc3c7"),
                edgecolor="white", width=0.5)

            # Label bar segments > 5%
            if v > 5:
                ax.text(x[j], bottom + v / 2, f"{v:.1f}%",
                        ha="center", va="center",
                        fontsize=12, color="white", fontweight="bold")
            bottom += v

    ax.set_title(scenario_labels.get(sid, sid), fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(step_labels, fontsize=12)
    ax.set_ylim(0, 100)

axes[0].set_ylabel("Posterior Probability (%)", fontsize=14)

# Shared legend
handles = [mpatches.Patch(color=class_colors[c], label=c.replace("\n", " "))
           for c in all_classes if c in class_colors]

fig.suptitle("Probability Distribution Following Diagnostic Actions",
             fontsize=18, fontweight="bold")

fig.legend(handles=handles, loc="outside lower center", ncol=4, fontsize=11,
           frameon=False)

# Tighten the padding (inches). Defaults are about 0.04; lower = tighter.
fig.get_layout_engine().set(h_pad=0.04, w_pad=0.075)

plt.savefig("probability_evolution.png", dpi=150, bbox_inches="tight", pad_inches=0.1)
plt.show()


## Probability Heatmap Over Iterative Diagnosis
step_counts = [len(runs) for runs in scenarios.values()]
fig, axes = plt.subplots(1, len(scenarios), figsize=(14, 6),
                         gridspec_kw={"width_ratios": step_counts})

for ax, (sid, runs) in zip(axes, scenarios.items()):
    runs = sorted(runs, key=lambda x: x["timestamp"])

    # Build matrix
    all_classes = list(col_rename.values())
    n_steps = len(runs)
    data = np.zeros((len(all_classes), n_steps))

    for j, r in enumerate(runs):
        for orig, short in col_rename.items():
            data[all_classes.index(short), j] = r["probabilities"].get(orig, 0.0)

    # Filter BEFORE passing to imshow
    nonzero_mask = data.sum(axis=1) > 0
    plot_data    = data[nonzero_mask]
    plot_classes = [c for c, keep in zip(all_classes, nonzero_mask) if keep]
    n_rows       = len(plot_classes)

    im = ax.imshow(plot_data, cmap="cividis", aspect="auto", vmin=0, vmax=100)

    step_labels = []
    for i, r in enumerate(runs):
        if i == 0:
            label = "Initial Diagnosis"
        else:
            prev_evidence = runs[i - 1]["best_evidence"].replace("[HIDDEN] ", "").replace("Pressure","\nPressure").replace("Panel", "\nPanel")
            label = f"Assess {prev_evidence}"
        step_labels.append(label)

    # For relevant anomalies, change y-tick text from the col_rename value
    ytick_overrides = {
        "Module Decompression\n(HALO)": "Module\nDecompression\n(HALO)",
        "Module Decompression\n(IHab)": "Module\nDecompression\n(IHab)",
        "O\u2082 Delivery\nMalfunction (HALO)": "O\u2082 Delivery\nMalfunction\n(HALO)",
        "O\u2082 Delivery\nMalfunction (IHab)": "O\u2082 Delivery\nMalfunction\n(IHab)"
    }

    def ytick_label(c):
        return ytick_overrides.get(c, c)

    ax.set_xticks(np.arange(n_steps))
    ax.set_yticks(np.arange(n_rows))
    ax.set_xticklabels(step_labels, fontsize=12)
    ax.set_yticklabels([ytick_label(c) for c in plot_classes], fontsize=12)

    # cividis is dark at low values, light at high values
    for i in range(len(plot_classes)):
        for j in range(n_steps):
            val = plot_data[i, j]
            text_color = "white" if val < 50 else "black"  # reversed from before
            ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                    fontsize=12, color=text_color,
                    fontweight = "bold" if text_color == "black" else "normal")

    # Minor grid
    ax.set_xticks(np.arange(n_steps + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(plot_classes)+1)-0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)

    ax.set_title(scenario_labels.get(sid, sid), fontsize=14, fontweight="bold")

    cbar = plt.colorbar(im, ax=ax, fraction=0.04, pad=0.03)
    cbar.set_label("Posterior Probability (%)", fontsize=12)
    cbar.ax.tick_params(labelsize=12)

fig.suptitle("Posterior Probability Distribution Following Diagnostic Actions", fontsize=18, fontweight="bold")
plt.tight_layout()
plt.savefig("iterative_heatmap.png", dpi=150)
plt.show()