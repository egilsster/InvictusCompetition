#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import pdb
import requests
from flask import Flask, render_template, redirect, Markup, jsonify
from bs4 import BeautifulSoup

from pprint import pprint

url = 'http://www.crossfitinvictus.com/category/wod/competition/'

app = Flask(__name__)
workout_links = {}
workouts = {}

'''
Return the contents of the page.
'''
def load_url(url):
    return requests.get(url).text


'''
Fetches workout markup.
'''
def load_workout(date):
    if date not in workouts:
        data = requests.get(workout_links[date]).text
        html = BeautifulSoup(data)

        workout_markup = str(html('div', class_="entry")[0])
        cutOff = workout_markup.find('<div class="divider">') # Remove info section below workout
        workout_markup = workout_markup.replace(u'\xa0', u' ')[:cutOff].strip()

        workouts[date] = workout_markup

    return workouts[date]

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
        workout_links[title] = link
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
    paged_url = url + 'page/' + str(pager)
    entries = generate_list(paged_url)

    paging_left = int(pager) > 1
    paging_right = len(entries) == 10

    return render_template('index.html', page=pager, paging_left=paging_left, paging_right=paging_right, result=entries)


@app.route("/workout/<date>")
def view_workout(date):
    return render_template('workout.html', title=date, workout=Markup(load_workout(date)))


'''
API to get the workout markup.
'''
@app.route("/api/v1.0/workout/<string:date>", methods=['GET'])
def get_workout(date):
    return load_workout(date)


'''
API to get the workout list.
'''
@app.route("/api/v1.0/workouts/<string:page>", methods=['GET'])
def get_workouts(page):
    list = generate_list(url + 'page/' + page)
    dic = {}

    for date in list:
        dic[date] = workout_links[date]

    return jsonify(dic)


if __name__ == "__main__":
    app.run(debug=True)
