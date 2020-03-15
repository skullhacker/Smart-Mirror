import requests


class Weather:
    '''
    usecase
    >>> w = Weather("1271715", "9864a219384ffd7d670f6fa0ad93c653")
    >>> w.getWeather()&APPID=
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
                "humidity": str(int(res["main"]["humidity"])),
                "description": res["weather"][0]["description"]}


if __name__ == "__main__":
    w = Weather("1271715", "9864a219384ffd7d670f6fa0ad93c653")
    try:
        d = w.getWeather()
        print("Weather = " + d["weather"])
        print("Temperature = " + d["temperature"])
        print("Humidity = " + d["humidity"])
        print("description = " + d["description"])
    except ValueError:
        print("invalid response")
