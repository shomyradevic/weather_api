from django.shortcuts import render, redirect
from requests import get
from json import load
from django.http import JsonResponse
from datetime import datetime
from .search import search_query
from django.contrib.messages import warning


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
    if request.is_ajax():
        # Point is to get city from pre-downloaded json file and then send that to the url to get temperature
        global API_KEY
        queryID, data = "", {"result": "empty set"}
        q = request.GET.get("query")
        if q:
            data["result"] = search_query(query=q)
        else:
            data["result"] = []
        return JsonResponse(data=data)
    else:
        return redirect(to="homepage")


def detail(request, id: int):
    data = {"result": "", "icon": ""}
    response = get(url="http://api.openweathermap.org/data/2.5/weather?id=" + str(id) + "&APPID=" + API_KEY)
    if response.status_code == 200:
        log(response.text)
        data["result"] = eval(response.text)
        data["icon"] = "http://openweathermap.org/img/w/" + data["result"]["weather"][0]["icon"] + ".png"
        return render(request=request, template_name="weather/detail.html", context={"data": data})
    else:
        warning(request=request, message=eval(response.text)["message"])
        return render(request=request, template_name="weather/homepage.html")


def location(request):
    coo = {"x": None, "y": None, "msg": ""}
    if request.is_ajax():
        coo["x"] = request.GET.get("Latitude")
        coo["y"] = request.GET.get("Longitude")
        if coo["x"] and coo["y"]:
            response = get(
                url="http://api.openweathermap.org/data/2.5/weather?lat=" + 
                str(coo["x"]) + "&lon=" + str(coo["y"]) + "&APPID=" + API_KEY
            )
            return JsonResponse(data={"location": eval(response.text)})
        else:
            coo["msg"] = "Coordinates not found."
        return JsonResponse(data=coo)
    else:
        return redirect(to="homepage")