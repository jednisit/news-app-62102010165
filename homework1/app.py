from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote, uses_query
from urllib.request import urlopen
import json

app = Flask(__name__)


newurl = "http://newsapi.org/v2/everything?q={0}&apiKey=2a67ee7b574845e6b12fe659c0f90921"
covidurl = "http://newsapi.org/v2/top-headlines?country=th&q=%E0%B9%82%E0%B8%84%E0%B8%A7%E0%B8%B4%E0%B8%94&apiKey=2a67ee7b574845e6b12fe659c0f90921"
weatherutl = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&lang=th&appid=c7f9a4a41eb61b1113705c085daa4705"
imgurl = "http://openweathermap.org/img/wn/{0}@2x.png"

@app.route('/')
def home():
    # 5 ข่าว Covid-19
    data = urlopen(covidurl).read()
    parsed = json.loads(data)
    covid_new = []
    for i in range(0, 5):
        covid_new.append({"head":parsed['articles'][i]['title'], 
            "content":parsed['articles'][i]['description'], 
            "img":parsed['articles'][i]['urlToImage'], 
            "url":parsed['articles'][i]['url']})

    # สภาพอากาศ ณ เวลานี้ของแต่ละเมือง
    city = request.args.get('city')
    if not city:
        city = "Bangkok"
    weather = get_weather(city)
    return render_template("home.html", news=covid_new, weather=weather)

# สภาพอากาศ
def get_weather(city):
    query_city = convert_to_unicode(city)
    url = weatherutl.format(query_city)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        temperature = parsed['main']['temp']
        description = parsed['weather'][0]['description']
        pressure = parsed['main']['pressure']
        humidity = parsed['main']['humidity']
        wind = parsed['wind']['speed']
        max_min = str(parsed['main']['temp_max']) + "/" + str(parsed['main']['temp_min'])
        city = parsed['name']
        country = parsed['sys']['country']
        img = imgurl.format(parsed['weather'][0]['icon'])

        weather = {'temperature': temperature, 
                   'description': description,
                   'pressure': pressure,
                   'humidity':humidity,
                   'wind':wind,
                   'max_min':max_min,
                   'city': city,
                   'country': country,
                   'img':img
                   }
    return weather

@app.route("/search")
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return render_template("search.html", news=[0,])

    news = get_news(keyword)
    return render_template("search.html", news=news)

def get_news( keyword):
    
    query_keyword = convert_to_unicode(keyword)
    url = newurl.format(query_keyword)
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = [len(parsed['articles'])]
    for i in range(len(parsed['articles'])):
        head = parsed['articles'][i]['title']
        content = parsed['articles'][i]['description']
        link = parsed['articles'][i]['url']
        news.append({"head":head, "content":content, "url":link})
    return news

@app.route("/about")
def about():
    return render_template("about.html")

def convert_to_unicode(txt):
    convert = str(txt.encode())[2:].replace("\\x", "%")
    encode = convert[:len(convert)-1]
    return encode

app.run(debug=True,use_reloader=True)