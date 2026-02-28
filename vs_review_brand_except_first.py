import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# ---------------------------------------------------
# [필수] 한글 폰트 & 마이너스 기호 깨짐 방지
# ---------------------------------------------------
if platform.system() == 'Darwin':  # Mac 사용자
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows 사용자
    plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# ---------------------------------------------------
# 1. 데이터 불러오기
# ---------------------------------------------------
df = pd.read_csv("oliveyoung_lip_2.10.csv")

# ---------------------------------------------------
# 2. 핵심 로직: 브랜드별 1등 제품 솎아내기
# ---------------------------------------------------
# 방법: 리뷰 수 기준으로 내림차순(큰 것부터) 줄을 세운 다음, 각 브랜드별 첫 번째(1등) 줄만 빼고 가져옵니다.

# 1) 브랜드와 리뷰수 기준으로 정렬
df_sorted = df.sort_values(by=['브랜드', '리뷰수'], ascending=[True, False])

# 2) 각 브랜드 그룹에서 2번째 제품부터 끝까지만 남기기 (iloc[1:] 활용)
# (만약 제품이 딱 1개밖에 없던 브랜드라면 자동으로 리스트에서 아예 사라집니다!)
df_without_top1 = df_sorted.groupby('브랜드').tail(-1)

# 3) 1등이 제외된 상태에서 브랜드별 리뷰수 합산 및 상위 10개 추출
brand_review_sum = df_without_top1.groupby('브랜드')['리뷰수'].sum().sort_values(ascending=False).head(10)

# ---------------------------------------------------
# 3. 시각화 (막대 그래프)
# ---------------------------------------------------
plt.figure(figsize=(12, 6))

sns.barplot(x=brand_review_sum.index, y=brand_review_sum.values, palette='Set1') # 강렬한 Set1 테마

plt.title('🛡️ 브랜드 맷집 테스트: 1등 간판 제품 제외한 누적 리뷰 수 Top 10', fontsize=16, pad=20)
plt.xlabel('브랜드명', fontsize=12)
plt.ylabel('나머지 제품들의 누적 리뷰 수 합계 (개)', fontsize=12)
plt.xticks(rotation=45)

# 숫자 텍스트 달아주기
offset = brand_review_sum.max() * 0.02
for i, count in enumerate(brand_review_sum.values):
    plt.text(i, count + offset, f"{count:,.0f}개", ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()