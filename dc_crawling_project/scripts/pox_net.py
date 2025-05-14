from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. 셀레니움 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 창 없이 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 2. 크롤링할 페이지 범위 설정
base_url = "https://www.paxnet.co.kr/tbbs/list?tbbsType=L&id=N11023&page={}"
titles, writers, views, likes, dates = [], [], [], [], []

# 3. 페이지 순회
for page in range(1, 11):
    url = base_url.format(page)
    print(f"📄 {page}페이지 크롤링 중...")
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    posts = soup.select("ul#comm-list li")  # 각 게시글은 li로 시작

    for post in posts:
        try:
            title = post.select_one("div.title")
            writer = post.select_one("div.write")
            view = post.select_one("div.viewer")
            like = post.select_one("div.like")
            date = post.select_one("div.date")

            # None 체크
            if None in (title, writer, view, like, date):
                continue

            titles.append(title.text.strip())
            writers.append(writer.text.strip())
            views.append(view.text.strip())
            likes.append(like.text.strip())
            dates.append(date.text.strip())

        except Exception as e:
            print(f"❌ 파싱 오류: {e}")
            continue

# 4. 종료 및 저장
driver.quit()

df = pd.DataFrame({
    "title": titles,
    "writer": writers,
    "views": views,
    "likes": likes,
    "date": dates
})
df.to_csv("paxnet_posts.csv", index=False, encoding='utf-8-sig')
print(f"✅ 크롤링 완료: {len(df)}건 ➝ paxnet_posts.csv 저장됨")