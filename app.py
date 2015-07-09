#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import pdb
import requests
from flask import Flask, render_template, redirect, Markup
from bs4 import BeautifulSoup


app = Flask(__name__)
workouts = {}


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
    soup = BeautifulSoup(data, "html.parser")
    links = soup('a', rel='bookmark')
    entries = []

    for x in links:
        title = x.text[:x.text.find('Competition')-len(' - ')] # Cut off text after date
        link = x['href']
        workouts[title] = link
        entries.append(title)

    return entries


'''
Index is at page 1, so I redirect from root to there.
'''
@app.route("/")
def workouts_list():
    return redirect("/page/1")


'''
Paging, to view more workouts if one desires.
'''
@app.route("/page/<pager>")
def workouts_by_page(pager):
    url = 'http://www.crossfitinvictus.com/category/wod/competition/'
    paged_url = url + 'page/' + str(pager)
    entries = generate_list(paged_url)

    paging_left = int(pager) > 1
    paging_right = len(entries) == 10

    return render_template('index.html', page=pager, paging_left=paging_left, paging_right=paging_right, result=entries)


@app.route("/workout/<date>")
def view_workout(date):
    data = requests.get(workouts[date]).text
    html = BeautifulSoup(data)

    workout = str(html('div', class_="entry")[0])
    cutOff = workout.find('<div class="divider">') # Remove info section below workout
    workout = workout.replace(u'\xa0', u' ')[:cutOff].strip()

    return render_template('workout.html', title=date, workout=Markup(workout))


if __name__ == "__main__":
    app.run()
