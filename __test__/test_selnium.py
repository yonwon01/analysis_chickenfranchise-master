import time
from selenium import webdriver

wd = webdriver.Chrome('D:/Python/webdriver/chromedriver.exe')
wd.get("http://www.goobne.co.kr/store/search_store.jsp")
time.sleep(5)

html = wd.page_source
wd.quit()

print(html)
