from django.urls import path
from .views import homepage, search, detail


urlpatterns = [
    path("", homepage, name="homepage"),
    path("search/", search, name="search"),
    path("search/<int:id>/", detail, name="detail")
]