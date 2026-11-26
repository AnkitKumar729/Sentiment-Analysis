# Draws the two charts used in the presentation (same numbers as the notebook output).
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK, SLATE, GRID = "#1F2A30", "#4A5A63", "#DDE3E1"
GREEN, RED, AMBER = "#2E8B57", "#C8483F", "#E8A33D"
plt.rcParams.update({"font.size": 13, "axes.edgecolor": GRID, "axes.labelcolor": SLATE,
                     "xtick.color": SLATE, "ytick.color": SLATE})

# Reviews per star rating
fig, ax = plt.subplots(figsize=(7.3, 4.6), dpi=200)
stars, counts = ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"], [477, 395, 679, 1333, 3774]
bars = ax.bar(stars, counts, color=AMBER, width=0.6)
ax.bar_label(bars, color=SLATE, padding=3)
ax.set_title("Reviews per star rating", color=INK, fontsize=15, loc="left")
ax.grid(axis="y", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
for side in ("top", "right", "left"): ax.spines[side].set_visible(False)
fig.tight_layout(); fig.savefig("outputs/slide_ratings.png", transparent=True)

# Positive vs negative sentences per feature
feats = ["sound", "quality", "price", "ear", "case", "noise", "battery", "fit", "bass", "cable", "cord", "volume"]
pos = [1804, 1433, 1059, 832, 566, 552, 489, 320, 307, 294, 267, 265]
neg = [277, 208, 22, 201, 39, 69, 44, 21, 58, 20, 50, 80]
fig, ax = plt.subplots(figsize=(7.6, 5.5), dpi=200)
ax.barh(feats[::-1], pos[::-1], color=GREEN, label="Positive sentences")
ax.barh(feats[::-1], neg[::-1], left=pos[::-1], color=RED, label="Negative sentences")
ax.grid(axis="x", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
for side in ("top", "right"): ax.spines[side].set_visible(False)
ax.legend(loc="lower right", frameon=False)
fig.tight_layout(); fig.savefig("outputs/slide_features.png", transparent=True)
print("charts saved")
