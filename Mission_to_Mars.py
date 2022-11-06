# 10.3.6 Export to Python

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
# parent element
slide_elem = news_soup.select_one('div.list_text')

# find:
# <div class="content_title">HiRISE Views NASA's InSight and Curiosity on Mars</div>
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ## 10.3.4 Scrape Mars Data: Featured Image

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

# Find the relative image url
# get('src') pulls the image link
# <img class="fancybox-image" src="image/featured/mars3.jpg" alt="">
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# ## 10.3.5 Scrape Mars Data: Mars Facts
# All she wants from this page is the table. Her plan is to display it as a table on her own web app, so keeping the current HTML table format is important.

# scrape the entire table with Pandas' .read_html() function
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

# shut down automated browser, because the scraping is done
browser.quit()
