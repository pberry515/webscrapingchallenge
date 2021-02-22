# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
def scrape():
    browser=init_browser()
    mars_dict={}
    ### NASA Mars News

    # URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(5)
    html=browser.html
    news_soup=bs(html,'html.parser')

    # Grab the latest news title and paragraph
    news_title=news_soup.find_all('div', class_='content_title')[1].text
    news_p=news_soup.find_all('div', class_='rollover_description_inner')[0].text
    
    ### JPL Mars Space Images - Featured Image

    jpl_nasa_url="https://www.jpl.nasa.gov"
    images_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)

    # HTML object
    html=browser.html
    time.sleep(5)
    # Parse HTML
    images_soup=bs(html,"html.parser")

    # Retrieve image url
    images_url=images_soup.find_all('article')

    images_url=images_soup.find('article')['style']
    images_url=images_url.split("'")[1]

    featured_image_url=jpl_nasa_url+images_url
    
    ### Mars Fact

    # Scrape Mars facts from https://space-facts.com/mars/
    marsfacts_url='https://space-facts.com/mars/'
    marstables=pd.read_html(marsfacts_url)
    
    marsfacts=marstables[0]
    marsfacts=marsfacts.rename(columns={0:"Profile",1:"Value"},errors="raise")
    marsfacts.set_index("Profile",inplace=True)
    marsfacts
    
    mars_html_tables=marsfacts.to_html()
    mars_html_tables.replace('\n','')
    
    ### Mars Hemispheres

    # Scrape Mars hemisphere title and image
    usgs_url='https://astrogeology.usgs.gov'
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    # Extract hemispheres item elements
    mars_hems=soup.find('div',class_='collapsible results')
    mars_item=mars_hems.find_all('div',class_='item')
    hemisphere_image_urls=[]

    # Loop through each hemisphere item
    for item in mars_item:
        # Error handling
        try:
            # Extract title
            hem=item.find('div',class_='description')
            title=hem.h3.text
            # Extract image url
            hem_url=hem.a['href']
            browser.visit(usgs_url+hem_url)
            html=browser.html
            soup=bs(html,'html.parser')
            image_src=soup.find('li').a['href']
            if (title and image_src):
                # Print results
                print('-'*50)
                print(title)
                print(image_src)
            # Create dictionary for title and url
            hem_dict={
                'title':title,
                'image_url':image_src
            }
            hemisphere_image_urls.append(hem_dict)
        except Exception as e:
            print(e)

    # Create dictionary for all info scraped from sources above
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,    
        "mars_fact_table":mars_html_table,
        "hemisphere_images":hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    return mars_dict