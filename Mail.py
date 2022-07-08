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

def separator(content: list):
    """Функция отбирает из ссылок только те, которые содержат в себе новости"""
    news_list = []
    for line in content:
        *args, id = line.split('/')
        if id.isdigit():
            news_list.append(line)
    print(f'{len(news_list)} id отобраны для включения в итоговый файл')
    return news_list



list_of_url = ['https://www.khabkrai.ru/events/news/events/news/191136', 'https://www.khabkrai.ru/events/news/events/news/191117', 'https://www.khabkrai.ru/events/news/events/video/191131']

for link in list_of_url:
    #html_content = page_open(link, headers)
    #print(BeautifulSoup(html_content, 'lxml'))
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(link)
    try:
        date = driver.find_element(By.CLASS_NAME, 'data-item').text

    except Exception as e: print(e)


"""
Распарсить все ссылки
Выделить в каждой id из ссылки, 
дату class="material-date data-item"
Заголовок <h1> и class wrapper
Текст <p>
и ссылку

Результаты представить в виде кортежа id, data, head, next, link

Из всей выборки взят те у которых дата равна 

"""


