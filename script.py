from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

def parser(articles):
    "Extract articles info"
    findart = soup_level1.findAll('div',{'class':'gs_r gs_or gs_scl'})
    Artlist = []
    for article in findart:
        Article = {}
        is_other_url = article.find('div',{'class':"gs_or_ggsm"}) is not None
        if is_other_url:
            Article['other_url'] = article.find('div',{'class':"gs_or_ggsm"}).find('a')['href']
        else:
            Article['other_url'] = ''
        Article['article_title'] = article.find('h3',{'class':"gs_rt"}).text
        Article['article_url'] = article.find('h3',{'class':"gs_rt"}).find('a')['href']
        Article['article_authors'] =";".join(["%s:%s"%(a.text,a['href']) for a in article.find('div',{'class':"gs_a"}).findAll('a')])
        Article['article_summary'] = article.find('div',{'class':"gs_rs"}).text
        stats = article.findAll('div',{'class':"gs_fl"})[-1].findAll('a')
        for a in stats:
            if a.text != '':
                if a.text.startswith('Cited'):
                    Article['article_cited_count'] = a.text.rstrip().split()[-1]
                    Article['article_cited_url'] = a['href']
                if a.text.startswith('Related'):
                    Article['article__Related_articles_url'] = a['href']
                if a.text.startswith('All'):
                    Article['article_goog_versions'] = a.text.rstrip().split()[1]
                    Article['article_goog_versions_url'] = a['href']
                if a.text.startswith('Import'):
                    Article['article_bibtex_url'] = a['href']
        Artlist.append(Article)
    
    return Artlist
 
def next_page(file_name):
    "To scrap next page"
    art = parser(BeautifulSoup(driver.page_source,'lxml'))
    pd.DataFrame(art).to_csv('%s.csv'%file_name)
    nxt =[i for i in driver.find_elements_by_tag_name('button') if  i.get_attribute('aria-label')=='Next']
    bnext = nxt[0]
    bnext.click()
    return x 

def Search(query,file_name):
    "Enter query and file_name to store articles"
    url = "https://scholar.google.com/"
    driver.get(url)
    #After opening the url above
    search = driver.find_element_by_name('q')
    # Search query
    search.send_keys(query)
    search.submit()
    art = parser(BeautifulSoup(driver.page_source,'lxml'))
    df = pd.DataFrame(art)
    df.to_csv('%s.csv'%file_name)
    df.head()
 
# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)

if __name__ == '__main__':
    Search('Enstein','p1')
    # if page 2  needed
    #next_page('p2')
