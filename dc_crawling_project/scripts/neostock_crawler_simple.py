from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

# 저장 리스트 초기화
post_ids, titles, writers, dates = [], [], [], []

# 셀레니움 드라이버 설정
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 페이지 순회 (1~10페이지)
BASE = "https://gall.dcinside.com"
GALLERY = "neostock"

for page in range(1, 20):
    url = f"{BASE}/board/lists/?id={GALLERY}&page={page}"
    print(f"\U0001F50D {page}페이지 요청 중...")
    try:
        driver.get(url)
        sleep(2)
    except:
        print(" 페이지 로드 실패"); break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.select('tr.ub-content.us-post')  

    print(f"{len(articles)}개 게시글 탐지됨")

    for row in articles:
        try:
            post_id = row.get("data-no")
            title_tag = row.select_one("td.gall_tit a")
            title = title_tag.text.strip()
            writer = row.select_one("td.gall_writer").get("data-nick") or "익명"
            date = row.select_one("td.gall_date").get("title") or row.select_one("td.gall_date").text.strip()

            post_ids.append(post_id)
            titles.append(title)
            writers.append(writer)
            dates.append(date)
        except Exception as e:
            print(f" 게시글 파싱 실패: {e}")
            continue

# 저장
df = pd.DataFrame({
    "id": post_ids,
    "title": titles,
    "writer": writers,
    "date": dates
})
df.to_csv("../data/neostock_posts.csv", index=False, encoding='utf-8-sig')

print(f"저장 완료! 총 {len(df)}건 ➝ neostock_posts.csv")
driver.quit()