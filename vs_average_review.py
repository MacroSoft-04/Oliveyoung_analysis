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
# 2. 분석 대상을 '점유율 Top 10 브랜드'로 한정하기 (공정한 비교)
# (상품 1개 올려놓고 우연히 리뷰 터진 브랜드가 1등하는 걸 막기 위함)
# ---------------------------------------------------
top_10_brands = df['브랜드'].value_counts().head(10).index
df_top = df[df['브랜드'].isin(top_10_brands)]

# 🌟 [핵심] 질문자님의 아이디어! 
# 총합(sum)이 아니라 평균(mean)을 구합니다! (알아서 총 리뷰수를 상품 개수로 나눠줍니다)
avg_review_brands = df_top.groupby('브랜드')['리뷰수'].mean().sort_values(ascending=False)

# ---------------------------------------------------
# 3. 막대 그래프 그리기
# ---------------------------------------------------
plt.figure(figsize=(12, 6))
sns.barplot(x=avg_review_brands.index, y=avg_review_brands.values, palette='Set3') # 색상 테마 변경

plt.title('🎯 점유율 Top 10 브랜드의 "제품 1개당 평균 리뷰 수"', fontsize=16, pad=20)
plt.xlabel('브랜드명', fontsize=12)
plt.ylabel('평균 리뷰 수 (개)', fontsize=12)
plt.xticks(rotation=45)

# 숫자 텍스트 달아주기
offset = avg_review_brands.max() * 0.02 
for i, val in enumerate(avg_review_brands.values):
    plt.text(i, val + offset, f"{val:,.0f}개", ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()