from bs4 import BeautifulSoup
from selenium import webdriver


class BiospaceScraper:

    def __init__(self, employer_category):
        self.employer_cat = employer_category
        self.__base_url = f"https://www.biospace.com"
        self.__employer_page = f"/employers/{self.employer_cat}/"
        self.__driver = webdriver.Chrome()
        self.__company_elements = "lister__item cf block js-clickable"
        self.__start_page = 1
    
    def __get_last_pagination(self):
        full_url = f"{self.__base_url}{self.__employer_page}{self.__start_page}"
        self.__driver.get(full_url)
        soup = BeautifulSoup(self.__driver.page_source, "html.parser")
        paginator_items = soup.find_all("li", {"class": "paginator__item"})
        last_page = paginator_items[-1].find("a")["href"]
        last_page = last_page.replace(self.__employer_page, "").replace("/", "")
        return int(last_page)

    def get_company_names(self):
        last_page_number = self.__get_last_pagination()
        company_names_list = []
        for page in range(self.__start_page, last_page_number + 1):
            full_url = f"{self.__base_url}{self.__employer_page}{page}"
            self.__driver.get(full_url)
            print(f"Visited URL: {full_url}")
            soup = BeautifulSoup(self.__driver.page_source, "html.parser")
            company_items = soup.find_all("li", {"class": self.__company_elements})
            company_names = [company.find("a").text for company in company_items]
            company_names_list.append(company_names)
        return company_names_list

