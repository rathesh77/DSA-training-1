#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, Response
from datetime import datetime
from time import time
import re
import numpy as np
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
    if date_prefix == None:
        return Response('error date is not stored', status=400)
        
    keys = list()
    seen = {}
    for date in dict:
        if re.search("^"+parsed_date, date) != None and not date in seen:
            keys.append(date)
            seen[date] = True
            
    if len(keys) == 0:
        return Response('error date is not stored', status=400)

    ans = list()
    
    ans = {}
    seen = {}
    for date in keys:
        urls = dict[date]
        urls_keys = list(urls.keys())
        for i in range(0, len(urls_keys)): 
            current_url = urls_keys[i]
            if not current_url in seen:
                seen[current_url] = True
                ans[current_url] = urls[current_url]
            else: 
                ans[current_url] += urls[current_url]
    out = []

    urls = list(ans.keys())
    print(len(urls))

    #for i in range(0, len(urls)):
    #    for j in range(i+1, len(urls)): 
    #        if ans[urls[i]] < ans[urls[j]]:
    #            temp = urls[i]
    #            urls[i] = urls[j]
    #            urls[j] = temp
    #    out.append({'url': urls[i], 'count': ans[urls[i]]})
    urls = merge_sort(urls, ans)
    for i in range(0, size): 
        out.append({'query': urls[i], 'count': ans[urls[i]]})
    end = time()
    print("time taken : " + str(round(end - start, 3)) + "s")

    return jsonify({"queries": out})


def merge_sort(array, ans):
    #TODO
    if len(array) > 3:
        a = np.array(array)
        mid = int((len(array) -1) / 2)
        left = a[0:mid]
        right = a[mid:len(array)]
        return arrange(merge_sort(left, ans), merge_sort(right, ans), ans)
    else:
        return bruteForce(array, ans)


def bruteForce(array, ans):
    for i in range(0, len(array)):
        for j in range(i+1, len(array)):
            if ans[array[i]] < ans[array[j]]:
                temp = array[i]
                array[i] = array[j]
                array[j] = temp
    return array


def arrange(left, right, ans):
    left = list(left)
    right = list(right)
    if len(left) > len(right):
        temp = left
        left = right
        right = temp
    index = 0
    while len(left) > 0:
        #print('left', left)
        #print('right',right)
        url = left[0]
        if (index >= len(right) -1):
            right.insert(index, url)
            break        
        while index <= len(right) -1 and ans[url] < ans[right[index]]:
            index+=1
        right.insert(index, url)
        left.remove(url)
        index +=1
    return right        


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