from django.urls import path
from .views import homepage, search


urlpatterns = [
    path("", homepage, name="homepage"),
    path("search/", search, name="search")
]