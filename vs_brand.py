import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# ---------------------------------------------------
# [필수] 한글 폰트 깨짐 방지 설정
# ---------------------------------------------------
if platform.system() == 'Darwin':  # Mac 사용자
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows 사용자
    plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False) # 마이너스 기호 깨짐 방지

# ---------------------------------------------------
# 1. 데이터 불러오기
# ---------------------------------------------------
# 할인율까지 추가하셨던 최종 파일을 불러옵니다.
df = pd.read_csv("oliveyoung_lip_2.10.csv")

# 2. 브랜드별 상품 개수 세기 (상위 10개만 추출)
# value_counts()는 기본적으로 개수가 많은 순서대로 내림차순 정렬해줍니다.
top_brands = df['브랜드'].value_counts().head(10)

# ---------------------------------------------------
# 3. 막대 그래프 그리기
# ---------------------------------------------------
plt.figure(figsize=(12, 6)) # 그래프 크기 설정 (가로 12, 세로 6)

# seaborn을 이용해 막대 그래프 그리기 (보기 좋은 색상 테마 적용)
sns.barplot(x=top_brands.index, y=top_brands.values, palette='Set2')

# 4. 그래프 디테일 꾸미기
plt.title('💄 올리브영 립 메이크업 Top 300 점유율 (상위 10개 브랜드)', fontsize=16, pad=20)
plt.xlabel('브랜드명', fontsize=12)
plt.ylabel('랭킹에 진입한 상품 개수 (개)', fontsize=12)
plt.xticks(rotation=45) # 브랜드명이 길면 겹치니까 45도 기울여서 표시

# 🌟 꿀팁: 막대기 위에 정확한 숫자(개수) 적어주기
for i, count in enumerate(top_brands.values):
    plt.text(i, count + 0.3, f"{count}개", ha='center', fontsize=11, fontweight='bold')

# 여백을 깔끔하게 자동 조정 후 화면에 띄우기
plt.tight_layout()
plt.show()