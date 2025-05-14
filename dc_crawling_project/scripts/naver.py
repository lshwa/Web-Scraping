import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://finance.naver.com/item/board.nhn?code=005930&page={}"
titles, writers, views, likes, dates = [], [], [], [], []

for page in range(1, 11):  # 1~10페이지
    url = base_url.format(page)
    print(f"📄 {page}페이지 요청 중...")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'euc-kr'  # 네이버 금융은 euc-kr 인코딩 사용
    soup = BeautifulSoup(res.text, 'html.parser')

    rows = soup.select("table.type2 tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 6:
            continue  # 게시글 row만 추출

        try:
            title = cols[1].get_text(strip=True)
            writer = cols[2].get_text(strip=True)
            view = cols[3].get_text(strip=True)
            like = cols[4].get_text(strip=True)
            date = cols[5].get_text(strip=True)

            titles.append(title)
            writers.append(writer)
            views.append(view)
            likes.append(like)
            dates.append(date)
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            continue

    time.sleep(1)

# 데이터 저장
df = pd.DataFrame({
    "title": titles,
    "writer": writers,
    "views": views,
    "likes": likes,
    "date": dates
})

df.to_csv("naver_samsung_board.csv", index=False, encoding='utf-8-sig')
print(f"✅ 저장 완료! 총 {len(df)}건 ➝ naver_samsung_board.csv")