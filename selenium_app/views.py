from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from django.http import HttpRequest, JsonResponse
from Site_App.models import Site_scrape
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from django.shortcuts import render
import itertools

def get_price_another(name):
    session = HTMLSession()
    name = name.replace(' ', '+')
    url = 'https://www.google.com/search?client=firefox-b-d&q=' + name
    r = session.get(url)
    Links = r.html.xpath('//a[@jsname = "UWckNb"]')
    TitrsSite = r.html.find('span.VuuXrf')
    TitrsList = []
    LinkList = []
    i = 0
    for titr in TitrsSite:
        if i % 2 == 0:
            TitrsList.append(titr.text)
        i += 1
    for link in Links:
        LinkList.append(link.attrs['href'])

    PriceAll = []
    for titr, link in zip(TitrsList, LinkList):
        SiteInfo = Site_scrape.objects.filter(name=titr).first()
        if SiteInfo is not None:
            # web driver search
            if SiteInfo.type_search == 1:
                options = Options()
                options.add_argument('--headless')
                driver = webdriver.Firefox(options=options)
                driver.get(link)
                time.sleep(0.3)
                try:
                    if SiteInfo.type == 0:
                        price = driver.find_element(By.CSS_SELECTOR, SiteInfo.address_element)  # erorr
                        PriceAll.append({'price': price.text, 'address_image': SiteInfo.image.url})
                    else:
                        price = driver.find_element(By.XPATH, SiteInfo.address_element)  # erorr
                        PriceAll.append({'price': price.text, 'address_image': SiteInfo.image.url})
                except:
                    PriceAll.append({'price': 'موجود نیست', 'address_image': SiteInfo.image.url})
                driver.close()
            ################### search of html session
            elif SiteInfo.type_search == 0:
                site_response = session.get(link)
                try:
                    if SiteInfo.type == 0:
                        price = site_response.html.find(SiteInfo.address_element, first=True)
                        PriceAll.append({'price': price.text, 'address_image': SiteInfo.image.url})
                    else:
                        price = site_response.html.xpath(SiteInfo.address_element, first=True)
                        PriceAll.append({'price': price.text, 'address_image': SiteInfo.image.url})
                except:
                    PriceAll.append({'price': 'موجود نیست', 'address_image': SiteInfo.image.url})
    return PriceAll



def scrape_price(request):
    name_product=request.GET['name_product']
    print(name_product)
    PriceAll =get_price_another( name_product)
    l = [PriceAll[i:i + 4] for i in range(0, len(PriceAll), 4)]
    return render(request, 'pages/scrape_side.html', {'group_price': l})
