#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import requests
from flask import Flask, render_template, redirect, Markup, jsonify
from bs4 import BeautifulSoup


url = 'http://www.crossfitinvictus.com/category/wod/competition/'

app = Flask(__name__)
workout_links = {}
workouts = {}

'''
Return the contents of the page.
'''


def load_url(uri):
    return requests.get(uri).text


'''
Fetches workout markup.
'''


def load_workout(date):
    if date not in workouts:
        data = requests.get(workout_links[date]).text
        html = BeautifulSoup(data, "html.parser")

        workout_markup = str(html('div', class_="entry")[0])
        cut_off = workout_markup.find('<div class="divider">')  # Remove info section below workout
        workout_markup = workout_markup.replace(u'\xa0', u' ')[:cut_off].strip()

        workouts[date] = workout_markup

    return workouts[date]


'''
Generates the list that contains the URLs to the workouts.
This is linked with the title of the workout which is the date.
'''


def generate_list(uri):
    data = load_url(uri)
    soup = BeautifulSoup(data, "html.parser")
    links = soup('a', rel='bookmark')
    entries = []

    for x in links:
        title = x.text[:x.text.find('Competition') - len(' - ')]  # Cut off text after date
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


@app.route("/api/workout/<string:date>", methods=['GET'])
def get_workout(date):
    return load_workout(date)


'''
API to get the workout list.
'''


@app.route("/api/workouts/<string:page>", methods=['GET'])
def get_workouts(page):
    url_list = generate_list(url + 'page/' + page)
    dic = {
        "workouts": [],
        "page": page
    }

    for date in url_list:
        workout_obj = {
            "title": date,
            "url": workout_links[date]
        }
        dic["workouts"].append({"workout": workout_obj})

    return jsonify(dic)


if __name__ == "__main__":
    app.run(debug=True)
