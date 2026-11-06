import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import numpy as np
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SRC_DIR
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
SAVE_DIR = OUTPUT_DIR / "review_ranking_relationship"

if platform.system() == "Darwin":  # Mac
    plt.rc("font", family="AppleGothic")
elif platform.system() == "Windows":  # Windows
    plt.rc("font", family="Malgun Gothic")
plt.rc("axes", unicode_minus=False)

df = pd.read_csv(DATA_DIR / "oliveyoung_lip_2.10.csv")

if "할인율(%)" not in df.columns:
    df["할인율(%)"] = df.apply(
        lambda x: (
            round((x["정가"] - x["판매가"]) / x["정가"] * 100, 1)
            if x["정가"] > 0
            else 0
        ),
        axis=1,
    )

plt.figure(figsize=(12, 7))

# 산점도 그리기 (랭킹 vs 리뷰수)
sns.scatterplot(data=df, x="랭킹", y="리뷰수", alpha=0.6, color="purple", s=80)

plt.title("랭킹과 리뷰 수의 관계", fontsize=16, pad=20)
plt.xlabel("랭킹 (1위 ➔ 300위)", fontsize=13)
plt.ylabel("누적 리뷰 수 (개)", fontsize=13)

plt.gca().invert_xaxis()

plt.ylim(0, 50000)

plt.axvspan(1, 10, color="yellow", alpha=0.15, label="Top 10 구역")
plt.legend()

plt.tight_layout()
plt.savefig(SAVE_DIR, dpi=300, bbox_inches="tight")
