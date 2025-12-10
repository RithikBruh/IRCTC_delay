import requests
import random
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from cache import cache_results
from cache import save_cache

# Randomized User-Agent rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
]


url_main = "https://runningstatus.in"


def scrape(req_station="lingampalli", train_num="12749",cache_override=False,scopes = ["lastyear","thisyear"] ,cache_update=False):
    """
    Scrape running status information for a specific Train at specific station.
    """

    scrape_output = {}
    cache_input = {"train-no": train_num, "each_station_data": {
    }}

    # TODO : First check cache for exitsting results
    cache_found = False 

    if not cache_override :
        cache_data = cache_results(train_num,req_station)
        if cache_data["is_avaliable"] :
            if not cache_update : 
                print(f"Found Cache Not Scraping!")
                return cache_data["data"]
            else :
                cache_found = True
                print("need to update cache")

    # TODO ; remove this
    test_limit = 4


     # order maintain

    for scope in scopes:
        url = "https://runningstatus.in/history/12749/" + scope
        headers = {
            "User-Agent": random.choice(user_agents),
        }

        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        soup = BeautifulSoup(html, "lxml")

        # print(__file__)

        # with open("output_main.txt", "w", encoding="utf-8") as f:
        #     f.write(soup.prettify())

        # TODO : do caching to avoid multiple requests

        dates = soup.select("td a")
        i = 0
    
        for date in dates:
            # testing 
            if i >= test_limit :
                print("Test limit reached")
                break 
            i += 1
            
            date_str = date.text
            if cache_found :
                if date_str in cache_data["data"].keys() :
                    print(f"Skipping cached date : {date_str} ")
                    continue
                else :
                    print(f"Date {date_str} not in cache , scraping... ")
        
            ## 
            date_page_link = date.get("href")

            date_page_link = url_main + date_page_link
            print(f'Going to -------{date_page_link} --------')

            # Initialize undetected Chrome with stealth options
            options = webdriver.ChromeOptions()
            # options.add_argument(
            #     '--disable-blink-features=AutomationControlled')
            # options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--no-sandbox')
            options.add_argument(f'user-agent={random.choice(user_agents)}')
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
            # TODO : headless mode 
            try:
                driver.get(date_page_link)

                # wait until some element appears (so JS is done)
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
                )

                html = driver.page_source
                soup = BeautifulSoup(html, "lxml")

                stations = soup.select("tr")
                # Each Table Row Contains -> Station Name , delay , ..

                # with open("output1.txt", "w", encoding="utf-8") as f:
                #     f.write(str(table_rows))

                for station in stations:
                    # if table_row.find("td") ==
                    # print(table_row.find())
                    # with open("output2.txt","a") as f:
                    #     f.write(str(station.prettify())+"\n\n\n")

                    # station :
                    #   <tr>
                    #       <td> Station Name </td>
                    #       <td> Delay </td>
                    #       ...
                    #   </tr>

                    try :
                        station_name = station.find().text
                        if station_name == "StationCode" :
                            continue
                        time_data = station.find().find_next_sibling().text
                    except :
                        continue    
                    # --> example --> each station data : {
                    #       "lingampalli" : {date : delay_data , date : delay_data}
                    #     }
                    if station_name in cache_input["each_station_data"].keys() :
                        cache_input["each_station_data"][station_name][date_str] = time_data
                    else :
                        cache_input["each_station_data"][station_name] = {date_str : time_data} 

                    if req_station.lower() in station_name.lower():
                        scrape_output[date.text] = time_data



                    # with open("output.txt", "a") as f:
                    #     f.write(str(table_row.prettify())+'\n\n\n')

                # for h in soup.select("h1"):
                #     print(h.get_text(strip=True))
                # with open("output.txt","w+") as f:
                #     f.write(soup.prettify()[:18000])
                # print(soup.prettify())


            finally:
                # Ensure driver closes even if error occurs
                driver.quit()

            
    
    print(f"Scrape data : {scrape_output} \n\n cache_data : {cache_input}")
    save_cache(cache_input)

    return scrape_output


if __name__ == "__main__" :
    print(scrape(cache_update=True))

