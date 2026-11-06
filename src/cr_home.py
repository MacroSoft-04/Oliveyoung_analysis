from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# when you remove comment it'll run on background whithout brower window

print("run chrom browser...")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

all_data = []
global_rank = 1

for page in range(1, 14):
    print(f"\n📄 {page}페이지 수집 중...", end="")

    url = f"https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100020006&fltDispCatNo=&prdSort=01&pageIdx={page}&rowsPerPage=24"
    driver.get(url)

    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    items = soup.select("div.prd_info")

    if not items:
        print(" -> 상품이 없습니다. 수집을 종료합니다.")
        break

    print(f" -> {len(items)}개 발견!", end="")

    for item in items:
        try:
            a_tag = item.select_one("a.prd_thumb")

            if a_tag and "data-ref-goodsno" in a_tag.attrs:
                goods_no = a_tag["data-ref-goodsno"]
                clean_url = f"https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo={goods_no}"

                name_tag = item.select_one(".tx_name")
                name = name_tag.text.strip() if name_tag else "이름모름"

                all_data.append(
                    {
                        "랭킹": global_rank,
                        "상품명": name,
                        "상품ID": goods_no,
                        "상세URL": clean_url,
                    }
                )

                global_rank += 1

        except Exception as e:
            print(f"\n에러 발생: {e}")
            continue

    time.sleep(random.uniform(1, 2))

driver.quit()

df = pd.DataFrame(all_data)
print("\n\n-----------------------")
print(f"총 {len(df)}개의 상품 데이터를 수집했습니다.")
print(df.head())
print("-----------------------")

if len(df) > 0:
    df.to_csv("oliveyoung_lip_list_all_pages.csv", index=False, encoding="utf-8-sig")
    print("save 'oliveyoung_lip_list_all_pages.csv'")
