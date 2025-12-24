import telebot
import requests
import json
from config import token, API

bot = telebot.TeleBot(token)
API = API


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать, я могу помочь узнать о погоде в вашем городе')
    bot.send_message(message.chat.id, 'Напишите свой город:')



@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(message.chat.id, 'Прекрасное фото, но мне нужен город!!!')
    bot.send_message(message.chat.id, 'Напишите свой город:')



@bot.message_handler(content_types=['text'])
def pogoda(message):
    city = message.text.strip().lower()

    pogodka = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru')
    #bot.send_message(message.chat.id, f'Сейчас температуа: {pogodka.json()}') Полная информация о погоде в json объекта

    info_pogoda = json.loads(pogodka.text)

    if pogodka.status_code == 200:

        temp = round(info_pogoda['main']['temp']) # температура
        whether_perevod = info_pogoda['weather'][0]['description'] # description теперь с переводом
        whether_id = info_pogoda['weather'][0]['id'] # определяет колич. осадков по  whether_id
        name_city = info_pogoda['name'] # Выводит название города
        not_good_pogoda = False

        if 200<= whether_id < 700:
            not_good_pogoda = True

        if  not_good_pogoda:
            otvetka = f'В настоящее время в городе {name_city} {temp}°C, {whether_perevod}'
        else:
            otvetka = f'В настоящее время в городе {name_city} {temp}°C, {whether_perevod}, без осадков'


        bot.send_message(message.chat.id, otvetka)



    else:
        bot.send_message(message.chat.id, f'Город указан не верно, проверьте на правильность написание')
        bot.send_message(message.chat.id, 'Повторите повытку!')


bot.polling(none_stop=True)



'''{'coord': {'lon': 135.0928, 'lat': 48.4808}, 
'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}], 
'base': 'stations', 'main': {'temp': -20.11, 'feels_like': -27.11, 'temp_min': -20.11, 'temp_max': -20.11, 'pressure': 1014, 'humidity': 54, 'sea_level': 1014, 'grnd_level': 1005}, 
'visibility': 10000, 'wind': {'speed': 8, 'deg': 230}, 
'clouds': {'all': 0}, 'dt': 1765960885, 
'sys': {'type': 1, 'id': 8867, 'country': 'RU', 'sunrise': 1765925169, 'sunset': 1765955107},
 'timezone': 36000, 'id': 2022890, 'name': 'Khabarovsk', 'cod': 200}'''

# Группы ID с осадками:
# 2xx - грозы
# 3xx - морось
# 5xx - дождь
# 6xx - снег
# 7xx - атмосферные явления (туман, пыль и т.д.)


'''{
    'weather': [{
        'id': 800, 
        'main': 'Clear', 
        'description': 'clear sky',  ← ВОТ ОН!
        'icon': '01n'
    }]
}'''



'''# Ясно/Облачно
    'clear sky': 'ясно',
    'few clouds': 'малооблачно',
    'scattered clouds': 'переменная облачность',
    'broken clouds': 'облачно с прояснениями',
    'overcast clouds': 'пасмурно',
    
    # Туман/Мгла
    'mist': 'лёгкий туман',
    'fog': 'туман',
    'haze': 'дымка',
    'smoke': 'дым',
    
    # Дождь
    'light rain': 'небольшой дождь',
    'moderate rain': 'дождь',
    'heavy intensity rain': 'сильный дождь',
    'very heavy rain': 'очень сильный дождь',
    'extreme rain': 'проливной дождь',
    'freezing rain': 'ледяной дождь',
    'light intensity shower rain': 'небольшой ливень',
    'shower rain': 'ливень',
    'heavy intensity shower rain': 'сильный ливень',
    'ragged shower rain': 'переменный ливень',
    
    # Снег
    'light snow': 'небольшой снег',
    'snow': 'снег',
    'heavy snow': 'сильный снег',
    'sleet': 'мокрый снег',
    'light shower sleet': 'небольшой мокрый снег',
    'shower sleet': 'мокрый снег',
    'light rain and snow': 'дождь со снегом',
    'rain and snow': 'дождь со снегом',
    'light shower snow': 'небольшой снегопад',
    'shower snow': 'снегопад',
    'heavy shower snow': 'сильный снегопад',
    
    # Гроза
    'thunderstorm with light rain': 'гроза с небольшим дождём',
    'thunderstorm with rain': 'гроза с дождём',
    'thunderstorm with heavy rain': 'гроза с сильным дождём',
    'light thunderstorm': 'слабая гроза',
    'thunderstorm': 'гроза',
    'heavy thunderstorm': 'сильная гроза',
    'ragged thunderstorm': 'нерегулярная гроза',
    'thunderstorm with light drizzle': 'гроза с мелким дождиком',
    'thunderstorm with drizzle': 'гроза с изморосью',
    'thunderstorm with heavy drizzle': 'гроза с сильной изморосью','''




# Сейчас -15, сегодня от -14 до -18, осадки не ожидаются
# Что и как надо сделать, что убрать, что добавить
