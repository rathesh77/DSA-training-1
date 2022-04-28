#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, Response
from datetime import datetime
from time import time
from Tree import *
import re
# Setting up Flask app
app = Flask(__name__)
dict = {}
trees = {}
# Utility functions
def load_logs(filename):
    print("loading, please wait...")
    start = time()
    with open(filename, 'r') as f:
        for line in f:
            splited = line.strip('\n').split('\t')
            date = datetime(*map(int, splited[0].replace(":", "-").replace(" ", "-").split("-")))
            url = splited[1]
            add_to_logs(date, url)
    end = time()
    print("loaded in : " + str(round(end - start, 3)) + "s")

def update_branch(trees, date, url):
    if (not date in trees):
        trees[date] = {}
    if not url in trees[date]:
        trees[date][url] = {'count': 1} 
    else:
        trees[date][url]['count'] += 1 

def slice_date(date, end):
    str = ''
    for i in range(0, end+1):
        str += date[i]
    return str

def add_to_logs(date, url):
    #TODO
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")

    f1 = slice_date(date_str, 15)
    f2 = slice_date(date_str, 12)
    f3 = slice_date(date_str, 9)
    f4 = slice_date(date_str, 6)
    f5 = slice_date(date_str, 3)
    
    if not date_str in dict:
        dict[date_str] = {url : {'count': 1}}
    else:
        update_branch(dict, date_str, url)
    update_branch(dict, f1, url)
    update_branch(dict, f2, url)
    update_branch(dict, f3, url)
    update_branch(dict, f4, url)
    update_branch(dict, f5, url)

def parse_date(date):
    
    if (parse_date := validate(date, '%Y-%m-%d')) == False:
        if (parse_date := validate(date, '%Y-%m')) == False:
            if (parse_date := validate(date, '%Y') )== False: 
                if (parse_date := validate(date, '%Y-%m-%d %H')) == False:
                    if (parse_date := validate(date, '%Y-%m-%d %H:%M')) == False:
                            if (parse_date := validate(date, '%Y-%m-%d %H:%M:%S')) == False:
                                return None
    return parse_date


@app.route('/1/queries/count/<date_prefix>', methods=['GET'])
def count(date_prefix=None):
    #TODO
    date_prefix = parse_date(date_prefix)
    if date_prefix == None:
        return Response('error date is not stored', status=400)
    
    dates = list()
    for date in dict:
        if re.search("^"+date_prefix, date) != None:
            dates.append(date)
    count = 0
    for date in dates:
        for url in dict[date]:
                count += dict[date][url]
    return jsonify({"count": count})


@app.route('/1/queries/popular/<date_prefix>', methods=['GET'])
def popular(date_prefix=None):
    size = request.args.get('size', type=int, default=3)
    #TODO
    start = time()
    parsed_date = parse_date(date_prefix)
    if parsed_date == None:
        return Response('error date is not stored', status=400)


    out = []

    out = trees[parsed_date].descendingSort(size)
    end = time()
    print("time taken : " + str(round(end - start, 3)) + "s")

    return jsonify({"queries": out})

def validate(date_text, format):
    try:
        datetime.strptime(date_text, format)
        return date_text
    except ValueError:
        return False

# LOADING LOGS
load_logs("hn_logs.tsv")

for date in dict:
    trees[date] = Tree()
    for url in dict[date]:
        el = {'url': url, 'count': dict[date][url]['count']}
        trees[date] = trees[date].insert(el)
if __name__ == '__main__':
    # LAUNCHING REST API
    app.run(host='0.0.0.0', port=5000, debug=False)