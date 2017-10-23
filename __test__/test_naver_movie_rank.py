# 네이버 영화 랭킹 정보 크롤링
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

request = Request('http://movie.naver.com/movie/sdb/rank/rmovie.nhn')
resp = urlopen(request)
html = resp.read().decode('cp949')

bs = BeautifulSoup(html, 'html.parser')
# print(bs.prettify())

tags_div = bs.findAll('div', attrs={'class': 'tit3'})
for index, tag_div in enumerate(tags_div):
    print(index+1, tag_div.a.text, tag_div.a['href'], sep=' : ')