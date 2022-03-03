from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    mars_data = {}
    browser = init_browser()
#News title and snippit
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_= 'content_title')
    news_title = news_title.text.strip()
    news_p = soup.find('div', class_= 'article_teaser_body')
    news_p = news_p.text.strip()
    
#Featured Image
    url_mars = 'https://spaceimages-mars.com/'
    browser.visit(url_mars)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_url = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = url_mars + image_url

#Mars table
    url_facts = 'https://galaxyfacts-mars.com/'
    df = pd.read_html(url_facts)
    facts_df = df[0]
    facts_df = facts_df.rename(columns = {0:'Info', 1:'Mars', 2:'Earth'})
    facts_df = facts_df.set_index('Info')
    facts_table = facts_df.to_html()
    facts_table = facts_table.replace('\n','')

#Hempisphere images and titles
    titles = []
    urls = []
    url_hemi = 'https://marshemispheres.com/'
    browser.visit(url_hemi)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')

    image_urls = []
    hemi = soup.find_all('div', class_='description')

    count = 0
    for each in hemi:
        title = each.a.find('h3')
        title = title.text
        titles.append(title)
        counter = count + 1
        if (count == 4):
            break

    count = 0
    for each in hemi:
        src = each.find('a')['href']
        site_url = url_hemi + src
        urls.append(site_url)
        count = count + 1
        if (count == 4):
            break

    for each in urls:
        browser.visit(each)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        src = soup.find('img',class_= 'wide-image')['src']
        full_url = url_hemi + src
        image_urls.append(full_url)

    hemi1 = {'title' : titles[0], 'img_url' : image_urls[0]}
    hemi2 = {'title' : titles[1], 'img_url' : image_urls[1]}
    hemi3 = {'title' : titles[2], 'img_url' : image_urls[2]}
    hemi4 = {'title' : titles[3], 'img_url' : image_urls[3]}

    hemisphere_urls = [hemi1, hemi2, hemi3, hemi4]

    mars_data['hemisphere_urls'] = hemisphere_urls
    mars_data['news_p'] = news_p
    mars_data['featured_image_url'] = featured_image_url
    mars_data['facts_table'] = facts_table

    return mars_data