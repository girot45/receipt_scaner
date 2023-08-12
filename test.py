import requests
url = "https://lkdr.nalog.ru/"

r = requests.get(url)
print(r.status_code)
print(r.content)
print(r.text)