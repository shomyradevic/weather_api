from django.urls import path
from .views import homepage, search, detail, location


urlpatterns = [
    path("", homepage, name="homepage"),
    path("search/", search, name="search"),
    path("search/<int:id>/", detail, name="detail"),
    path("location/", location, name="location")
]