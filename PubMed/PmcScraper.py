from bs4 import BeautifulSoup
import requests
import re


class PmcScraper:

    def __init__(self, api_key):
        self.__api_key = api_key
    
    def search_pmc(self, search_term, number_of_articles):
        """
        Method that takes in a search term and number of articles as inputs and
        then returns ncbi eutils request in json format.
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            'db': 'pmc',
            'term': search_term,
            'retmax': number_of_articles,
            'usehistory': 'y',
            'retmode': 'json',
            'api_key': self.__api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.json()

    def fetch_full_text(self, list_of_pmc_ids):
        """
        Provided a list of pmcids, this method returns the full text of articles
        in xml format.
        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            'db': 'pmc',
            'retmode': 'xml',
            'id': list_of_pmc_ids,
            'api_key': self.__api_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            return response.text

    def extract_section(self, full_text_articles, section_to_extract):
        """
        Method that extracts a certain section of articles, given that the full
        text article and sections names are provided as inputs.
        """
        section_text_list = []
        soup = BeautifulSoup(full_text_articles, 'lxml-xml')
        articles = soup.find_all("article")
        for article in articles:
            all_sections_of_article = article.find_all("sec")
            for section in all_sections_of_article:
                section_title = section.find("title").text.lower()
                if section_title:
                    if section_to_extract in section_title:
                        text = section.text
                        text = re.sub(r'\s+', ' ', text).strip()
                        section_text_list.append(text)
        return section_text_list
