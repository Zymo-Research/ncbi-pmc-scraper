from PubMed.PmcScraper import PmcScraper
import os

# need .env file to store ncbi api key
pmc_scraper = PmcScraper(os.environ['NCBI_API_KEY'])

# search based on keyword and retrieve the desired amount of articles
search_results = pmc_scraper.search_pmc(search_term="gut microbiota", number_of_articles=2)

# extract the full text version of articles using pmcids
full_text_articles = pmc_scraper.fetch_full_text(search_results['esearchresult']['idlist'])

# extract the desired section of articles
method_sections = pmc_scraper.extract_section(full_text_articles, 'method')

# print as dictionary
method_dict = dict(zip(search_results['esearchresult']['idlist'], method_sections))
print(method_dict)
