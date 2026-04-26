"""
Bank Customer Churn - Chart Exporter for LinkedIn
Run this script to generate and save 6 professional charts
as PNG images inside a 'linkedin_charts' folder.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

# ── Setup ──────────────────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "linkedin_charts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Style
sns.set_theme(style="darkgrid", palette="muted")
plt.rcParams.update({
    "figure.facecolor": "#1a1a2e",
    "axes.facecolor":   "#16213e",
    "axes.labelcolor":  "white",
    "xtick.color":      "white",
    "ytick.color":      "white",
    "text.color":       "white",
    "axes.titlecolor":  "white",
    "grid.color":       "#2a2a4a",
    "font.family":      "DejaVu Sans",
})

ACCENT   = "#e94560"
SAFE     = "#0f3460"
TEAL     = "#00b4d8"
GOLD     = "#ffd166"
PURPLE   = "#a29bfe"

# ── Load Data ──────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "bank_clean.csv")
df = pd.read_csv(DATA_PATH)

print(f"✅  Loaded {len(df):,} rows from bank_clean.csv")
print(f"📁  Charts will be saved to: {OUTPUT_DIR}\n")

# ── Chart 1 : Churn Distribution (Pie) ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 7), facecolor="#1a1a2e")
churn_counts = df["churn"].value_counts()
labels  = ["Retained 🟢", "Churned 🔴"]
colors  = [TEAL, ACCENT]
explode = (0, 0.08)

wedges, texts, autotexts = ax.pie(
    churn_counts, labels=labels, colors=colors, explode=explode,
    autopct="%1.1f%%", startangle=140,
    textprops={"color": "white", "fontsize": 13},
    wedgeprops={"edgecolor": "#1a1a2e", "linewidth": 2},
)
for a in autotexts:
    a.set_fontsize(15)
    a.set_fontweight("bold")

ax.set_title("Customer Churn Distribution\n(10,000 Bank Customers)", fontsize=16,
             fontweight="bold", color="white", pad=20)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "1_churn_distribution.png"), dpi=150,
            bbox_inches="tight", facecolor="#1a1a2e")
plt.close()
print("✅  Chart 1 saved: 1_churn_distribution.png")

# ── Chart 2 : Churn Rate by Country ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5), facecolor="#1a1a2e")
country_churn = df.groupby("country")["churn"].mean().sort_values(ascending=False) * 100
bars = ax.bar(country_churn.index, country_churn.values,
              color=[ACCENT, GOLD, TEAL, PURPLE][:len(country_churn)],
              edgecolor="#1a1a2e", linewidth=1.5, width=0.5)

for bar, val in zip(bars, country_churn.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f"{val:.1f}%", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color="white")

ax.set_title("Churn Rate by Country", fontsize=15, fontweight="bold", color="white")
ax.set_ylabel("Churn Rate (%)", fontsize=12)
ax.set_xlabel("Country", fontsize=12)
ax.set_ylim(0, country_churn.max() + 8)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "2_churn_by_country.png"), dpi=150,
            bbox_inches="tight", facecolor="#1a1a2e")
plt.close()
print("✅  Chart 2 saved: 2_churn_by_country.png")

# ── Chart 3 : Churn Rate by Age Group ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5), facecolor="#1a1a2e")
df["age_group"] = pd.cut(df["age"],
                          bins=[18, 30, 40, 50, 60, 100],
                          labels=["18-30", "31-40", "41-50", "51-60", "60+"])
age_churn = df.groupby("age_group", observed=True)["churn"].mean() * 100

ax.plot(age_churn.index.astype(str), age_churn.values,
        marker="o", markersize=10, linewidth=2.5,
        color=ACCENT, markerfacecolor=GOLD, markeredgecolor="white", markeredgewidth=1.5)

for x, y in enumerate(age_churn.values):
    ax.text(x, y + 1.2, f"{y:.1f}%", ha="center", fontsize=11,
            fontweight="bold", color="white")

ax.set_title("Churn Rate by Age Group", fontsize=15, fontweight="bold", color="white")
ax.set_ylabel("Churn Rate (%)", fontsize=12)
ax.set_xlabel("Age Group", fontsize=12)
ax.set_ylim(0, age_churn.max() + 12)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "3_churn_by_age.png"), dpi=150,
            bbox_inches="tight", facecolor="#1a1a2e")
plt.close()
print("✅  Chart 3 saved: 3_churn_by_age.png")

# ── Chart 4 : Active Member vs Churn ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), facecolor="#1a1a2e")
active_churn = df.groupby("active_member")["churn"].mean() * 100
labels = ["Inactive Member", "Active Member"]
colors = [ACCENT, TEAL]

bars = ax.barh(labels, active_churn.values, color=colors,
               edgecolor="#1a1a2e", linewidth=1.5, height=0.4)

for bar, val in zip(bars, active_churn.values):
    ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}%", va="center", fontsize=13,
            fontweight="bold", color="white")

ax.set_title("Churn Rate: Active vs Inactive Members", fontsize=14,
             fontweight="bold", color="white")
ax.set_xlabel("Churn Rate (%)", fontsize=12)
ax.set_xlim(0, active_churn.max() + 12)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "4_active_member_churn.png"), dpi=150,
            bbox_inches="tight", facecolor="#1a1a2e")
plt.close()
print("✅  Chart 4 saved: 4_active_member_churn.png")

# ── Chart 5 : Credit Score Distribution (Churn vs Retained) ───────────────────
fig, ax = plt.subplots(figsize=(10, 5), facecolor="#1a1a2e")
churned  = df[df["churn"] == 1]["credit_score"]
retained = df[df["churn"] == 0]["credit_score"]

ax.hist(retained, bins=40, alpha=0.7, color=TEAL,   label="Retained", edgecolor="#1a1a2e")
ax.hist(churned,  bins=40, alpha=0.7, color=ACCENT, label="Churned",  edgecolor="#1a1a2e")

ax.set_title("Credit Score Distribution: Churned vs Retained", fontsize=14,
             fontweight="bold", color="white")
ax.set_xlabel("Credit Score", fontsize=12)
ax.set_ylabel("Number of Customers", fontsize=12)
ax.legend(fontsize=12,
          handles=[
              mpatches.Patch(color=TEAL,   label="Retained"),
              mpatches.Patch(color=ACCENT, label="Churned"),
          ])
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "5_credit_score_distribution.png"), dpi=150,
            bbox_inches="tight", facecolor="#1a1a2e")
plt.close()
print("✅  Chart 5 saved: 5_credit_score_distribution.png")

# ── Chart 6 : Churn by Gender ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5), facecolor="#1a1a2e")
gender_churn = df.groupby("gender")["churn"].mean().sort_values(ascending=False) * 100
colors = [ACCENT, TEAL]

bars = ax.bar(gender_churn.index, gender_churn.values, color=colors,
              edgecolor="#1a1a2e", linewidth=1.5, width=0.4)

for bar, val in zip(bars, gender_churn.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f"{val:.1f}%", ha="center", fontsize=13,
            fontweight="bold", color="white")

ax.set_title("Churn Rate by Gender", fontsize=15, fontweight="bold", color="white")
ax.set_ylabel("Churn Rate (%)", fontsize=12)
ax.set_xlabel("Gender", fontsize=12)
ax.set_ylim(0, gender_churn.max() + 10)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "6_churn_by_gender.png"), dpi=150,
            bbox_inches="tight", facecolor="#1a1a2e")
plt.close()
print("✅  Chart 6 saved: 6_churn_by_gender.png")

# ── Done ───────────────────────────────────────────────────────────────────────
print(f"\n🎉 All 6 charts saved to → {OUTPUT_DIR}")
print("📌 Upload them to LinkedIn starting with Chart 1 (Churn Distribution) as the cover image!")
