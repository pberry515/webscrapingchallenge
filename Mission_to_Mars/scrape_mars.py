# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    # Mars News URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    news_soup = bs(html, 'html.parser')
    # Retrieve the latest news title and paragraph
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image to be scraped
    jpl_nasa_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    images_soup = bs(html, 'html.parser')
    # Retrieve featured image link
    relative_image_path = images_soup.find_all('img')[3]["src"]
    featured_image_url = jpl_nasa_url + relative_image_path

    # Mars facts to be scraped, converted into html table
    marsfacts_url = 'https://space-facts.com/mars/'
    marstables = pd.read_html(facts_url)
    marsfacts_df = tables[2]
    marsfacts_df.columns = ["Description", "Value"]
    mars_html_table = mars_facts_df.to_html()
    mars_html_table.replace('\n', '')
    
    # Mars hemisphere name and image to be scraped
    usgs_url = 'https://astrogeology.usgs.gov'
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    hemis_soup = bs(html, 'html.parser')
    # Mars hemispheres products data
    mars_hemis = hemis_soup.find('div', class_='collapsible results')
    mars_items = mars_hemis.find_all('div', class_='item')
    hemisphere_image_urls = []
    # Iterate through each hemisphere data
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

    # Mars 
    mars_dict={
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "mars fact_table":mars_html_table,
    "hemisphere_images":hemisphere_image_urls
}

    return mars_dict