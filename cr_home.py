from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# 1. 브라우저 옵션 설정 (사람인 척 하기)
options = webdriver.ChromeOptions()
# options.add_argument("--headless") # 이 줄 주석을 풀면 브라우저 창이 안 뜨고 백그라운드에서 돕니다.

# 2. 브라우저 열기 (자동으로 크롬 드라이버 설치해서 실행함)
print("🚀 크롬 브라우저를 실행합니다...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_data = [] # 모든 페이지의 데이터를 모을 리스트
global_rank = 1 # 페이지가 넘어가도 계속 숫자가 올라갈 랭킹 변수

for page in range(1, 14):
    print(f"\n📄 {page}페이지 수집 중...", end="")
    # 3. 올리브영 페이지 접속
    url = f"https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100020006&fltDispCatNo=&prdSort=01&pageIdx={page}&rowsPerPage=24"
    driver.get(url)

    # 4. 자바스크립트가 상품을 다 불러올 때까지 3초 정도 기다려줌 (가장 중요!!)
    time.sleep(3) 

    # 5. 로딩이 끝난 현재 페이지의 HTML을 가져옴
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 6. 이제 질문자님이 원하시던 'div.prd_info'를 찾아봅니다.
    items = soup.select("div.prd_info")
    
    if not items:
        print(" -> 상품이 없습니다. 수집을 종료합니다.")
        break

    print(f" -> {len(items)}개 발견!", end="")

    for item in items:
        try:
            # a 태그 찾기 (prd_thumb 클래스가 있는 a 태그)
            a_tag = item.select_one("a.prd_thumb")
            
            if a_tag and 'data-ref-goodsno' in a_tag.attrs:
                goods_no = a_tag['data-ref-goodsno']
                clean_url = f"https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo={goods_no}"
                
                # 상품명도 한번 가져와 볼까요? (선택)
                name_tag = item.select_one(".tx_name")
                name = name_tag.text.strip() if name_tag else "이름모름"

                all_data.append({
                    "랭킹": global_rank,
                    "상품명": name,
                    "상품ID": goods_no,
                    "상세URL": clean_url
                })
                
                global_rank += 1

        except Exception as e:
            print(f"\n에러 발생: {e}")
            continue

    time.sleep(random.uniform(1, 2))

# 브라우저 닫기
driver.quit()

# 결과 확인
df = pd.DataFrame(all_data)
print("\n\n-----------------------")
print(f"총 {len(df)}개의 상품 데이터를 수집했습니다.")
print(df.head())
print("-----------------------")

if len(df) > 0:
    df.to_csv("oliveyoung_lip_list_all_pages.csv", index=False, encoding="utf-8-sig")
    print("✅ 'oliveyoung_lip_list_all_pages.csv' 저장 완료!")