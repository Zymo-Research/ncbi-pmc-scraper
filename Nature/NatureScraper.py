from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class NatureScraper:

    def __init__(self):
        self.base_url = "https://www.nature.com"
        self.search_url = "/search"
        self.query_parameter = "q"
        self.page_parameter = "page"
        self.login_btn = "c-article__button"
        self.__driver = webdriver.Chrome()
    
    def get_url(self, url):
        self.__driver.get(url)
    
    def __construct_search_url(self, search_term):
        full_url = f"{self.base_url}{self.search_url}?{self.query_parameter}={search_term}"
        self.__full_search_url = full_url
    
    def __get_max_page_number(self, search_term):
        self.__construct_search_url(search_term)
        self.get_url(self.__full_search_url)
        soup = BeautifulSoup(self.__driver.page_source, "html.parser")
        page_items = soup.find_all("li", {"class": "c-pagination__item"})
        pagination = [page.get('data-page') for page in page_items]
        integers = [int(i) for i in pagination if isinstance(i, str) and i.isdigit()]
        max_page_number = max(integers) if integers else 1
        return max_page_number

    def get_article_links(self, search_term):
        max_page_number = self.__get_max_page_number(search_term)
        all_links = []
        for i in range(1, max_page_number):
            page_url = f"{self.__full_search_url}&{self.page_parameter}={i}"
            self.get_url(page_url)
            time.sleep(1)
            soup = BeautifulSoup(self.__driver.page_source, "html.parser")
            articles = soup.find_all("li", {"class": "app-article-list-row__item"})
            headers = [article.find("h3", {"class": "c-card__title"}) for article in articles]
            links = [link.find("a")['href'] for link in headers]
            full_links = [f"{self.base_url}{link}" for link in links]
            all_links.extend(full_links)
        return all_links

    def get_full_articles(self, article_links):
        method_sections = []
        for article in article_links:
            self.get_url(article)
            time.sleep(1)
            soup = BeautifulSoup(self.__driver.page_source, "html.parser")
            sections = soup.find_all("div", {"class": "c-article-section"})
            methods = []
            for section in sections:
                section_titles = section.find_all("h2")
                method_sections = [title for title in section_titles if "method" in title.text.lower()]
                if method_sections:
                    methods.append(section.text)
            method_sections.append(" ".join(methods))
            print(method_sections)
        return method_sections

    def close_driver(self):
        self.__driver.quit()

