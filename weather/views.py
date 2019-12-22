from django.shortcuts import render


def homepage(request):
    return render(request=request, template_name='weather/homepage.html')


def test():
    from requests import get
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_API_KEY"
    response = get(url=url)