import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all article titles (adjust the selector based on the website's structure)
        titles = soup.find()
        print(titles.get_text())
        # Print out each title
    #     for title in titles:
    #         print(title.get_text())
    # else:
    #     print(f"Failed to retrieve the page. Status code: {response.status_code}")

# URL of the website you want to scrape
url = 'https://jarrarcpa.com/about-us/'
scrape_website(url)
