from django.shortcuts import render
from requests import get
from json import load, loads
from django.http import JsonResponse
from datetime import datetime


API_KEY = ""


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
    queryCity, data = "", {"result": ""}
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + queryCity + "&APPID=" + API_KEY
    response = get(url=url)
    data["result"] = loads(response.text)
    return JsonResponse(data=data)

def city_json(query: str):
    five_cities = []
    with open(file="city.json", mode="r", encoding="utf-8") as json:
        j = load(json)
        json.close()
        for city in j:
            pass