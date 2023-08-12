import json
import os
import tempfile
from datetime import datetime

import requests
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import INPUT_DATE_FORMATE, OUTPUT_DATE_FORMATE
from read_qr import decode_qr_code

app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"),
          name="templates")
templates = Jinja2Templates(directory="templates")


# Ваша функция для создания данных таблицы
def create_table_data(img):
    # Возвращает список списков с данными
    decoded_data = decode_qr_code(img)
    if decoded_data is None:
        print("Неправильное фото чека")
        return []
    else:

        url = "https://proverkacheka.com/api/v1/check/get"
        data = {
            "token": "23306.aCEXzF1zJg260dfSp",
            "qrraw": decoded_data
        }

        resp = requests.post(url, data=data)
        receipt_info = json.loads(resp.text)
        # pprint.pprint(receipt_info)

        receipt = receipt_info["data"]["json"]

        print(datetime.strptime(receipt['dateTime'],
                                INPUT_DATE_FORMATE).strftime(
            OUTPUT_DATE_FORMATE))
        print(receipt["totalSum"] / 100)
        table = []
        for item in receipt["items"]:
            row = ["1", item['name'], str(item['price'] / 100),
                   str(item['quantity']), str(item['sum'] / 100)]
            print(f"Стоимость: {item['price'] / 100} | Кол-во: "
                  f"{item['quantity']} | Сумма: {item['sum'] / 100} | "
                  f"Название:"
                  f" {item['name']}")
            table.append(row)
        print(table)
        return table


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})


@app.post("/get_table_data")
async def get_table_data(file: UploadFile = File(...)):
    img_data = await file.read()  # Чтение данных изображения в виде байтов

    # Создаем временный файл и записываем в него байты изображения
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_filename = temp_file.name
        temp_file.write(img_data)

    try:
        data = create_table_data(temp_filename)  # Используем вашу функцию для создания данных
        return data
    finally:
        os.remove(temp_filename)
