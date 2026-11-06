import pandas as pd
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = SRC_DIR
DATA_DIR = PROJECT_ROOT / "data"

df = pd.read_csv(DATA_DIR / "oliveyoung_lip_2.10.csv")

df["할인율(%)"] = df.apply(
    lambda x: (
        round((x["정가"] - x["판매가"]) / x["정가"] * 100, 1) if x["정가"] > 0 else 0
    ),
    axis=1,
)

df.to_csv(DATA_DIR / "oliveyoung_lip_2.10.csv", index=False, encoding="utf-8-sig")
print(" done. check the data")
