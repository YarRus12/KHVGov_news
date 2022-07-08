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

"""Это очень легкий и достаточно быстрый скраппер. Он вытаскивает всю html разметку
Находим блок инфомрации между заданной датой и предыдущим тегом о дате
Ищет все вхождения ссылок и распарсевает их"""

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

def parse_content(content: str):
    """Функция принимает в себя контент достает ссылки"""
    #регулярным выражением ищем все ссылки в html и собираем их по сайту
    list_of_links = []
    links = re.findall('/events/news/[0-9]*', html_content)
    for link in links:
        list_of_links.append('https://www.khabkrai.ru'+link)
    return list_of_links

def news_parser(link):
    """Функция принимает в себя ссылку, извлекает id, ищет и преобразует дату, ищет заголовок и текст
    и Возвращает кортеж из указанных значений"""
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(link)
    try:
        *args, id = link.split('/')
        date = driver.find_element(By.CLASS_NAME, 'data-item').text
        date_l = functional.change_date(date)
        # заголовок ищется двумя методами
        try:
            head = driver.find_element(By.CSS_SELECTOR, 'body > div.main-wrapper > div.content.main.standart_shablons__news_detail > div > div > div.content-block > h1 > span').text
        except:
            try:
                head = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/h1/text()').text
            except: head = 'Заголовок не найден'
        try:
            #page_text = driver.find_element(BY.CLASS_NAME, 'content-text').text
            page_text = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div/div[2]/div[4]').text # Это самый нестабильный способ, но только он сработал
        except: page_text = 'На странице не обнаружен текст'
    except Exception as e: print(e)
    print(f'Страница распарсена')
    return id, date_l, head, page_text

year,month,day = str(date.today()).split("-")
today = f'{day}.{month}.{year}'
print(f'Сегодня {today}')
html_content = page_open(URL, headers, 1)
#today = '08.07.2022'

begin_index = html_content.find(today)
end_index = html_content.find('date-splitter', begin_index+1)
html_content = html_content[begin_index : end_index]
list_of_links = set(parse_content(html_content))
print(f'В рассматриваемом разделе обнаружены {len(list_of_links)} новостных ссылок')
result = [news_parser(link) for link in list_of_links] # Ограничимся ВЫБОРКОЙ В 10 СТРАНИЦ

for row in result:
    print(row)
