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
# 1. 데이터 불러오기 및 전처리
# ---------------------------------------------------
df = pd.read_csv("oliveyoung_lip_2.10.csv")

# 🌟 [핵심 변경점] 
# 이전에는 value_counts()로 '상품의 개수'를 세었지만,
# 이번에는 groupby()를 써서 브랜드별로 '리뷰수'를 모두 더해줍니다(sum).
top_review_brands = df.groupby('브랜드')['리뷰수'].sum().sort_values(ascending=False).head(10)

# ---------------------------------------------------
# 2. 막대 그래프 그리기
# ---------------------------------------------------
plt.figure(figsize=(12, 6))

# 막대 그래프 생성 (이전과 동일한 Set2 색상 테마)
sns.barplot(x=top_review_brands.index, y=top_review_brands.values, palette='Set2')

# 그래프 디테일 꾸미기
plt.title('🏆 올리브영 립 메이크업 누적 리뷰 수 (상위 10개 브랜드)', fontsize=16, pad=20)
plt.xlabel('브랜드명', fontsize=12)
plt.ylabel('누적 리뷰 수 (개)', fontsize=12)
plt.xticks(rotation=45)

# 🌟 막대기 위에 정확한 숫자 적어주기 (리뷰 수는 단위가 크므로 콤마(,) 추가)
# 최고 높은 막대기 기준으로 텍스트 위치를 살짝 위로 띄움 (max 값의 2% 정도)
offset = top_review_brands.max() * 0.02 

for i, count in enumerate(top_review_brands.values):
    # {count:,.0f} 를 쓰면 100000 -> 100,000 처럼 천 단위 콤마가 예쁘게 찍힙니다.
    plt.text(i, count + offset, f"{count:,.0f}개", ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()