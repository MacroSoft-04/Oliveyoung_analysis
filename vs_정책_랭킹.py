import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import numpy as np

# ---------------------------------------------------
# [필수] 한글 폰트 & 마이너스 기호 깨짐 방지
# ---------------------------------------------------
if platform.system() == 'Darwin':  # Mac
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows
    plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# ---------------------------------------------------
# 1. 데이터 불러오기 및 전처리
# ---------------------------------------------------
df = pd.read_csv("oliveyoung_lip_2.10.csv")

# 혹시 '할인율(%)' 컬럼이 없다면 방어용으로 추가 생성
if '할인율(%)' not in df.columns:
    df['할인율(%)'] = df.apply(lambda x: round((x['정가'] - x['판매가']) / x['정가'] * 100, 1) if x['정가'] > 0 else 0, axis=1)

# ===================================================
# 💡 3번 아이디어: 리뷰 수 vs 랭킹의 관계 (산점도)
# ===================================================
plt.figure(figsize=(12, 7))

# 산점도 그리기 (랭킹 vs 리뷰수)
sns.scatterplot(data=df, x='랭킹', y='리뷰수', alpha=0.6, color='purple', s=80)

plt.title('🏆 랭킹과 리뷰 수의 관계', fontsize=16, pad=20)
plt.xlabel('랭킹 (1위 ➔ 300위)', fontsize=13)
plt.ylabel('누적 리뷰 수 (개)', fontsize=13)

# 직관적으로 1위가 왼쪽, 300위가 오른쪽에 오도록 X축 뒤집기
plt.gca().invert_xaxis()

# 🌟 [핵심 해결책] Y축(리뷰 수)을 0개부터 50,000개까지만 잘라서 확대해서 봅니다!
# (25만 개짜리 국민템은 그래프 위쪽 천장 밖으로 잠시 벗어납니다)
plt.ylim(0, 50000)

# 랭킹 1위~10위 구간에 직사각형으로 하이라이트 표시
plt.axvspan(1, 10, color='yellow', alpha=0.15, label='Top 10 구역')
plt.legend()

plt.tight_layout()
plt.show() # 두 번째 창이 뜹니다.