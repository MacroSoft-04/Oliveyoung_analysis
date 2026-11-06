import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SRC_DIR
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SAVE_DIR = OUTPUT_DIR / "review_cnt"

plt.style.use("seaborn-v0_8-whitegrid")  # First and only
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Malgun Gothic", "AppleGothic", "NanumGothic"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv(DATA_DIR / "oliveyoung_lip_2.10.csv")

top_10_brands = df["브랜드"].value_counts().head(10).index
df_top = df[df["브랜드"].isin(top_10_brands)]

avg_review_brands = (
    df_top.groupby("브랜드")["리뷰수"].mean().sort_values(ascending=False)
)

plt.figure(figsize=(12, 6))
sns.barplot(
    x=avg_review_brands.index,
    y=avg_review_brands.values,
    hue=avg_review_brands.index,
    palette="Set3",
    legend=False,
)

plt.title("점유율 Top 10 브랜드의 제품 1개당 평균 리뷰 수", fontsize=16, pad=20)
plt.xlabel("브랜드명", fontsize=12)
plt.ylabel("평균 리뷰 수 (개)", fontsize=12)
plt.xticks(rotation=45)

offset = avg_review_brands.max() * 0.02
for i, val in enumerate(avg_review_brands.values):
    plt.text(
        i, val + offset, f"{val:,.0f}개", ha="center", fontsize=11, fontweight="bold"
    )

plt.tight_layout()
plt.savefig(SAVE_DIR, dpi=300, bbox_inches="tight")
