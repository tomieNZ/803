"""
W1A1 Data Analysis - Sales Category Performance
使用数据聚合技术分析各产品类别的销售表现
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np
import os

# ── 1. 加载数据 ──────────────────────────────────────────────────────────────
df = pd.read_excel("Data_set_w1A1.xlsx", sheet_name="descriptive_aggregation (1)")

# ── 2. 派生聚合指标 ──────────────────────────────────────────────────────────
total_sales    = df["sales_sum"].sum()
total_qty      = df["quantity_sum"].sum()
total_txns     = df["sales_count"].sum()

df["sales_share_%"]    = (df["sales_sum"]    / total_sales * 100).round(2)
df["quantity_share_%"] = (df["quantity_sum"] / total_qty   * 100).round(2)
df["txn_share_%"]      = (df["sales_count"]  / total_txns  * 100).round(2)

# 每单位销售额（平均售价）
df["avg_price_per_unit"] = (df["sales_sum"] / df["quantity_sum"]).round(2)

# 与均值的偏差（衡量类别强弱）
df["sales_mean_vs_avg"] = (df["sales_mean"] - df["sales_mean"].mean()).round(2)

print("=" * 60)
print("  AGGREGATED DATASET OVERVIEW")
print("=" * 60)
print(df.to_string(index=False))
print()
print(f"  Total Revenue   : ${total_sales:,}")
print(f"  Total Units Sold: {total_qty:,}")
print(f"  Total Transactions: {total_txns}")
print()

# ── 3. 关键洞察 ──────────────────────────────────────────────────────────────
top_revenue  = df.loc[df["sales_sum"].idxmax(),    "category"]
top_avg      = df.loc[df["sales_mean"].idxmax(),   "category"]
top_vol      = df.loc[df["quantity_sum"].idxmax(), "category"]
top_price    = df.loc[df["avg_price_per_unit"].idxmax(), "category"]

print("  KEY INSIGHTS (Aggregation-based)")
print(f"  • Highest Total Revenue    : Category {top_revenue}")
print(f"  • Highest Avg Transaction  : Category {top_avg}")
print(f"  • Most Units Sold          : Category {top_vol}")
print(f"  • Highest Avg Unit Price   : Category {top_price}")
print("=" * 60)

# ── 4. 可视化 ────────────────────────────────────────────────────────────────
COLORS = {"A": "#4C9BE8", "B": "#F28C38", "C": "#6DBF67"}
cats   = df["category"].tolist()
colors = [COLORS[c] for c in cats]

fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor("#F7F9FC")
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

def style_ax(ax, title):
    ax.set_facecolor("#FFFFFF")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=10)

# ── 4-1. Total Sales Bar ─────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
bars = ax1.bar(cats, df["sales_sum"], color=colors, width=0.5, edgecolor="white")
for bar, val in zip(bars, df["sales_sum"]):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
             f"${val:,}", ha="center", va="bottom", fontsize=10, fontweight="bold")
style_ax(ax1, "Total Sales Revenue by Category")
ax1.set_ylabel("Revenue ($)")
ax1.set_ylim(0, df["sales_sum"].max() * 1.15)

# ── 4-2. Average Transaction Value Bar ───────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
bars2 = ax2.bar(cats, df["sales_mean"], color=colors, width=0.5, edgecolor="white")
grand_mean = df["sales_mean"].mean()
ax2.axhline(grand_mean, color="gray", linestyle="--", linewidth=1.2, label=f"Overall Mean: ${grand_mean:.1f}")
for bar, val in zip(bars2, df["sales_mean"]):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f"${val:.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
style_ax(ax2, "Avg Transaction Value by Category")
ax2.set_ylabel("Avg Sale ($)")
ax2.set_ylim(500, df["sales_mean"].max() * 1.15)
ax2.legend(fontsize=9)

# ── 4-3. Revenue Share Donut ─────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[0, 2])
wedges, texts, autotexts = ax3.pie(
    df["sales_share_%"], labels=cats, colors=colors,
    autopct="%1.1f%%", startangle=90,
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    pctdistance=0.75
)
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight("bold")
ax3.set_title("Revenue Share by Category", fontsize=12, fontweight="bold", pad=10)

# ── 4-4. Quantity vs Transactions Grouped Bar ─────────────────────────────────
ax4 = fig.add_subplot(gs[1, 0])
x    = np.arange(len(cats))
w    = 0.35
b1   = ax4.bar(x - w/2, df["quantity_sum"], w, label="Units Sold", color=colors, edgecolor="white")
b2   = ax4.bar(x + w/2, df["sales_count"],  w, label="Transactions",
               color=[c + "99" for c in ["#4C9BE8","#F28C38","#6DBF67"]],
               edgecolor="white", hatch="//")
# 半透明色
for bar2, col in zip(b2, colors):
    bar2.set_facecolor(col)
    bar2.set_alpha(0.55)
ax4.set_xticks(x); ax4.set_xticklabels(cats)
style_ax(ax4, "Units Sold vs Transactions")
ax4.set_ylabel("Count")
ax4.legend(fontsize=9)
for bar, val in zip(b1, df["quantity_sum"]):
    ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2, str(val),
             ha="center", va="bottom", fontsize=9)
for bar, val in zip(b2, df["sales_count"]):
    ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2, str(val),
             ha="center", va="bottom", fontsize=9)

# ── 4-5. Avg Unit Price ───────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[1, 1])
bars5 = ax5.bar(cats, df["avg_price_per_unit"], color=colors, width=0.5, edgecolor="white")
for bar, val in zip(bars5, df["avg_price_per_unit"]):
    ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
             f"${val:.2f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
style_ax(ax5, "Avg Price per Unit by Category")
ax5.set_ylabel("Price per Unit ($)")
ax5.set_ylim(0, df["avg_price_per_unit"].max() * 1.2)

# ── 4-6. Sales Mean Deviation from Overall Average ────────────────────────────
ax6 = fig.add_subplot(gs[1, 2])
deviations = df["sales_mean_vs_avg"].tolist()
bar_colors  = ["#E85C5C" if d < 0 else "#6DBF67" for d in deviations]
bars6 = ax6.bar(cats, deviations, color=bar_colors, width=0.5, edgecolor="white")
ax6.axhline(0, color="gray", linewidth=1)
for bar, val in zip(bars6, deviations):
    offset = 1 if val >= 0 else -3
    ax6.text(bar.get_x()+bar.get_width()/2, val + offset,
             f"{val:+.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
style_ax(ax6, "Avg Transaction Value vs Overall Mean")
ax6.set_ylabel("Deviation ($)")

# ── 主标题 ────────────────────────────────────────────────────────────────────
fig.suptitle(
    "Sales Performance Analysis by Category\n"
    "Story: Category B leads in all key metrics — revenue, volume, and transaction value",
    fontsize=14, fontweight="bold", y=1.01, color="#2C3E50"
)

plt.savefig("analysis_output.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("\n  Chart saved → analysis_output.png")
plt.close()
