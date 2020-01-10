from django.shortcuts import render, redirect
from requests import get
from json import load
from django.http import JsonResponse
from .search import search_query
from django.contrib.messages import warning
from .help import process_data, log


API_KEY = ""


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
        return JsonResponse(data=data)
    else:
        return redirect(to="homepage")


def detail(request, id: int):
    data = {
        "icon": "",
        "json": {

        }
    }
    response = get(url="http://api.openweathermap.org/data/2.5/weather?id=" + str(id) + "&APPID=" + API_KEY)
    if response.status_code == 200:
        data["json"] = eval(response.text)
        data["icon"] = "http://openweathermap.org/img/w/" + data["json"]["weather"][0]["icon"] + ".png"
        data = process_data(data=data)
        return render(request=request, template_name="weather/detail.html", context={"data": data})
    else:
        warning(request=request, message=eval(response.text)["message"])
        return render(request=request, template_name="weather/homepage.html")
        # sunrise, sunset, humidity, pressure, wind speed


def location(request):
    coo = {"x": None, "y": None, "msg": ""}
    if request.is_ajax():
        coo["x"] = request.GET.get("Lat")
        coo["y"] = request.GET.get("Lon")
        if coo["x"] and coo["y"]:
            response = get(
                url="http://api.openweathermap.org/data/2.5/weather?lat=" + 
                str(coo["x"]) + "&lon=" + str(coo["y"]) + "&APPID=" + API_KEY
            )
            data = eval(response.text)
            Wimg = "http://openweathermap.org/img/w/" + data["weather"][0]["icon"] + ".png"
            return JsonResponse(data={"data": data, "Wimg": Wimg})
        else:
            coo["msg"] = "Coordinates not found."
        return JsonResponse(data=coo)
    else:
        return redirect(to="homepage")
