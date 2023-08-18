---
marp: true

---
# Telegrma Bot API

---
**API** - Application Programming Interface (программный интерфейс приложения) - набор правил взаимодействия с каким-либо сервисом с помощью программных запросов. Это описание того, как можно обратиться к сервису и какие ответы от него получить.

![bg left](file/weather.png)

---
![bg right](file/example_json.png)
JSON (JavaScript Object Notation) - простой формат обмена данными, удобный для чтения и написания как человеком, так и компьютером.

---
![bg fit](file/api_server.png)

---

![bg fit](file/handler_filter.png)


---
# Взаимодействие через браузер

`https://api.telegram.org/bot<token>/getMe` - информация о боте
`https://api.telegram.org/bot<token>/getUpdates` - проверка апдейтов за ближайшее время (история взаимодействий с ботом)
`https://api.telegram.org/bot<token>/sendMessage?chat_id=<чат-id из getMe>&text=Привет!` - отправка сообщения

---
**Немного котиков**

```python
import requests
import time

API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
BOT_TOKEN = 'BOT TOKEN HEAR'
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('
offset = -2
counter = 0

while counter < 100:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()
    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
    time.sleep(1)
    counter += 1

```
