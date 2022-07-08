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
    print(f'{len(news_list)} ссылок отобраны для включения в итоговый список')
    return news_list

def news_parser(link):
    """Функция принимает в себя ссылку, извлекает id, ищет и преобразует дату, ищет заголовок и текст"""
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


today = f'{date.today()}'

links = parse_pages(URL, headers, 1) #один раз мы прокручиваем страницу для увеличения выборки сайта
news_links = separator(links)
result = [news_parser(link) for link in news_links[:10]] # Ограничимся ВЫБОРКОЙ В 10 СТРАНИЦ

# Печатает с новой строки только те записи, в которых день совпадает с текущим днем
for row in result:
    if row[1]==today:
        print(row)
