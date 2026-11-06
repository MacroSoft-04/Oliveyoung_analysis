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
SAVE_DIR = OUTPUT_DIR / "cumulated_review_cnt"

plt.style.use("seaborn-v0_8-whitegrid")  # First and only
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Malgun Gothic", "AppleGothic", "NanumGothic"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv(DATA_DIR / "oliveyoung_lip_2.10.csv")

df_sorted = df.sort_values(by=["브랜드", "리뷰수"], ascending=[True, False])

df_without_top1 = df_sorted.groupby("브랜드").tail(-1)

brand_review_sum = (
    df_without_top1.groupby("브랜드")["리뷰수"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

sns.barplot(x=brand_review_sum.index, y=brand_review_sum.values, palette="Set1")

plt.title(
    "브랜드 맷집 테스트: 1등 간판 제품 제외한 누적 리뷰 수 Top 10", fontsize=16, pad=20
)
plt.xlabel("브랜드명", fontsize=12)
plt.ylabel("나머지 제품들의 누적 리뷰 수 합계 (개)", fontsize=12)
plt.xticks(rotation=45)

offset = brand_review_sum.max() * 0.02
for i, count in enumerate(brand_review_sum.values):
    plt.text(
        i,
        count + offset,
        f"{count:,.0f}개",
        ha="center",
        fontsize=11,
        fontweight="bold",
    )

plt.tight_layout()
plt.savefig(SAVE_DIR, dpi=300, bbox_inches="tight")
