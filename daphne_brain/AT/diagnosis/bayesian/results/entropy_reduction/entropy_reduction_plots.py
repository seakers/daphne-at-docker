import json
import matplotlib.pyplot as plt
import numpy as np

# Load data from default results
records = []
with open("default_results.jsonl") as f:
    for line in f:
        records.append(json.loads(line))

scenarios       = [r["scenario_id"] for r in records]
initial_entropy = [r["initial_entropy"] for r in records]
updated_entropy = [r["updated_entropy"] for r in records]
delta_entropy   = [r["delta_entropy"] for r in records]

# Sort by delta entropy for readability
order           = np.argsort(delta_entropy)
scenarios_s     = [scenarios[i] for i in order]
initial_s       = [initial_entropy[i] for i in order]
updated_s       = [updated_entropy[i] for i in order]
delta_s         = [delta_entropy[i] for i in order]

# Threshold for significant change
THRESHOLD = 0.15

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 10), constrained_layout=True)
# remove plt.tight_layout() at the bottom

y = np.arange(len(scenarios_s))

# Draw connecting lines between initial and updated entropy
for i, (init, upd, delta, scenario) in enumerate(zip(initial_s, updated_s, delta_s, scenarios_s)):    # Color by direction of change
    color = "#117733" if delta > 0 else "#CC6677" if delta < 0 else "black"  # green = reduction, red = increase


    # Draw connecting line from initial to updated entropy
    ax.plot([init, upd], [i, i], color=color, linewidth=0.8, alpha=0.6, zorder=1)

    # Dot only at updated entropy, colored by direction
    ax.scatter(upd, i, color=color, s=60, zorder=3, edgecolor="white", linewidth=0.5)

    X_RIGHT_THRESHOLD = 0.9  # adjust based on your x-axis range
    X_LEFT_THRESHOLD = 0.05  # if dot is very close to the left edge

    if abs(delta) >= THRESHOLD:
        flipped = False
        if delta > 0:
            if upd <= X_LEFT_THRESHOLD:
                x_pos = upd + 0.0075  # flip to right side
                ha    = "left"
                flipped = True
            else:
                x_pos = upd - 0.0075
                ha    = "right"
        else:
            if upd >= X_RIGHT_THRESHOLD:
                # Flip to left side to avoid running off the right edge
                x_pos = upd - 0.0075
                ha    = "right"
                flipped = True
            else:
                x_pos = upd + 0.0075
                ha    = "left"
 
        text_kwargs = dict(
            fontsize=14,
            va="center",
            ha=ha,
            color="black",
            fontweight="bold",
            zorder=4,
        )
        if flipped:
            # Flipped labels sit on the same side as the line's far endpoint,
            # so give them a white backing to keep the line from showing through
            text_kwargs["bbox"] = dict(
                facecolor="white", edgecolor="none", pad=1.5, alpha=0.85
            )
 
        ax.text(x_pos, i, scenario, **text_kwargs)
 
ax.set_yticks([])

# Formatting
ax.set_xlabel("Entropy (bits)", fontsize=20)
ax.tick_params(axis="x", labelsize=20)
ax.set_title(
    "Change in Entropy Following Diagnostic Actions (Baseline Model)",
    fontsize=20, fontweight="bold"
)
ax.set_xlim([0, 1.005])
# ax.grid(axis="x", linestyle="--", alpha=0.4)

plt.savefig("entropy_change_dotplot.png", dpi=150)
plt.show()