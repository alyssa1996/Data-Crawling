
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import re
import time
import numpy as np
import csv

hyperlink=re.compile(r'.*ng-href="(.*)" target.*')
target=input("Enter a fishing keyword: ") #fishing keyword 입력요청
maxPages=input("Enter the maximum page number of this websites for crawling") #크롤링 몇페이지까지 읽을 지 페이지수 요청

maintitle=re.compile(r'ng-bind-html="post.title">(.*)</span>.*')#변경해야할 부분 maintitle 위치
Field2RE=re.compile(r'<em class="name_author">(.*)</em>.*')#변경해야할 부분 Field2 위치
Field3RE=re.compile(r'ng-if="post.contents" target="_blank">(.*)</a>.*') #변경해야할 부분 Field3 위치

driver=webdriver.Chrome("C:/Users/JisuPark/Desktop/Programming/chromedriver")
driver.set_window_size(1120,800)
driver.get("https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword="+target)
time.sleep(3)
isFinished=False
row=1

with open('CrawledText.csv','w',newline="") as f:
    writer=csv.writer(f)
    writer.writerow(['Field1','Field2','Field3']) #저장 화일의 칼럼별 해당 변수 지정
    while not isFinished:
        for page in range(int(maxPages)):
            actualPage=str(page+1)
            print("Viewing Page N"+actualPage)
            driver.get("https://section.blog.naver.com/Search/Post.nhn?pageNo="+actualPage+"&rangeType=ALL&orderBy=sim&keyword="+target)

            time.sleep(5)
            soup=BeautifulSoup(driver.page_source,"html.parser")
            """가져온 소스코드 중 특정 메시지 1건 잘라오기
            이 내용은 각각 div class=""형태로 구성되고 이때 원하는 내용의 소스에서 ""에
            해당하는 내용을 이용해 찾을 수 있다.
            네이버는 list_search_post임(이것도 직접 네이버에서 소스코드 보고 확인해야함)
            소스코드에서 원하는 곳 커서로 찾고 해당 소스코드에서 <div class의 "..." 부분을
            아래 list_search_post에 교체할 것"""
            link=soup.find_all("div",{"class":"list_search_post"})
        #해당하는 글 시작 부분 상응하는 전체 클라스 "list_search_pot"안의 내용을 find_all로 찾아 link에 넣기
            for posts in link:
                time.sleep(0.33)
                z=str(posts)
                url=hyperlink.search(z).group(1).strip()
                Field1=maintitle.search(z).group(1).strip()
            #검색 키워드가 bold 처리되어있으면 소스코드에 strong 표시 나오는데 이것 제거
                if '<strong class="search_keyword">' in Field1:
                    m=re.search(r'(.*)<strong class="search_keyword">(.*)</strong>(.*)',Field1)
                    Field1=m.group(1)+m.group(2)+m.group(3)

                introURL=urllib.request.urlopen(url)
                soupURL=BeautifulSoup(introURL, "html.parser")
                linkURL=soupURL.find_all("span",{"class":"title"})
            #소스코드 보고 제목 부분이 <span class ="title" ng..="post.title" 나오는 부분인 경우
            # TITLE을 넣은 것. 이것 변형해야 함. 다음은 TIT)
                Field2=Field2RE.search(z).group(1).strip()
                Field3=Field3RE.search(z).group(1).strip()
                if '<strong class="search_keyword">' in Field3:
                    m=re.search(r'(.*)<strong class="search_keyword">(.*)</strong>(.*)',Field3)
                    Field3=m.group(1)+m.group(2)+m.group(3)
            #변경할 것 4,5번째 항목 넣을려면 위에서 범위 지정 부분 넣고 여기에서 추가하면 됨"

                information=[Field1,Field2,Field3]
                print(Field1)
                print(Field2)
                print(Field3)
                try:
                    writer.writerow(information)
                except UnicodeEncodeError:
                    pass
        isFinished=True
