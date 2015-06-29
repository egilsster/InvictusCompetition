import pdb
import re
import requests
import concurrent.futures
import urllib.request
from bs4 import BeautifulSoup
from pprint import pprint

postnr = re.compile(r'class="post-(\d+)\s')

'''
Return the contents of the page.
'''
def load_url(url):
    return requests.get(url).text

'''

'''
def getWorkouts(entries):
    workouts = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_url = { executor.submit(load_url, url): url for url in entries }
        for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
            url = future_to_url[future]
            try:
                data = future.result()
                html = BeautifulSoup(data)
                title = html('h1')[0].text
                workout = str(html('div', class_="entry")[0])
                cutOff = workout.find(' \n\nBy') # Remove info section below workout
                workout = workout.replace(u'\xa0', u' ')[:cutOff].strip()
                workouts[title] = workout
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))

    return workouts


'''

'''
def generateList(markup):
    for item in markup:
        print(item)

nammi = None
if __name__ == "__main__":
    url = 'http://www.crossfitinvictus.com/category/wod/competition/'
    data = load_url(url)
    soup = BeautifulSoup(data)
    hrefs = soup('a', rel='bookmark')
    entries = [ x['href'] for x in hrefs ]

    workouts = getWorkouts(entries[:1])
    nammi = workouts
    pprint(workouts)
