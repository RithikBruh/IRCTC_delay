import requests
import random
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Randomized User-Agent rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
]

headers = {
    "User-Agent": random.choice(user_agents),
}

url = "https://runningstatus.in/history/12749/thisyear"
url2 = "https://runningstatus.in"

def Scrape(req_station = "lingampalli"):

    req_station = "lingampalli"

    response = requests.get(url, headers=headers, timeout=10)
    html = response.text

    soup = BeautifulSoup(html, "lxml")

    print(__file__)
    with open("output_main.txt","w", encoding="utf-8") as f :
        f.write(soup.prettify())

    #TODO : do caching to avoid multiple requests 

    table = soup.select("td a")
    for table_data in table :
        page_link = table_data.get("href")

        # TODO : remove below
        page_link = "/status/12749-on-20250616"

        page_link = url2 + page_link 
        print(f'Going to -------{page_link} --------')
        
        # Initialize undetected Chrome with stealth options
        options = uc.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        driver = uc.Chrome(options=options, use_subprocess=True)
        
        try:
            driver.get(page_link)

            # wait until some element appears (so JS is done)
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
            )

            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")

            
                
            table_rows = soup.select("tr")
            with open("output1.txt","w", encoding="utf-8") as f : 
                f.write(str(table_rows))

            for table_row in table_rows :
                # if table_row.find("td") == 
                # print(table_row.find())
                # with open("output2.txt","a") as f:
                #     f.write(str(table_row.find().text)+"\n\n\n")
                if req_station.lower() in str(table_row.find().text).lower():
                    print(table_row.find().find_next_sibling().text)
                # with open("output.txt","a") as f:
                #     f.write(str(table_row.prettify())+'\n\n\n')

            
            # for h in soup.select("h1"):
            #     print(h.get_text(strip=True))
            # with open("output.txt","w+") as f:
            #     f.write(soup.prettify()[:18000])
            # print(soup.prettify())

        finally:
            # Ensure driver closes even if error occurs
            driver.quit()

        break



        


