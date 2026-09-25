import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

## Initial Diagnosis Entropy per Injected Fault Scenario
# Load data
records = []
with open("run_results.jsonl") as f:
    for line in f:
        records.append(json.loads(line))

scenarios   = [r["scenario_id"] for r in records]
entropy     = [r["initial_entropy"] for r in records]
is_or       = [r["true_anomaly_or"] for r in records]
hits1       = [r["hits@1"] for r in records]
runtime     = [r["inference_runtime"] for r in records]

# Sort by entropy descending
order = np.argsort(entropy)[::-1]
scenarios_s = [scenarios[i] for i in order]
entropy_s   = [entropy[i]   for i in order]
is_or_s     = [is_or[i]     for i in order]
hits1_s     = [hits1[i]     for i in order]
runtime_s = [runtime[i] for i in order]

# Color logic
colors = []
for i in range(len(scenarios_s)):
    if hits1_s[i] == 0: # hits@1 miss
        colors.append("red")
    elif is_or_s[i]: # OR/ambiguous anomaly
        colors.append("orange")
    else: # correct prediction
        colors.append("green")

# fig, ax = plt.subplots(figsize=(12, 6))
# bars = ax.barh(scenarios_s, entropy_s, color=colors, edgecolor="white", height=0.6)

# # Annotate values
# for bar, val in zip(bars, entropy_s):
#     if val > 0.9:
#         # Place inside the bar, right-aligned, white text
#         ax.text(val - 0.0025, bar.get_y() + bar.get_height() / 2,
#                 f"{val:.4f}", va="center", ha="right",
#                 fontsize=10, color="black")
#     else:
#         # Place outside the bar as before
#         ax.text(val + 0.0025, bar.get_y() + bar.get_height() / 2,
#                 f"{val:.4f}", va="center", ha="left",
#                 fontsize=10, color="black")

# ax.set_xlabel("Entropy (nats)", fontsize=12)
# ax.set_title("Initial Diagnosis Entropy by Injected Fault Scenario", fontsize=18, fontweight="bold")
# ax.tick_params(axis="both", labelsize=10)
# ax.set_xlim(0, 1)
# ax.margins(y=0.01)

# legend_handles = [
#     mpatches.Patch(color="green", label="Correct Diagnosis (hits@1 = 1)"),
#     mpatches.Patch(color="orange", label="Ambiguous/OR anomaly"),
#     mpatches.Patch(color="red", label="Incorrect Diagnosis (hits@1 = 0)"),
# ]
# ax.legend(handles=legend_handles, loc="upper right")
# plt.tight_layout()
# plt.savefig("entropy_by_scenario.png", dpi=150)
# plt.show()


# ## Posterior Probability Heatmap
# scenarios = [r["scenario_id"].replace(".biosim", "") for r in records]
# entropy   = [r["initial_entropy"] for r in records]

# # Sort by entropy descending (consistent with other plots)
# order = np.argsort(scenarios)   # alphabetical by scenario name
# scenarios_s = [scenarios[i] for i in order]
# records_s   = [records[i]   for i in order]

# prob_rows = {}

# for r in records_s:
#     name = r["scenario_id"].replace(".biosim", "")
#     prob_rows[name] = r["probabilities"]

# df_prob = pd.DataFrame(prob_rows).T.fillna(0.0)

# # Keep anomaly columns in the order they appear in the data
# col_order = list(df_prob.columns)
# df_prob = df_prob[col_order]

# data = df_prob.values # shape: (n_scenarios, n_classes)
# n_rows, n_cols = data.shape

# # Plot results
# fig, ax = plt.subplots(figsize=(13, 8))

# im = ax.imshow(data, cmap="cividis", aspect="auto", vmin=0, vmax=100)

# # Colorbar
# cbar = plt.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
# cbar.set_label("Posterior Probability (%)", fontsize=12)
# cbar.ax.tick_params(labelsize=12)

# x_labels = [
#     c.replace("Decompression\n", "\nDecompression\n")
#      .replace("Malfunction\n", "\nMalfunction ")
#     for c in df_prob.columns
# ]

# # Axis labels
# ax.set_xticks(np.arange(n_cols))
# ax.set_yticks(np.arange(n_rows))
# ax.set_xticklabels(x_labels, fontsize=12, ha="center", va="top", multialignment="center")
# ax.set_yticklabels(df_prob.index, fontsize=12)

# # Annotate each cell with value
# # cividis is dark at low values, light at high values
# for i in range(n_rows):
#     for j in range(n_cols):
#         val = data[i, j]
#         text_color = "white" if val < 50 else "black" # reversed from before
#         ax.text(j, i, f"{val:.1f}", ha="center", va="center",
#                 fontsize=12, color=text_color,
#                 fontweight = "bold" if text_color == "black" else "normal")

# # Grid lines between cells
# ax.set_xticks(np.arange(n_cols + 1) - 0.5, minor=True)
# ax.set_yticks(np.arange(n_rows + 1) - 0.5, minor=True)
# ax.grid(which="minor", color="white", linewidth=1.5)
# ax.tick_params(which="minor", bottom=False, left=False)

