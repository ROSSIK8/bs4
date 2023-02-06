import json

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_headers():
    headers = Headers(browser='firefox', os='windows')
    return headers.generate()

URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
response = requests.get(URL, headers=get_headers()).text
soup_1 = BeautifulSoup(response, 'lxml')

data = soup_1.find('div', class_="vacancy-serp-content")
vacancies = data.find_all('div', class_="serp-item")

suitable_vacancies = []
for item in vacancies:
    title = item.find('a', class_='serp-item__title').text
    link = item.find('a', class_='serp-item__title')['href']
    result = requests.get(link, headers=get_headers()).text
    soup_2 = BeautifulSoup(result, 'lxml')
    description = item.find('div', class_='g-user-content').text



    if 'Django' in description or 'django' in description or 'Flask' in description or 'flask' in description:
        company_town = item.find_all('div', class_="bloko-text")
        company = company_town[0].text.replace('\xa0', '')
        town = company_town[1].text.replace('\xa0', '')
        salary = soup_2.find('span', class_="bloko-header-section-2 bloko-header-section-2_lite").text.replace('\xa0', '')
        suitable_vacancies.append({title: [link, salary, company, town]})

if __name__ == '__main__':
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(suitable_vacancies, file, indent=4)


