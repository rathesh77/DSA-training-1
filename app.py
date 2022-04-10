#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, Response
from datetime import datetime
from time import time
import re
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
        for url in dict[date_prefix]:
            count += dict[date_prefix][url]
            
        #count = len(dict[date_prefix])    
    return jsonify({"count": count})


@app.route('/1/queries/popular/<date_prefix>', methods=['GET'])
def popular(date_prefix=None):
    size = request.args.get('size', type=int, default=3)
    #TODO
    parsedDate = None
    if (parsedDate := validate(date_prefix, '%Y-%m-%d')) == False:
        if (parsedDate := validate(date_prefix, '%Y-%m')) == False:
            if (parsedDate := validate(date_prefix, '%Y') )== False: 
                if (parsedDate := validate(date_prefix, '%Y-%m-%d %H:%M:%S')) == False:
                    return Response('invalid date format', status=400)

    #if (not date_prefix in dict) :
    #    return Response('error date is not stored', status=400)
    keys = list()
    seen = {}
    for date in dict:
        if re.search("^"+parsedDate, date) != None and not date in seen:
            keys.append(date)
            seen[date] = True
            
    if len(keys) == 0:
        return Response('error date is not stored', status=400)

    json = {"queries": []}
    ans = list()

    print(keys)
    quit = False
    count = 0
    for date in keys:
        urls = dict[date]

        urls_keys = list(urls.keys())
        res = list()
        for i in range(0, len(urls_keys)): 
            for j in range (i+1, len(urls_keys)): 
                if urls[urls_keys[i]] < urls[urls_keys[j]]:
                    temp = urls_keys[i]
                    urls_keys[i] = urls_keys[j]
                    urls_keys[j] = temp
            res.append(urls_keys[i])
            count+=1
            if (count == size):
                quit = True
                break
        print(urls_keys)
        print(res)
        for i in range(0, len(res)):
            ans.append({'url': res[i], 'count': urls[res[i]], date: date})
        if quit == True:
            break

    json["queries"].append({"query": ans})
    return jsonify(json)

def validate(date_text, format):
    try:
        datetime.strptime(date_text, format)
        return date_text
    except ValueError:
        return False

# LOADING LOGS
load_logs("hn_logs.tsv")

if __name__ == '__main__':
    # LAUNCHING REST API
    app.run(host='0.0.0.0', port=5000, debug=False)