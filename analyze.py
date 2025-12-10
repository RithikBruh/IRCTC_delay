from scrape import scrape 
from datetime import datetime
import matplotlib.pyplot as plt


def get_delay(delay_str : str) -> int :
    delay_str = delay_str.upper()
    # 12H 14M late 
    # 12M Late
    hours = 0
    minutes = 0

    # extract H
    if "H" in delay_str:
        hours = int(delay_str.split("H")[0].strip())

    # extract M
    if "M" in delay_str:
        # split at H first, then at M
        parts = delay_str.split("H")[-1] if "H" in delay_str else delay_str
        minutes = int(parts.split("M")[0].strip())

    return hours * 60 + minutes

def filter(dates : list ,delays : list) : 

    dates_filtered = []
    delays_filtered = [] 

    for date, delay in zip(dates,delays) :
        if "no record" in delay.lower() :
            continue

        # convert string → datetime object
        dt = datetime.strptime(date, "%d %b, %Y")

        # convert datetime → desired format yy-mm-dd
        formatted = dt.strftime("%y-%m-%d")
        dates_filtered.append(formatted)

        if "no delay" in delay.lower() :
            delays_filtered.append(0)
        else :
            delays_filtered.append(get_delay(delay))
    
    return (dates_filtered,delays_filtered)

def plot(x , y) : 
    # bar chart
    plt.bar(x, y)

    # labels and title
    plt.xlabel("Samples")
    plt.ylabel("Values")
    plt.title("Bar Chart of Samples vs Values")

    # show plot
    plt.show()            # display graph

def analyze() :
    scrape_data = scrape(train_num="12749",req_station="secunderabad",cache_override=True)
    print(scrape_data)
    dates = scrape_data.keys()
    delays = list(map(lambda x : x[19:] , list(scrape_data.values()) ))
    
    dates_filtered , delays_filtered = filter(dates,delays)
    print(dates_filtered,delays_filtered)
    plot(dates_filtered,delays_filtered)

    

    # print(delays)


if __name__ == "__main__" : 
    analyze()
    # print(get_delay("1H Late"))