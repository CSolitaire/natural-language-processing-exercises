import pandas as pd
import numpy as np

from requests import get
import re
from bs4 import BeautifulSoup
import os
######################################## Web Scraping Function #########################################

# Create a helper function that requests and parses HTML returning a soup object.

def make_soup(url):
    '''
    This helper function takes in a url and requests and parses HTML
    returning a soup object.
    '''
    headers = {'User-Agent': 'Codeup Data Science'} 
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_blog_articles(urls, cached=False):
    '''
    This function takes in a list of Codeup Blog urls and a parameter
    with default cached == False which scrapes the title and text for each url, 
    creates a list of dictionaries with the title and text for each blog, 
    converts list to df, and returns df.
    If cached == True, the function returns a df from a json file.
    '''
    if cached == True:
        df = pd.read_json('big_blogs.json')
        
    # cached == False completes a fresh scrape for df     
    else:

        # Create an empty list to hold dictionaries
        articles = []

        # Loop through each url in our list of urls
        for url in urls:

            # Make request and soup object using helper
            soup = make_soup(url)

            # Save the title of each blog in variable title
            title = soup.find('h1').text

            # Save the text in each blog to variable text
            content = soup.find('div', class_="jupiterx-post-content").text

            # Create a dictionary holding the title and content for each blog
            article = {'title': title, 'content': content}

            # Add each dictionary to the articles list of dictionaries
            articles.append(article)
            
        # convert our list of dictionaries to a df
        df = pd.DataFrame(articles)

        # Write df to a json file for faster access
        df.to_json('big_blogs.json')
    
    return df
