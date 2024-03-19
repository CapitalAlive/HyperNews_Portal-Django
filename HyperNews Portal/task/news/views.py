from django.shortcuts import render, redirect
from django.conf import settings
import json
from . import forms
from datetime import datetime


def index(request):
    return redirect("news_url")


def news_details(request, link):
    file_path = settings.NEWS_JSON_PATH
    with open(file_path) as file:
        _news = json.load(file)
    news_dict = next((item for item in _news if item.get('link') == link), None)
    return render(request, "news_details.html", {"news_dict": news_dict})


def news(request):

    file_path = settings.NEWS_JSON_PATH
    with open(file_path) as file:
        news_list = json.load(file)

    if request.GET.get("q"):
        news_list = [article for article in news_list if request.GET.get("q").lower() in article['title'].lower()]
    dates_list = set(date.get("created")[:10] for date in news_list)
    dates_list = sorted(dates_list, reverse=True)
    data = [{date: []} for date in dates_list]
    for date in data:
        for article in news_list:
            if article["created"][:10] == list(date.keys())[0]:
                date[list(date.keys())[0]].append(article)
    for date_dict in data:
        for date, articles in date_dict.items():
            articles.sort(key=lambda x: x['title'])

    return render(request, "news.html", {"data": data})


def create_news(request):
    if request.method == "GET":
        return render(request, "create_news.html", {"form": forms.NewArticle})
    elif request.method == "POST" and forms.NewArticle(request.POST).is_valid():
        with open(settings.NEWS_JSON_PATH) as file:
            news_list = json.load(file)
        existing_links = {x["link"] for x in news_list}
        link = max(existing_links) + 1 if existing_links else 0
        news_list.append(
            {'created': str(datetime.now())[:19],
             'text': request.POST['text'],
             'title': request.POST["title"],
             'link': link})
        with open(settings.NEWS_JSON_PATH, "w") as file:
            json.dump(news_list, file)
    return redirect("news_url")
