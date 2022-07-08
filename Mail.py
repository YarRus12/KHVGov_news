import requests
from urllib.request import urlopen
from urllib.response import addinfourl
import urllib
from bs4 import BeautifulSoup
import re
from fake_user_agent.main import user_agent
import selenium
from selenium import webdriver
import time
from selenium import webdriver

months = {1: 'января',
          2: 'февраля',
          3: 'марта',
          4: 'апреля',
          5: 'мая',
          6: 'июня',
          7: 'июля',
          8: 'августа',
          9: 'сентября',
          10: 'октября',
          11: 'ноября',
          12: 'декабря',
          }



URL = 'https://www.khabkrai.ru/events/news' #В качестве URL передаем ссылку на страницу новостей Правительства края
user_agent = user_agent("chrome")
#Передаем в переменную headers значения юзерагента для
headers = {'accept': '*/*', 'user-agent': user_agent}

def page_open(url: str, headers: str,  iterations: int):
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

        while iterations > 0:
            # Находим кнопку "Загрузить еще и нажимаем ее"
            #'ajax_paginator_btn'
            driver.find_element(By.XPATH,
                                     '/html/body/div[2]/div[2]/div[7]/div/div[3]/div[2]/div[1]/div/div/div/a/span').click()
            # Ожидание прогрузки страницы
            time.sleep(5)
            iterations -= 1
        html_content = driver.page_source
        return html_content

def parse_pages(url: str, headers: str) -> list:
    """Функция принимает в себя адрес и заголовки
    на странице ссылки и возвращает список ссылок"""
    Links = []
    html_content = page_open(url, headers)
    soup = BeautifulSoup(html_content, 'lxml')
    #регулярным выражением ищем все ссылки в html и собираем их по сайту
    for link in soup.find_all('a', href=re.compile('^(/|.*' + url + ')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in Links:
                if link.attrs['href'].startswith('/'):
                    Links.append(url + link.attrs['href'])
                else:
                    Links.append(link.attrs['href'])
        else:
            print("Connection Error")
    print(f"Обнаружено {len(Links)} ссылок")
    return Links

def working_check(links: list, headers: str) -> list:
    """Функция принимает в себя список ссылок и заголовки,
    проверяет работоспособность ссылок и возвращает список работоспособных ссылок"""
    working_links = []
    for link in links:
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            working_links.append(link)
        #    print(f'Обнаруженная ссылка № {n} {link} работает и добавлена в список')
        #else:
        #    print(f'Обнаруженная ссылка № {n} {link} не отвечает')
    print(f'Работоспособны {len(working_links)} ссылок')
    return working_links

"""
Распарсить все ссылки
Выделить в каждой id из ссылки, 
дату class="material-date data-item"
Заголовок <h1> и class wrapper
Текст <p>
и ссылку

Результаты представить в виде кортежа id, data, head, next, link

Из всей выборки взят те у которых дата равна 

year,m,d = date.split(' ') # 7 июля 2022
year = int(year)
m = 
today == date.today()
return (row for result if row[i] == date.today()
"""


if __name__ == '__main__':
    links = parse_pages()
    page_open()