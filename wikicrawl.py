import requests
from bs4 import BeautifulSoup
import time
import urllib

# response = requests.get('https://en.wikipedia.org/wiki/Dead_Parrot_sketch')
# html = response.text
# soup = BeautifulSoup(html, 'html.parser')
# print(soup.title.text)

start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"

def continue_crawl(search_history, target_url, max_steps=25):
    if search_history[-1] == target_url:
        print("Found target URL")
        return False
    elif len(search_history) > max_steps:
        print("Search exceeded max steps")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("We've been here before")
        return False
    else:
        return True

def find_first_link(url):
    # get the HTML from "url", use the requests library
    response = requests.get(url)
    html = response.text
    # feed the HTML into Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # find the first link in the article, or set to None if there is no link
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")
    article_link = None
    
    # Find all the direct children of content_div that are paragraphs
    for element in content_div.find_all("p", recursive=False):
        # Find the first anchor tag that's a direct child of paragraph.
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break
    if not article_link:
        return
    
    # Build a full url from the relative article_link url
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)
    
    return first_link
    
article_chain = [start_url]
    
while continue_crawl(article_chain, target_url):
    print(article_chain[-1])
    # download html of last article in article_chain
    # find the first link in that html
    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print('Article with NO LINKS!')
        break
    # add the first link to article_chain
    article_chain.append(first_link)
    # delay for about two seconds
    time.sleep(2)