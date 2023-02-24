from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import re


def Search_careerjunction(search_term):
    """
    Searches careerjunctions website for matching search criteria
    """
    page_number = 1
    results = []
    base_url = "https://www.careerjunction.co.za"
    #headers = {"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"}
    page = requests.get(f"{base_url}/jobs/results?keywords={search_term}&autosuggestEndpoint=%2fautosuggest&location=0&category=&btnSubmit=+&page={page_number}").text
    soup = BeautifulSoup(page, 'lxml')
    #total_pages = soup.find('ul', id='pagination').findChildren()[-3].text
    #while page_number < int(2):
    for job in soup.find_all('div', class_='module job-result'):
        items = {}
        items["title"] = job.find_all('a')[1].text + " @ " + job.find('h3').text.strip()
        link = base_url + job.find_all('a')[1].get('href').strip()
        details_page = requests.get(link).text
        details_soup = BeautifulSoup(details_page, 'lxml')
        #items["description"] = details_soup.find_all('div', class_="job-details")[1]
        digits = re.findall("[0-9]+", job.find_all('li', class_="expires")[0].text, flags=0)
        if digits != None:
            #add_days = (digits[0])
            add_days = 1
        else:
            add_days = 0
        items["closing_date"] = date.today() + timedelta(int(add_days))
        items["link"] = link.strip()
        results.append(items)
#page_number += 1
    #page = requests.get(f"{base_url}/jobs/results?keywords={search_term}&autosuggestEndpoint=%2fautosuggest&location=0&category=&btnSubmit=+&page={page_number}").text
    #soup = BeautifulSoup(page, 'lxml')
    
    return results
