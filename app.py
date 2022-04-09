#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from datetime import datetime
from time import time

# Setting up Flask app
app = Flask(__name__)
dict = {}
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


def add_to_logs(date, url):
    #TODO
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")

    if (not date_str in dict) :
        dict[date_str] = {}
        dict[date_str][url] = 1
    else :
        if (not url in dict[date_str]) :
            dict[date_str][url] = 1
        else :
            dict[date_str][url] += 1


@app.route('/1/queries/count/<date_prefix>', methods=['GET'])
def count(date_prefix=None):
    #TODO
    count = 0
    if (date_prefix in dict) :
        for url, c in dict[date_prefix] :
            count += c
            
        #count = len(dict[date_prefix])    
    return jsonify({"count": count})


@app.route('/1/queries/popular/<date_prefix>', methods=['GET'])
def popular(date_prefix=None):
    size = request.args.get('size', type=int, default=3)
    #TODO
    if (not date_prefix in dict) :
        return 'error date is not stored'
    json = {"queries": []}
    queries = dict[date_prefix]
    keys = list(queries.keys())
    end = size
    if end > len(keys):
        end = len(keys)
    for i in range(0, end): 
        for j in range (i+1, len(keys)): 
            if queries[keys[i]] < queries[keys[j]]: 
                temp = keys[i]
                keys[i] = keys[j]
                keys[j] = temp
    ans = list()
    for i in range(0, end):
        ans.append({'url': keys[i], 'count': queries[keys[i]]})

    json["queries"].append({"query": ans, "count": 1})
    return jsonify(json)

# LOADING LOGS
load_logs("hn_logs.tsv")
for key in dict:
    for value in dict[key] :
        if dict[key][value] > 1:
            print(key, value, dict[key][value])
if __name__ == '__main__':
    # LAUNCHING REST API
    app.run(host='0.0.0.0', port=5000, debug=False)