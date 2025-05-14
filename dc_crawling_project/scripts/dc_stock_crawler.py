from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

# 저장 리스트 초기화
post_ids, titles, contents, dates = [], [], [], []

# 셀레니움 드라이버 설정
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 기본 설정
BASE = "https://gall.dcinside.com"
GALLERY = "neostock"

# 3~5페이지만 순회
for page in range(3, 6):
    url = f"{BASE}/board/lists/?id={GALLERY}&page={page}"
    print(f"🔎 {page}페이지 요청 중...")

    try:
        driver.get(url)
        sleep(2)
    except:
        print("🚫 페이지 로드 실패")
        continue

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.select("tbody tr.us-post")

    for row in articles:
        try:
            # 공지/AD 제외
            subject = row.select_one("td.gall_subject")
            if subject and subject.get_text(strip=True) in ["공지", "설문", "AD"]:
                continue

            post_id = row.select_one("td.gall_num").get_text(strip=True)
            title_tag = row.select_one("a.title_us")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            href = BASE + title_tag['href']

            # 날짜
            date_tag = row.select_one("td.gall_date")
            date_raw = date_tag.get("title") or date_tag.get_text(strip=True)

            # 본문 크롤링
            try:
                driver.get(href)
                sleep(1)
                post_soup = BeautifulSoup(driver.page_source, 'html.parser')
                content_div = post_soup.select_one("div.write_div")
                content = content_div.get_text(strip=True) if content_div else ""
            except:
                content = ""

            # 저장
            post_ids.append(post_id)
            titles.append(title)
            contents.append(content)
            dates.append(date_raw)

            # 출력 디버깅
            print(f"✅ {title} | {date_raw}")

        except Exception as e:
            print(f"⚠️ 게시글 오류: {e}")
            continue

# 저장
df = pd.DataFrame({
    "id": post_ids,
    "title": titles,
    "content": contents,
    "date": dates
})
df.to_csv("sample_stock_posts.csv", index=False, encoding='utf-8-sig')

print(f"\n📦 총 {len(df)}건 저장됨 ➝ sample_stock_posts.csv")
driver.quit()