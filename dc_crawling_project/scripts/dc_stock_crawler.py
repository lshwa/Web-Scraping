import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://gall.dcinside.com"
GALLERY_ID = "kospi"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_posts(page):
    url = f"{BASE_URL}/mgallery/board/lists/?id={GALLERY_ID}&page={page}"
    print(f"📄 {page}페이지 크롤링 중...")
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.select("tr.ub-content")
    post_data = []

    for row in rows:
        try:
            post_id = row.select_one("td.gall_num").text.strip()
            subject = row.select_one("td.gall_subject").text.strip()
            title_tag = row.select_one("td.gall_tit.ub-word a")
            title = title_tag.text.strip()
            link = BASE_URL + title_tag['href']
            writer = row.select_one("td.gall_writer").text.strip()
            date = row.select_one("td.gall_date").text.strip()
            views = row.select_one("td.gall_count").text.strip()
            recommends = row.select_one("td.gall_recommend").text.strip()

            post_data.append({
                "id": post_id,
                "subject": subject,
                "title": title,
                "writer": writer,
                "date": date,
                "views": views,
                "recommends": recommends,
                "link": link
            })
        except Exception as e:
            print(f"⚠️ 오류 발생: {e}")
            continue

    return post_data


# 전체 페이지 순회
all_posts = []
for page in range(1, 11):  # 1~10페이지
    posts = fetch_posts(page)
    all_posts.extend(posts)
    time.sleep(1)  # 서버 부하 방지

# CSV 저장
df = pd.DataFrame(all_posts)
df.to_csv("kospi_gallery_posts.csv", index=False, encoding='utf-8-sig')
print(f"\n✅ 총 {len(df)}건 크롤링 완료: kospi_gallery_posts.csv 저장됨")