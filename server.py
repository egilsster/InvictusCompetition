import pdb
import re
import requests
from flask import Flask, render_template, request, redirect, url_for, session, Markup
from bs4 import BeautifulSoup
from pprint import pprint
# import urllib.request
# import concurrent.futures
# from collections import OrderedDict


app = Flask(__name__)

# postnr = re.compile(r'class="post-(\d+)\s')

url = 'http://www.crossfitinvictus.com/category/wod/competition/'
workouts = {}
entries = []

'''
Return the contents of the page.
'''
def load_url(url):
    return requests.get(url).text

'''
Generates the list that contains the URLs to the workouts.
This is linked with the title of the workout which is the date.
'''
def generate_list(url):
    data = load_url(url)
    soup = BeautifulSoup(data)
    hrefs = soup('a', rel='bookmark')
    entries = []

    for x in hrefs:
        title = x.text[:x.text.find(' – ')]
        link = x['href']
        workouts[title] = link
        entries.append(title)

    return entries

@app.route("/")
def workouts_list():
    return redirect("/page/1")

'''
Paging, to view more workouts if one desires.
'''
@app.route("/page/<pagenr>")
def workouts_by_page(pagenr):
    paged_url = url + 'page/' + str(pagenr)
    entries = generate_list(paged_url)

    paging_left = int(pagenr) > 1
    paging_right = len(entries) == 10

    return render_template('index.html', page=pagenr, paging_left=paging_left, paging_right=paging_right, result=entries)

@app.route("/workout/<wdate>")
def view_workout(wdate):
    data = requests.get(workouts[wdate]).text
    html = BeautifulSoup(data)

    workout = str(html('div', class_="entry")[0])
    cutOff = workout.find('<div class="divider">') # Remove info section below workout
    workout = workout.replace(u'\xa0', u' ')[:cutOff].strip()

    return render_template('workout.html', title=wdate, workout=Markup(workout))



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)
