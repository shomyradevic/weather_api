from django.shortcuts import render
from requests import get
from json import load, loads
from django.http import JsonResponse
from datetime import datetime
from time import perf_counter


API_KEY = ""
#url = "http://api.openweathermap.org/data/2.5/weather?id=" + queryID + "&APPID=" + API_KEY


def log(value: str):
    with open(file="log.log", mode="a", encoding="utf-8") as f:
        f.write(str(datetime.now()) + " - " + value + "\n")
        f.close()


def set_key():
    global API_KEY
    with open(file="config.json", mode="r", encoding="utf-8") as f:
        json_cont = load(f)
        API_KEY = json_cont["API_KEY"]
        f.close()


def homepage(request):
    return render(request=request, template_name='weather/homepage.html')


def search(request):
    # Point is to get city from pre-downloaded json file and then send that to the url to get temperature
    global API_KEY
    queryID, data = "", {"result": "empty set"}
    q = request.GET.get("query")
    if q:
        data["result"] = city_json(query=q)
    else:
        data["result"] = []
    return JsonResponse(data=data)


def city_json(query: str):
    five_cities = [] # list of dicts: id, name
    added = []
    with open(file="city.json", mode="r", encoding="utf-8") as json:
        # maybe open file immediately when run server
        j = load(json)
        json.close()
        for city in j:
            cn = city["name"]
            if cn.lower().find(query, 0, len(cn)) >= 0 and cn not in added:
                added.append(cn)
                five_cities.append(dict({"id": city["id"], "name": city["name"]}))
            if len(five_cities) == 5:
                return five_cities
    return five_cities
