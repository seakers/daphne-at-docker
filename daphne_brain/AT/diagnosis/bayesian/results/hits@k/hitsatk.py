import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import seaborn as sns
import pandas as pd

# --- Load data ---
records = []
with open("default_results.jsonl") as f:
    for line in f:
        records.append(json.loads(line))

n = len(records)


# =================================================================
# 1. Aggregate accuracy: Initial vs Updated, hits@1
# =================================================================
metrics = ["initial_hits@1", "updated_hits@1", "initial_hits@3", "updated_hits@3"]
accs = [np.mean([r[m] for r in records]) for m in metrics]
initial_vals = [accs[0], accs[2]]
updated_vals = [accs[1], accs[3]]
 
# fig, ax = plt.subplots(figsize=(7, 5))
# x = np.arange(2)
# width = 0.35
 
# b1 = ax.bar(x - width / 2, initial_vals, width, label="Initial Diagnosis", color="#88CCEE", edgecolor="black")
# b2 = ax.bar(x + width / 2, updated_vals, width, label="Following Diagnostic Action", color="#44AA99", edgecolor="black")
 
# for bars in (b1, b2):
#     for bar in bars:
#         h = bar.get_height()
#         ax.text(bar.get_x() + bar.get_width() / 2, h + 0.01, f"{h:.0%}",
#                 ha="center", va="bottom", fontsize=20)
 
# ax.set_xticks(x)
# ax.set_xticklabels(["hits@1", "hits@3"], fontsize=20)
# ax.set_ylabel("Accuracy")
# ax.set_ylim(0, 1.1)
# ax.set_title(f"Baseline Model Diagnostic Accuracy by Inference Stage (n={n})", fontsize=20, fontweight="bold")
# ax.legend(fontsize= 20, loc='upper left')
# fig.tight_layout()
# fig.savefig("accuracy_bars.png", dpi=150)
# plt.show()


# =================================================================
# 2. Transition heatmap: hits@1 (initial hit/miss x updated hit/miss)
# =================================================================
# matrix1 = np.zeros((2, 2), dtype=int)
# for r in records:
#     matrix1[r["initial_hits@1"]][r["updated_hits@1"]] += 1

# fig, ax = plt.subplots(figsize=(5, 5))
# im = ax.imshow(matrix1, cmap="Blues", vmin=0)

# labels = ["Miss", "Hit"]
# ax.set_xticks([0, 1]); ax.set_xticklabels(labels, fontsize=11)
# ax.set_yticks([0, 1]); ax.set_yticklabels(labels, fontsize=11)
# ax.set_xlabel("Updated", fontsize=20)
# ax.set_ylabel("Initial", fontsize=20)
# ax.set_title(f"hits@1 Transitions (n={n})", fontsize=20, fontweight="bold")

# for i in range(2):
#     for j in range(2):
#         count = matrix1[i, j]
#         pct = count / n
#         color = "white" if count > matrix1.max() / 2 else "black"
#         ax.text(j, i, f"{count}\n({pct:.0%})", ha="center", va="center",
#                 color=color, fontsize=20, fontweight="bold")

# fig.colorbar(im, ax=ax, label="Count", shrink=0.8)
# fig.tight_layout()
# fig.savefig("transition_heatmap_hits1.png", dpi=150)
# plt.show()


# =================================================================
# 3. Entropy vs correctness (boxplot): does low entropy => correct?
# =================================================================
# correct = [r["updated_entropy"] for r in records if r["updated_hits@1"] == 1]
# incorrect = [r["updated_entropy"] for r in records if r["updated_hits@1"] == 0]

# fig, ax = plt.subplots(figsize=(6, 5))
# bp = ax.boxplot([correct, incorrect], tick_labels=["Correct (hits@1)", "Incorrect"],
#                  patch_artist=True, widths=0.5)
# for patch, color in zip(bp["boxes"], ["#117733", "#CC6677"]):
#     patch.set_facecolor(color)
#     patch.set_alpha(0.6)

# for i, vals in enumerate([correct, incorrect], start=1):
#     jitter = np.random.normal(0, 0.04, size=len(vals))
#     ax.scatter(np.full(len(vals), i) + jitter, vals, color="black", alpha=0.5, s=20, zorder=3)

# ax.set_ylabel("Updated Entropy (bits)", fontsize=20)
# ax.set_title("Updated Entropy vs. Final Correctness", fontsize=20, fontweight="bold")
# fig.tight_layout()
# fig.savefig("entropy_by_correctness.png", dpi=150)
# plt.show()

# =================================================================
# 4. Entropy change grouped by transition category (hits@1) — violin
#    Note: delta_entropy in the data is defined as initial - updated
#    (positive = reduction), which reads backwards on a plot. Here we
#    plot updated - initial instead, so a REDUCTION in entropy is
#    NEGATIVE (drops below zero) and an INCREASE is POSITIVE (rises
#    above zero) — matching the intuitive "down = reduced" reading.
# =================================================================
groups = {"Stayed Correct": [], "Improved (Miss → Hit)": [],
          "Worsened (Hit → Miss)": [], "Stayed Wrong": []}

for r in records:
    i, u = r["initial_hits@1"], r["updated_hits@1"]
    entropy_change = -r["delta_entropy"]  # flip sign: updated - initial
    if i == 1 and u == 1:
        groups["Stayed Correct"].append(entropy_change)
    elif i == 0 and u == 1:
        groups["Improved (Miss → Hit)"].append(entropy_change)
    elif i == 1 and u == 0:
        groups["Worsened (Hit → Miss)"].append(entropy_change)
    else:
        groups["Stayed Wrong"].append(entropy_change)

group_labels = [k for k, v in groups.items() if len(v) > 0]
data = [groups[k] for k in group_labels]
palette = {"Stayed Correct": "#117733", "Improved (Miss → Hit)": "#44AA99",
           "Worsened (Hit → Miss)": "#CC6677", "Stayed Wrong": "#882255"}
colors = [palette[lab] for lab in group_labels]

# Restructure into long-format DataFrame, respecting label order
df = pd.DataFrame({
    "Entropy Change": [v for vals in data for v in vals],
    "Transition": [lab for lab, vals in zip(group_labels, data) for _ in vals],
})

fig, ax = plt.subplots(figsize=(10, 6))

sns.violinplot(
    data=df,
    x="Transition",
    y="Entropy Change",
    order=group_labels,
    palette=dict(zip(group_labels, colors)),
    inner="box",
    inner_kws=dict(box_width=6, whis_width=2, color="grey", zorder=5),
    alpha=0.4,
    ax=ax
)

# After plotting, update each violin's edge color to match its fill color
for violin, color in zip(ax.collections, colors):
    r, g, b, _ = mcolors.to_rgba(color)
    violin.set_edgecolor((r, g, b, 0.6))

# Overlay individual data points (jittered)
for i, (vals, color) in enumerate(zip(data, colors)):
    x = np.random.normal(i, 0.04, size=len(vals))
    ax.scatter(x, vals, alpha=0.5, s=45, color=color, edgecolor="white", linewidth=0.5, zorder=3)

ax.axhline(0, color="gray", linestyle="--", linewidth=1)
ax.set_xlabel("")
ax.set_ylabel("Entropy Change (bits)", fontsize=20)
ax.set_title("Baseline Model Entropy Change Following Diagnostic Actions (by hits@1 Transition Category)", fontsize=20, fontweight="bold")
ax.tick_params(axis="both", labelsize=20)

fig.tight_layout()
fig.savefig("entropy_change_by_transition_violin.png", dpi=150)
plt.show()