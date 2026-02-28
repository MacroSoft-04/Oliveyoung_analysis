import pandas as pd

# 1. 방금 수집한 파일 불러오기
df = pd.read_csv("oliveyoung_lip_2.10.csv")

# 2. 할인율 계산 (정가가 0보다 클 때만 계산, 소수점 1자리까지 깔끔하게 반올림)
df['할인율(%)'] = df.apply(lambda x: round((x['정가'] - x['판매가']) / x['정가'] * 100, 1) if x['정가'] > 0 else 0, axis=1)

# 3. 같은 이름으로 덮어쓰기 저장
df.to_csv("oliveyoung_lip_2.10.csv", index=False, encoding="utf-8-sig")
print("✅ 할인율 컬럼 장착 완료! 데이터 확인해보세요.")