# ax.set_title("Posterior Probability Distribution Across Anomalies (Initial Inference)",
#              fontsize=18, fontweight="bold", pad=12)
# ax.set_xlabel("Anomalies", fontsize=14)
# ax.set_ylabel("Injected Fault Scenario", fontsize=14)

# plt.tight_layout()
# plt.savefig("probability_heatmap.png", dpi=150)
# plt.show()


# ## Confidence vs Entropy
# top_prob = []
# for r in records:
#     top_anomaly = r["top_predicted_anomaly"]
#     top_prob.append(r["probabilities"].get(top_anomaly, 0.0))

# fig, ax = plt.subplots(figsize=(9, 6))

# ENTROPY_THRESHOLD = 0.5  # only label scenarios at or above this initial entropy

# for i, r in enumerate(records):
#     color  = "red" if hits1[i] == 0 else ("orange" if is_or[i] else "green")
#     marker = "D" if is_or[i] else "o"
#     ax.scatter(entropy[i], top_prob[i], color=color, marker=marker,
#                s=100, edgecolors="black", linewidths=0.5, zorder=3)

#     if entropy[i] >= ENTROPY_THRESHOLD:
#         label = scenarios[i]

#         ax.annotate(
#             label,
#             (entropy[i], top_prob[i]),
#             textcoords="offset points",
#             xytext=(-8, 8) if "Malfunction (IHab)" in label else (-6, -4),
#             ha="right",
#             va="top",
#             fontsize=12,
#             color="black"
#         )

# ax.tick_params(axis="both", labelsize=12)
# ax.set_xlabel("Initial Entropy (nats)", fontsize=14)
# ax.set_ylabel("Top Predicted Anomaly Probability (%)", fontsize=14)
# ax.set_title("Model Confidence vs. Entropy per Injected Fault Scenario", fontsize=18, fontweight="bold")
# ax.set_xlim(-0.006, 1)
# ax.set_ylim(0, 101.25)

# legend_handles = [
#     mpatches.Patch(color="green", label="Correct Diagnosis (single anomaly)"),
#     mpatches.Patch(color="orange", label="Correct Diagnosis (OR anomaly)"),
#     mpatches.Patch(color="red", label="Incorrect Diagnosis (hits@1 = 0)"),
#     plt.Line2D([0], [0], marker="D", color="w", markerfacecolor="grey",
#                markersize=10, label="OR anomaly scenario"),
# ]
# ax.legend(handles=legend_handles, fontsize=12)
# plt.tight_layout()
# plt.savefig("entropy_vs_confidence.png", dpi=150)
# plt.show()


## Inference Runtime Distribution

fig, ax = plt.subplots(figsize=(10, 4))

y = np.zeros(len(runtime))

ax.scatter(
    runtime,
    y,
    s=80,
    edgecolors="black",
    linewidths=0.5
)

# Mean and median
mean_runtime = np.mean(runtime)
median_runtime = np.median(runtime)

ax.axvline(
    mean_runtime,
    linestyle="--",
    linewidth=2,
    label=f"Mean = {mean_runtime:.3f} s"
)

ax.axvline(
    median_runtime,
    linestyle=":",
    linewidth=2,
    label=f"Median = {median_runtime:.3f} s"
)

ax.set_xlabel("Inference Runtime (s)", fontsize=12)
ax.set_yticks([])
ax.set_title(
    "Distribution of Inference Runtime",
    fontsize=18,
    fontweight="bold"
)

ax.legend(fontsize=11)

plt.tight_layout()
plt.savefig("inference_runtime_distribution.png", dpi=150)
plt.show()


# ## Hits@1 and Hits@3 <-- slightly redundant given current model performance
# hits3 = [r["hits@3"] for r in records]

# x = np.arange(len(scenarios))
# width = 0.35

# fig, ax = plt.subplots(figsize=(14, 5))
# b1 = ax.bar(x - width/2, hits1, width, label="Hits@1",
#             color=["red" if h == 0 else "blue" for h in hits1],
#             edgecolor="white")
# b2 = ax.bar(x + width/2, hits3, width, label="Hits@3",
#             color="green", edgecolor="white", alpha=0.8)

# ax.set_xticks(x)
# ax.set_xticklabels(scenarios, rotation=40, ha="right", fontsize=12)
# ax.set_yticks([0, 1])
# ax.set_yticklabels(["Miss", "Hit"])
# ax.set_title("Hits@1 vs Hits@3 per Scenario", fontsize=18, fontweight="bold")
# ax.legend()

# # Annotate the miss
# miss_idx = hits1.index(0)
# ax.annotate("Only miss\n(top-1)", xy=(miss_idx - width/2, 0),
#             xytext=(miss_idx - 2, 0.4),
#             arrowprops=dict(arrowstyle="->", color="red"),
#             fontsize=10, color="red")

# plt.tight_layout()
# plt.savefig("hits_comparison.png", dpi=150)
# # plt.show()