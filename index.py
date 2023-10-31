from bs4 import BeautifulSoup
import requests
import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get("https://programmers.co.kr/learn/challenges?tab=all_challenges")

baseURL = "https://programmers.co.kr"

# 0. 언어를 선택한다.
browser.find_element(By.XPATH, '//span[text()="JavaScript"]').click()

# 1. 코테 문제를 저장할 파일
with open("programmers.json", "w", encoding="utf-8") as f:

    data = []

    # 2. level 1부터 시작해서 5까지 클릭하기
    for level in range(1, 6):
        # print("level : "+str(level))
        browser.find_element(
            By.XPATH, '//span[text()="Level '+str(level)+'"]').click()
        time.sleep(3)  # 언어와 레벨에 따른 문제가 로딩되기를 기다린다.

        soup = BeautifulSoup(browser.page_source, "lxml")
        parent = soup.find("div", attrs={"class": "algorithm-list"})

        pages = []
        for child in parent.find_all("ul", attrs={"class": "pagination"}):
            pages = child.text.split(' ')
            # print(child.text)

        total_pages = len(pages)-2

        if total_pages == -2:  # pages = 0 인 경우, page가 1 페이지라서 해당 코드 추가 해줘야 함
            total_pages = 1
        # print("total_pages : "+str(total_pages))

        # 3. 페이지별로 문제 가져오기
        for i in range(1, total_pages+1):
            # print("now Page : "+str(i))
            soup = BeautifulSoup(browser.page_source, "lxml")
            parent = soup.find("div", attrs={"class": "algorithm-list"})

            # 해당 페이지의 모든 문제 가져오기
            for child in parent.find_all("div", attrs={"class": "col-item"}):
                data.append({"Level": level, "Title": child.h4.get_text(),
                             "Url": child.a["href"]})
                # print(baseURL+child.a["href"])
                # print(child.h4.get_text())

            # 다음 페이지로 이동
            if i+1 <= total_pages:
                # print("i+1 :" + str(i+1))
                # print("total_pages :" + str(total_pages))
                btn_next_page = browser.find_element(
                    By.XPATH, '//a[text()="'+str(i+1)+'"]')
                # print("btn_next_page : "+btn_next_page.text)
                btn_next_page.click()
                time.sleep(3) # 프로그래머스 페이지 로드 자체가 느려서, 해당 html을 못 읽어오는 오류를 해결하기 위해  각 페이지마다 3초의 텀을 둠

        # 다음 레벨의 문제만 얻기 위해, 현재 레벨 취소 선택
        browser.find_element(
            By.XPATH, '//span[text()="Level '+str(level)+'"]').click()

    # 4. 최종 결과물 json 파일에 저장
    json.dump(data, f, ensure_ascii=False, indent=2)
