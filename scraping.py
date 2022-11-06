# 10.3.6 Export to Python
# 10.5.2 Update the Code
# 10.5.3 Integrate MongoDB Into the Web App

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt


# Initialize the browser.
# Create a data dictionary.
# End the WebDriver and return the scraped data.
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary.
 
    # This dictionary does two things: It runs all of the functions 
    # we've created
    # —featured_image(browser), for example
    # —and it also stores all of the results. 
    # When we create the HTML template, we'll create paths to 
    # the dictionary's values, which lets us present our data on our template. 
    # We're also adding the date the code was run last 
    # by adding "last_modified": dt.datetime.now().
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
        
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    # parent element
    slide_elem = news_soup.select_one('div.list_text')

    try:  
        # find:
        # <div class="content_title">HiRISE Views NASA's InSight and Curiosity on Mars</div>
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None

    return news_title, news_p


# ## 10.3.4 Scrape Mars Data: Featured Image

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button (there are only 3 buttons)
    # [1] at the end means click 2nd button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # begin to scrape full-size image
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        # get('src') pulls the image link
        # <img class="fancybox-image" src="image/featured/mars3.jpg" alt="">
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# ## 10.3.5 Scrape Mars Data: Mars Facts
# All she wants from this page is the table. Her plan is to display it as a table on her own web app, so keeping the current HTML table format is important.

def mars_facts():

    try:
        # scrape the entire table with Pandas' .read_html() function
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
        
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
