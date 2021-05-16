import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
from random import randint
import numpy as np
import re
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

BASE_URL = 'https://www.airbnb.fr'

city = input('give me the name of the city where you want to go: ')

length_of_stay = input('Do you want to stay a weekend, a week, a month? ')

if length_of_stay not in {'weekend', 'week', 'month'}:
    raise ValueError ("wrong input choose between 1.weekend 2.week 3.month !")
    
during_which_month = input('during which month would you like to travel? ')

if during_which_month not in {'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre'}:
    raise ValueError ("wrong input choose between 1.Mai 2.Juin 3.Juillet 4.Aout 5.Septembre 6.Octobre !")
    
def find_destination_and_date():
    
    #Start airbnb website
    
    browser = webdriver.Chrome( '/Users/louis/Downloads/chromedriver-2')
    time.sleep(2)
    
    browser.get('https://www.airbnb.fr')
    time.sleep(2)
    
    #clear pop up
    
    accept_button = browser.find_element_by_class_name('_1qnlffd6').click()
    if not accept_button:
        pass
    else:
        accept_button.click()
    
    #LOC 
    location = browser.find_element_by_name('query')
    location.send_keys(city)

    #WHEN
    arrivée = browser.find_elements_by_css_selector('div._uh2dzp')[0].click()
    time.sleep(3)
    
    dates_flexibles = browser.find_element_by_id('tab--tabs--1').click()
    
    time.sleep(3)

    if length_of_stay == 'week':
        week = browser.find_elements_by_css_selector('button._t6p96s')[0].click()
    elif length_of_stay == 'month':
        month = browser.find_elements_by_css_selector('button._t6p96s')[1].click()

    time.sleep(3)

    if during_which_month == 'Mai':
        #dois cliquer dessus pour enlever la préselection
        juin = browser.find_elements_by_css_selector('button._100b7maj')[1].click()
        
        time.sleep(2)
        
        mai = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
    
    elif during_which_month == 'Juin':
        #dois cliquer dessus pour enlever la préselection
        mai = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
        
        time.sleep(2)
        
        juin = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
    
    elif during_which_month == 'Juillet':
        #dois cliquer dessus pour enlever la préselection
        mai = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
        time.sleep(2)
        
        juillet = browser.find_elements_by_css_selector('button._1irern2')[1].click()
        time.sleep(2)
        
        juin = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
        
        
    elif during_which_month == 'Aout':
        #dois cliquer dessus pour enlever la préselection
        mai = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
        time.sleep(2)
        
        aout = browser.find_elements_by_css_selector('button._1irern2')[2].click()
        time.sleep(2)
        
        juin = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
        
        
    elif during_which_month == 'Septembre':
        #dois cliquer dessus pour enlever la préselection
        mai = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
        time.sleep(2)
        
        septembre = browser.find_elements_by_css_selector('button._1irern2')[3].click()
        time.sleep(2)
        
        juin = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
        
        
    elif during_which_month == 'Octobre':
        #dois cliquer dessus pour enlever la préselection
        mai = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
        time.sleep(2)
        
        octobre = browser.find_elements_by_css_selector('button._1irern2')[4].click()
        time.sleep(2)
        
        juin = browser.find_elements_by_css_selector('button._100b7maj')[0].click()
        
        

    time.sleep(3)

    #SEARCH
    recherche = browser.find_element_by_css_selector('div._w64aej').click()
    
    #return url
    url = browser.current_url
    
    return url

url = find_destination_and_date()


def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def getnexturl(soup):
    page = soup.find('div', {'class': '_99vlue'})
    next_page = BASE_URL + page.find('a', {'aria-label': 'Suivant'})['href']
    return next_page

def getpages(url, number_of_pages):
    a_list = []
    for elem in range(number_of_pages):
        
        soup = get_data(url)
        url = getnexturl(soup)
        a_list.append(url)
        
    #print(a_list)
    return a_list

pages = getpages(url, 4)

price = []
urls = []
title = []
location = []
the_type = []
score = []
number_of_comments = []


for page in pages:
    url = page
    results = requests.get(url)
    soup = BeautifulSoup(results.text, 'html.parser')
    rent_div = soup.find_all('div', class_ = '_fhph4u')
    time.sleep(randint(2,10))
    #print(rent_div)
    for section in rent_div:
        
        #PRICES 
        
        tags_with_prices = section.find_all('span' , {'class': '_155sga30'})
        for elem in tags_with_prices:
            prices = int(''.join(re.findall('[0-9]', str(elem).split(">")[1])))
            #print(prices)
            price.append(prices)
       
        #URLS
        
        tags_with_url = section.find_all('meta', {'itemprop' : 'url'})
        for elem in tags_with_url:
            a = re.split('"' ,str(elem))[1]
            b = re.split(';', a)
            b.pop(2)
            url = ''.join(b)
            #print(url)
            urls.append(url)
        
         #TITLE
        
        tags_with_name = soup.find_all('meta', {'itemprop' :'name'})
        for elem in tags_with_name:
            a = re.split('=',str(elem))
            a.pop(0)
            a.pop(1)
            b = re.split('"', str(a))[1]
            #print(b)
            title.append(b)
            
        #NOTE 
        
        tags_with_notes = soup.find_all('span', {'class':'_18khxk1'})
        for elem in tags_with_notes:
            
            hey =str(elem).split(';')[0]
            pattern = '\d+'
            numbers = re.findall(pattern,hey)
            floa = float(numbers[0] + '.' + numbers[1])
            #print(floa)
            score.append(floa)
        
        #NUMBERCOMMENTS 
        tags_with_comments = soup.find_all('span', {'class':'_18khxk1'})
        for elem in tags_with_comments:
            pattern = '\d+'
            com = ''.join(re.findall(pattern,str(elem).split('"')[1].split(';')[1]))
            #print(com)
            
            number_of_comments.append(com)
            
            
        #LOCATION 
        tags_with_location_and_type = soup.find_all('div', {'class': '_b14dlit'})
        for elem in tags_with_location_and_type:
            loc = str(elem).split('à')[1].split('<')[0]
            location.append(loc)
        
        #TYPE 
        tags_with_location_and_type = soup.find_all('div', {'class': '_b14dlit'})
        for elem in tags_with_location_and_type:
            type_ = str(elem).split('à')[0].split('>')[1]
            the_type.append(type_)
            

d = {'Titre' : title,
     'Prix' : price,
     'Situation': location,
     'Type': the_type,
     'Notes': score,
     'Nombre de commentaires': number_of_comments,
     'liens': urls}

    
    
#df = pd.DataFrame(d)
df = pd.DataFrame.from_dict(d, orient='index')
df = df.transpose()
df.to_excel('airbnb.xlsx')

