from itertools import cycle
from bs4 import BeautifulSoup as bs
import requests
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from datetime import datetime
from kivy.clock import Clock
from pathlib import Path
# Window.fullscreen = True
# Window.size = (1920, 1080)


class Weather:
    '''
    usecase
    >>> w = Weather("1271715", "9864a219384ffd7d670f6fa0ad93c653")
    >>> w.getWeather()
    '''

    def __init__(self, cityid, appid):
        self.url = ('https://api.openweathermap.org/data/2.5/weather?id=' +
                    cityid + '&APPID=' + appid)

    def getWeather(self):
        res = requests.get(self.url)
        if res.status_code != 200:
            raise ValueError
        res = res.json()
        return {"weather": res["weather"][0]["icon"],
                "temperature": str(int(res["main"]["temp"] - 273.15)) + "°",
                "humidity": str(int(res["main"]["humidity"])) + "%",
                "description": res["weather"][0]["description"]}


class News:

    def __init__(self):
        url = 'https://inshorts.com/en/read'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError
        soup = bs(response.text, features="html5lib")
        self.headlines = soup.find_all(attrs={"itemprop": "headline"})
        self.headline = cycle(self.headlines)

    def getheadline(self):
        return next(self.headline).text


def gettime():
    dt = datetime.now()
    date = dt.strftime("%d %B %Y")
    day = dt.strftime("%A")
    time = dt.strftime("%I:%M %p")
    return time, day, date


class Widgets(AnchorLayout):
    # settime_obj = ObjectProperty()
    # setdate_obj = ObjectProperty()
    # setday_obj = ObjectProperty()
    # settemp_obj = ObjectProperty()
    # sethumidity_obj = ObjectProperty()
    # setnews_obj = ObjectProperty()
    # setimage_obj = ObjectProperty()
    # setdescription_obj = ObjectProperty()
    # settime = StringProperty()
    # setdate = StringProperty()
    # setday = StringProperty()
    # settemp = StringProperty()
    # sethumidity = StringProperty()
    # setnews = StringProperty()
    # setimage = ObjectProperty()
    # setdescription = StringProperty()

    def __init__(self):
        self.event_method = None
        super().__init__()
        self.set_constructor()
        self.event_time = Clock.schedule_interval(self.set_time, 0.5)
        self.event_constructor = Clock.schedule_interval(
            self.set_constructor, 3600)

    def set_time(self, *args):
        time, day, date = gettime()
        self.ids.time.text = time
        self.ids.day.text = day
        self.ids.date.text = date

    def set_constructor(self, *args):
        if self.event_method:
            self.event_method.cancel()
        while(True):
            try:
                self.weather = Weather(
                    "1271715", "9864a219384ffd7d670f6fa0ad93c653")
                self.news = News()
                break
            except Exception as e:
                print(e)
        self.event_method = Clock.schedule_interval(self.set_methods, 7)

    def set_methods(self, *args):
        while True:
            try:
                d = self.weather.getWeather()
                self.ids.news.text = self.news.getheadline()
                print(self.ids.news.text)
                break
            except Exception as e:
                print(e)
        weather_image = "assets\\" + d["weather"] + ".png"
        if not Path(weather_image).is_file():
            weather_image = 'assets\\black.png'
        self.ids.temp.text = d["temperature"]
        self.ids.description.text = d["description"]
        self.ids.humidity.text = "Humidity: " + d["humidity"]
        self.ids.image.source = weather_image


class SmartMirror(App):
    def build(self):
        return Widgets()


if __name__ == "__main__":
    # print(gettime())
    SmartMirror().run()
