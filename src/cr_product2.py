from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

# =========================================================
# 1. CSV 파일 불러오기
# =========================================================
print("📂 'oliveyoung_lip_list_all_pages.csv' 파일을 읽어옵니다...")
try:
    df = pd.read_csv("oliveyoung_lip_list_all_pages.csv")
    df = df.dropna(subset=['상품ID']) 
    print(f"✅ 총 {len(df)}개의 상품을 수집합니다.")
except:
    print("❌ 파일을 찾을 수 없습니다.")
    exit()

# =========================================================
# 2. 브라우저 실행 (Selenium) - 이게 해결사입니다!
# =========================================================
print("🚀 크롬 브라우저를 실행합니다... (차단 우회)")
options = webdriver.ChromeOptions()
# options.add_argument("--headless") # 창 안 보고 싶으면 주석 해제
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

final_data = []

# =========================================================
# 3. 한 땀 한 땀 방문해서 긁어오기
# =========================================================
for index, row in df.iterrows():
    try:
        rank = row['랭킹']
        goods_id = str(row['상품ID'])
        
        # 🌟 질문자님이 원하시던 '트래킹 코드 포함 URL' (Selenium은 이걸 소화해냅니다)
        # 굳이 params 안 쓰고 f-string으로 박아도 브라우저라 괜찮습니다.
        target_url = f"https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo={goods_id}&dispCatNo=100000100020006&trackingCd=Cat100000100020006_MID"
        
        # 진행상황 출력
        if (index + 1) % 5 == 0:
            print(f"[{index+1}/{len(df)}] {rank}위 제품 수집 중...", end='\r')

        # 브라우저로 이동
        driver.get(target_url)
        
        # ⚠️ 페이지 로딩 기다리기 (필수!)
        time.sleep(1.5) 
        
        # HTML 가져오기 (requests.text 대신 driver.page_source 사용)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # --- [데이터 추출] ---
        # 1. 브랜드
        brand_tag = soup.select_one("button[class*='TopUtils_btn-brand']")
        brand = brand_tag.text.strip() if brand_tag else row.get('브랜드', '')

        # 2. 상품명
        name_tag = soup.select_one("[data-qa-name='text-product-title']")
        if name_tag:
            name = name_tag.text.strip()
        else:
            title_tag = soup.select_one("div[class*='GoodsDetailInfo_title']")
            name = title_tag.get_text(strip=True) if title_tag else row.get('상품명', '')

        # 3. 가격
        sale_tag = soup.select_one("[data-qa-name='text-product-discount-price']")
        if not sale_tag: sale_tag = soup.select_one(".price_2 strong")
        sale_price = int(re.sub(r'[^0-9]', '', sale_tag.text)) if sale_tag else 0

        org_tag = soup.select_one("[data-qa-name='text-product-original-price']")
        org_price = int(re.sub(r'[^0-9]', '', org_tag.text)) if org_tag else sale_price

        # 4. 별점
        rating = 0.0
        rating_tag = soup.select_one(".rating")
        if rating_tag:
            txt = re.sub(r'[^0-9.]', '', rating_tag.text)
            if txt: rating = float(txt)

        # 5. 리뷰 수
        review_cnt = 0
        review_btn = soup.select_one("button[class*='ReviewArea_btn-review']")
        if review_btn:
            txt = re.sub(r'[^0-9]', '', review_btn.text)
            if txt: review_cnt = int(txt)

        final_data.append({
            "랭킹": rank,
            "브랜드": brand,
            "상품명": name,
            "정가": org_price,
            "판매가": sale_price,
            "별점": rating,
            "리뷰수": review_cnt,
            "상세URL": target_url
        })
        
        # 너무 빠르면 기계인 줄 아니까 랜덤 휴식
        time.sleep(random.uniform(0.5, 1.0))

    except Exception as e:
        print(f"\n⚠️ 에러 ({rank}위): {e}")
        continue

driver.quit()

# 저장
print("\n🎉 드디어 성공! 수집 완료!")
df_final = pd.DataFrame(final_data)
df_final.to_csv("oliveyoung_lip_final_selenium.csv", index=False, encoding="utf-8-sig")
print("✅ 'oliveyoung_lip_final_selenium.csv' 저장되었습니다.")