import requests
from urllib.request import urlopen
from urllib.response import addinfourl
import urllib
from bs4 import BeautifulSoup
import re
from fake_user_agent.main import user_agent
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import functional
from datetime import date
import re

"""pip install -r requirements.txt"""

""" В текущий момент это очень тяжелый краулер, не предназначенный для скоростного поиска.
Он страшно жрет ресурсы оперативной памати, но при этом может уверено и методично переработать хоть весь сайт Правительства края, 
лищь бы хватило ресурсов у машины. Его не пустят в ПРОМ"""

URL = 'https://www.khabkrai.ru/events/news' #В качестве URL передаем ссылку на страницу новостей Правительства края
user_agent = user_agent("chrome")
#Передаем в переменную headers значения юзерагента для
headers = {'accept': '*/*', 'user-agent': user_agent}

def page_open(url: str, headers: str,  iterations: int = 1):
    """Функция принимает в себя адрес и заголовки, обращается к вэб странице,
    установленное количество раз нажимает кнопку "Загружить еще",
    извлекает контент в html файл"""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        """Применение опции открытия браузера в фоновом режиме"""
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)

        """Открытие страницы в режиме реального времени"""
        #driver = webdriver.Chrome()#Открытие страницы вживую
        #driver.get(url) #Открытие страницы вживую
        #time.sleep(5)

        while iterations >= 1:
            # Находим кнопку "Загрузить еще и нажимаем требуемое число итераций"
            try:
                driver.find_element(By.ID, 'ajax_paginator_btn').click()
                print("Нажата кнопка 'Загрузить еще' ")
                # Ожидание прогрузки страницы
                time.sleep(5)
            except: pass
            iterations -= 1
        html_content = driver.page_source
        return html_content

def parse_pages(url: str, headers: str,  iterations: int) -> list:
    """Функция принимает в себя адрес и заголовки
    на странице ссылки и возвращает список ссылок"""
    Links = []
    html_content = page_open(url, headers, iterations)
    soup = BeautifulSoup(html_content, 'lxml')
    #регулярным выражением ищем все ссылки в html и собираем их по сайту
    for link in soup.find_all('a', href=re.compile('^(/|.*' + url + '/[0-9])')):
        if link.attrs['href'] is not None:

            if link.attrs['href'] not in Links:
                if link.attrs['href'].startswith('/'):
                    Links.append(url + link.attrs['href'])
                else:
                    Links.append(link.attrs['href'])
        else:
            print("Connection Error")
    print(f"Обнаружено {len(Links)} ссылок")
    return list(set(Links))

def parse_content(content: str):
    """Функция принимает в себя контент достает ссылки"""
    #регулярным выражением ищем все ссылки в html и собираем их по сайту
    list_of_links = []
    links = content.find_all(re.compile('\/events\/news\/[0-9]*')) # нужно сделать это выражение не жадным
    print(links)


year,month,day = str(date.today()).split("-")
today = f'{day}.{month}.{year}'
print(f'Сегодня {today}')
html_content = page_open(URL, headers, 3)
today = '08.07.2022'

begin_index = html_content.find('date-splitter')
end_index = html_content.find('date-splitter', begin_index+1)
html_content = html_content[begin_index : end_index]
print(parse_content(html_content))


