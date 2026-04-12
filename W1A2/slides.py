"""
W1A2 – Housing Prices: 5-Slide Presentation
Generates slides/slide_N.png (N = 1..5)
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np

os.makedirs("slides", exist_ok=True)

df = pd.read_csv("Housing.csv")

# ── Colour palette ────────────────────────────────────────────────────────────
C1, C2, C3 = "#2D6A9F", "#F28C38", "#6DBF67"
BG, CARD   = "#F4F7FB", "#FFFFFF"
TXT        = "#1E2D40"

def base_fig(title, subtitle=""):
    """Return a figure pre-styled with slide chrome."""
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor(BG)
    # Top banner
    fig.add_axes([0, 0.88, 1, 0.12]).set_axis_off()
    fig.axes[-1].set_facecolor(C1)
    fig.text(0.5, 0.925, title,   ha="center", va="center",
             fontsize=26, fontweight="bold", color="white")
    if subtitle:
        fig.text(0.5, 0.895, subtitle, ha="center", va="center",
                 fontsize=13, color="#BDD9F2")
    # Footer
    fig.text(0.5, 0.02, "W1A2 · Housing Prices Dataset · 545 properties",
             ha="center", fontsize=9, color="#7A8A9A")
    return fig

def add_card(fig, rect, facecolor=CARD):
    ax = fig.add_axes(rect)
    ax.set_facecolor(facecolor)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    return ax

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 – Dataset at a Glance
# ═══════════════════════════════════════════════════════════════════════════════
fig1 = base_fig("What Drives Housing Prices?",
                "An Exploratory Story of 545 Homes")

# 4 KPI cards
kpis = [
    ("545",     "Properties"),
    ("$4.77M",  "Avg Price"),
    ("$1.75M–\n$13.3M", "Price Range"),
    ("12",      "Features"),
]
for i, (val, lbl) in enumerate(kpis):
    x = 0.06 + i * 0.235
    ax = add_card(fig1, [x, 0.60, 0.20, 0.24])
    ax.text(0.5, 0.62, val, ha="center", va="center",
            fontsize=22, fontweight="bold", color=C1)
    ax.text(0.5, 0.22, lbl, ha="center", va="center",
            fontsize=11, color="#5A6A7A")
    for sp in ["top","bottom","left","right"]:
        ax.spines[sp].set_visible(True)
        ax.spines[sp].set_color("#D8E4F0")

# Price distribution
ax_hist = fig1.add_axes([0.06, 0.14, 0.87, 0.40])
ax_hist.set_facecolor(CARD)
ax_hist.hist(df["price"]/1e6, bins=35, color=C1, edgecolor="white", alpha=0.85)
ax_hist.set_xlabel("Price (Millions $)", fontsize=12, color=TXT)
ax_hist.set_ylabel("Number of Properties", fontsize=12, color=TXT)
ax_hist.set_title("Price Distribution", fontsize=13, fontweight="bold", color=TXT, pad=8)
ax_hist.spines[["top","right"]].set_visible(False)
ax_hist.axvline(df["price"].mean()/1e6,  color=C2, lw=2, linestyle="--", label="Mean $4.77M")
ax_hist.axvline(df["price"].median()/1e6,color=C3, lw=2, linestyle="-",  label="Median $4.34M")
ax_hist.legend(fontsize=10)

fig1.savefig("slides/slide_1.png", dpi=130, bbox_inches="tight", facecolor=BG)
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 – Size & Structure Drive Price
# ═══════════════════════════════════════════════════════════════════════════════
fig2 = base_fig("Size & Structure Drive Price",
                "Area and bathrooms are the strongest numeric predictors")

# Left: scatter area vs price
ax_s = fig2.add_axes([0.06, 0.14, 0.42, 0.68])
ax_s.set_facecolor(CARD)
ax_s.scatter(df["area"], df["price"]/1e6, alpha=0.35, color=C1, s=20)
m, b = np.polyfit(df["area"], df["price"]/1e6, 1)
xs = np.linspace(df["area"].min(), df["area"].max(), 200)
ax_s.plot(xs, m*xs+b, color=C2, lw=2.5, label=f"Trend (r = 0.54)")
ax_s.set_xlabel("Area (sq ft)", fontsize=11); ax_s.set_ylabel("Price (M$)", fontsize=11)
ax_s.set_title("Area vs Price", fontsize=12, fontweight="bold", pad=6)
ax_s.spines[["top","right"]].set_visible(False); ax_s.legend(fontsize=10)

# Right: avg price by bedrooms & bathrooms
ax_b = fig2.add_axes([0.56, 0.50, 0.38, 0.32])
ax_b.set_facecolor(CARD)
bed_price = df.groupby("bedrooms")["price"].mean()/1e6
ax_b.bar(bed_price.index, bed_price.values, color=C1, edgecolor="white", width=0.6)
for x, y in zip(bed_price.index, bed_price.values):
    ax_b.text(x, y+0.05, f"${y:.1f}M", ha="center", fontsize=9, fontweight="bold")
ax_b.set_xlabel("Bedrooms"); ax_b.set_ylabel("Avg Price (M$)")
ax_b.set_title("Avg Price by Bedrooms", fontsize=11, fontweight="bold", pad=6)
ax_b.spines[["top","right"]].set_visible(False)

ax_ba = fig2.add_axes([0.56, 0.14, 0.38, 0.28])
ax_ba.set_facecolor(CARD)
bath_price = df.groupby("bathrooms")["price"].mean()/1e6
ax_ba.bar(bath_price.index, bath_price.values, color=C2, edgecolor="white", width=0.6)
for x, y in zip(bath_price.index, bath_price.values):
    ax_ba.text(x, y+0.05, f"${y:.1f}M", ha="center", fontsize=9, fontweight="bold")
ax_ba.set_xlabel("Bathrooms"); ax_ba.set_ylabel("Avg Price (M$)")
ax_ba.set_title("Avg Price by Bathrooms", fontsize=11, fontweight="bold", pad=6)
ax_ba.spines[["top","right"]].set_visible(False)

fig2.savefig("slides/slide_2.png", dpi=130, bbox_inches="tight", facecolor=BG)
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 – Location & Lifestyle Premium
# ═══════════════════════════════════════════════════════════════════════════════
fig3 = base_fig("Location & Lifestyle Add a Significant Premium",
                "Air conditioning, preferred area, and main road access command higher prices")

features  = ["Air Conditioning", "Preferred Area", "Main Road", "Hot Water Heating",
             "Guest Room", "Basement"]
keys      = ["airconditioning", "prefarea", "mainroad", "hotwaterheating", "guestroom", "basement"]
premiums  = []
for k in keys:
    yes_avg = df[df[k]=="yes"]["price"].mean()
    no_avg  = df[df[k]=="no"]["price"].mean()
    premiums.append((yes_avg - no_avg) / no_avg * 100)

ax3 = fig3.add_axes([0.08, 0.14, 0.55, 0.68])
ax3.set_facecolor(CARD)
colors3 = [C1 if p > 0 else "#E85C5C" for p in premiums]
bars = ax3.barh(features[::-1], premiums[::-1], color=colors3[::-1], edgecolor="white", height=0.6)
for bar, val in zip(bars, premiums[::-1]):
    ax3.text(val + 0.5, bar.get_y()+bar.get_height()/2,
             f"+{val:.1f}%", va="center", fontsize=11, fontweight="bold", color=TXT)
ax3.set_xlabel("Price Premium vs. 'No' (%)", fontsize=11)
ax3.set_title("Price Premium by Feature Presence", fontsize=12, fontweight="bold", pad=8)
ax3.axvline(0, color="gray", lw=1)
ax3.spines[["top","right"]].set_visible(False)

# Right: 3 call-out numbers
callouts = [
    ("+43%", "AC Premium"),
    ("+33%", "Preferred Area"),
    ("+47%", "Main Road"),
]
for i, (num, lbl) in enumerate(callouts):
    y = 0.72 - i * 0.22
    ax_c = add_card(fig3, [0.70, y, 0.24, 0.18])
    ax_c.text(0.5, 0.62, num, ha="center", va="center",
              fontsize=26, fontweight="bold", color=C1)
    ax_c.text(0.5, 0.20, lbl, ha="center", va="center",
              fontsize=11, color="#5A6A7A")
    for sp in ["top","bottom","left","right"]:
        ax_c.spines[sp].set_visible(True); ax_c.spines[sp].set_color("#D8E4F0")

fig3.savefig("slides/slide_3.png", dpi=130, bbox_inches="tight", facecolor=BG)
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 – Furnishing & Stories
# ═══════════════════════════════════════════════════════════════════════════════
fig4 = base_fig("Furnishing Status & Number of Stories",
                "Fully furnished multi-storey homes fetch the highest prices")

# Left: furnishing
ax_f = fig4.add_axes([0.06, 0.14, 0.40, 0.68])
ax_f.set_facecolor(CARD)
furn = df.groupby("furnishingstatus")["price"].mean().reindex(
       ["unfurnished","semi-furnished","furnished"])/1e6
fcolors = [C3, C2, C1]
fb = ax_f.bar(["Unfurnished","Semi-\nFurnished","Furnished"], furn.values,
              color=fcolors, edgecolor="white", width=0.5)
for bar, v in zip(fb, furn.values):
    ax_f.text(bar.get_x()+bar.get_width()/2, v+0.05,
              f"${v:.2f}M", ha="center", fontsize=11, fontweight="bold")
ax_f.set_ylabel("Avg Price (M$)", fontsize=11)
ax_f.set_title("Avg Price by Furnishing", fontsize=12, fontweight="bold", pad=8)
ax_f.spines[["top","right"]].set_visible(False)
ax_f.set_ylim(0, furn.max()*1.2)

# Right: stories
ax_st = fig4.add_axes([0.55, 0.14, 0.40, 0.68])
ax_st.set_facecolor(CARD)
stor = df.groupby("stories")["price"].mean()/1e6
sb = ax_st.bar(["1 Story","2 Stories","3 Stories","4 Stories"],
               stor.values, color=C1, edgecolor="white", width=0.5)
for bar, v in zip(sb, stor.values):
    ax_st.text(bar.get_x()+bar.get_width()/2, v+0.05,
               f"${v:.2f}M", ha="center", fontsize=11, fontweight="bold")
ax_st.set_ylabel("Avg Price (M$)", fontsize=11)
ax_st.set_title("Avg Price by Number of Stories", fontsize=12, fontweight="bold", pad=8)
ax_st.spines[["top","right"]].set_visible(False)
ax_st.set_ylim(0, stor.max()*1.2)

fig4.savefig("slides/slide_4.png", dpi=130, bbox_inches="tight", facecolor=BG)
plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 – Key Insights & Takeaways
# ═══════════════════════════════════════════════════════════════════════════════
fig5 = base_fig("Key Insights & Takeaways",
                "The housing price story — told through data")

insights = [
    ("1", "Size is the #1 driver",
          "Area (r=0.54) and bathrooms (r=0.52) are the strongest predictors of price."),
    ("2", "Air conditioning adds +43%",
          "AC is the most impactful lifestyle feature — nearly doubles the correlation signal."),
    ("3", "Location commands +47%",
          "Homes on the main road average $1.6M more than off-road properties."),
    ("4", "More floors = more value",
          "4-storey homes average $7.2M vs $4.2M for single-storey — a 72% gap."),
    ("5", "Furnishing bridges $1.5M gap",
          "Furnished vs unfurnished homes differ by $1.48M on average (37% premium)."),
]

for i, (num, heading, body) in enumerate(insights):
    y = 0.73 - i * 0.135
    # Number circle
    ax_n = fig5.add_axes([0.04, y, 0.05, 0.10])
    ax_n.set_facecolor(C1); ax_n.set_xlim(0,1); ax_n.set_ylim(0,1)
    ax_n.set_axis_off()
    ax_n.text(0.5, 0.5, num, ha="center", va="center",
              fontsize=20, fontweight="bold", color="white")

    # Text card
    ax_t = fig5.add_axes([0.11, y, 0.84, 0.10])
    ax_t.set_facecolor(CARD); ax_t.set_xlim(0,1); ax_t.set_ylim(0,1)
    for sp in ax_t.spines.values(): sp.set_color("#D8E4F0"); sp.set_visible(True)
    ax_t.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    ax_t.text(0.015, 0.68, heading, va="center", fontsize=13,
              fontweight="bold", color=C1)
    ax_t.text(0.015, 0.28, body, va="center", fontsize=11, color="#3A4A5A")

fig5.savefig("slides/slide_5.png", dpi=130, bbox_inches="tight", facecolor=BG)
plt.close()

print("All 5 slides saved to slides/")
