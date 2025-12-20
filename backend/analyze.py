import os
import matplotlib.pyplot as plt
from scrape import scrape
from datetime import datetime

import matplotlib
matplotlib.use("Agg")


curr_path = os.path.dirname(__file__)


def get_delay(delay_str: str) -> int:
    """ Input format : 1H 14M late , 12M Late
        Output Format : 74 , 12 (converts to minutes)"""
    delay_str = delay_str.upper()
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


def filter(dates: list, delays: list) -> tuple[list, list]:
    dates_filtered = []
    delays_filtered = []

    for date, delay in zip(dates, delays):
        if "no record" in delay.lower():
            continue

        # convert string → datetime object
        dt = datetime.strptime(date, "%d %b, %Y")

        # convert datetime → desired format yy-mm-dd
        formatted = dt.strftime("%y-%m-%d")
        dates_filtered.append(formatted)

        if "no delay" in delay.lower():
            delays_filtered.append(0)
        else:
            delays_filtered.append(get_delay(delay))

    return (dates_filtered, delays_filtered)


def plot(train_num, req_station, x, y, mean):
    line_g_path = os.path.join(curr_path, "graphs", "line_graph.png")
    bar_g_path = os.path.join(curr_path, "graphs", "bar_graph.png")
    # 1.Line Graph
    plt.plot(x, y)
    plt.grid(True)
    plt.tick_params(axis='x', labelbottom=False)
    plt.xlabel(f"{x[0]} to {x[-1]}")
    plt.axhline(y=mean, color='r', linestyle='--',
                label=f'Mean Delay: {mean:.2f} mins')
    plt.legend()
    # plt.show()
    plt.savefig(line_g_path)
    # bar chart
    plt.close("all")
    plt.bar(x, y)

    # labels and title
    plt.xlabel("Samples")
    plt.ylabel("Values")
    plt.title("Bar Chart of Samples vs Values")
    plt.tick_params(axis='x', labelbottom=False)
    plt.axhline(y=mean, color='r', linestyle='--',
                label=f'Mean Delay: {mean:.2f} mins')
    plt.legend()

    # show plot
    plt.savefig(bar_g_path)            # display graph
    plt.close("all")


def analyze(train_num="12749", req_station="secunderabad", cache_override=False, cache_update=True) -> dict:
    """Calls scrape.py and analyses the data

    Output Format : 
    {
        "mean" : mean_delay_in_mins
        "imgs" : ["bar_graph.png","line_graph.png"]
        "data" : [ {"date","<date>" , "delay", <delay_in_mins> } ,{..} , ... ] }
    }
    """
    scrape_data = scrape(train_num=train_num, req_station=req_station,
                         cache_override=cache_override, cache_update=cache_update)
    # print(scrape_data)
    dates = scrape_data.keys()
    delays = list(map(lambda x: x[19:], list(scrape_data.values())))

    dates_filtered, delays_filtered = filter(dates, delays)
    # print(dates_filtered, delays_filtered)

    mean = sum(delays_filtered)/len(delays_filtered)
    plot(train_num, req_station, dates_filtered, delays_filtered, mean)

    data = {"mean": mean, "imgs": ["bar_graph.png", "line_graph.png"],
            "data": [ {"date": date, "delay": delay} for date, delay in zip(
                dates_filtered, delays_filtered)]
                }
    print(data)
    return data

    # print(delays)


if __name__ == "__main__":
    analyze()
    # print(get_delay("1H Late"))
