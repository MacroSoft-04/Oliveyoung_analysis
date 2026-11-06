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
SAVE_DIR = OUTPUT_DIR / "top10_brand"

plt.style.use("seaborn-v0_8-whitegrid")  # First and only
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Malgun Gothic", "AppleGothic", "NanumGothic"]
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_csv(DATA_DIR / "oliveyoung_lip_2.10.csv")

top_brands = df["브랜드"].value_counts().head(10)

plt.figure(figsize=(12, 6))

sns.barplot(x=top_brands.index, y=top_brands.values, palette="Set2")

plt.title("올리브영 립 메이크업 Top 300 점유율 (상위 10개 브랜드)", fontsize=16, pad=20)
plt.xlabel("브랜드명", fontsize=12)
plt.ylabel("랭킹에 진입한 상품 개수 (개)", fontsize=12)
plt.xticks(rotation=45)  # 브랜드명이 길면 겹치니까 45도 기울여서 표시

for i, count in enumerate(top_brands.values):
    plt.text(i, count + 0.3, f"{count}개", ha="center", fontsize=11, fontweight="bold")

plt.tight_layout()
plt.savefig(SAVE_DIR, dpi=300, bbox_inches="tight")
