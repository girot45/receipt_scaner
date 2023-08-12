import json
import pprint
from datetime import datetime

import requests

from read_qr import decode_qr_code
from config import INPUT_DATE_FORMATE, OUTPUT_DATE_FORMATE

img = "img_3.png"
decoded_data = decode_qr_code(img)
if decoded_data is None:
    print("Неправильное фото чека")
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
                            INPUT_DATE_FORMATE).strftime(OUTPUT_DATE_FORMATE))
    print(receipt["totalSum"]/100)
    table = []
    for item in receipt["items"]:
        row = [1,item['name'], item['price']/100,item['quantity'],item['sum']/100 ]
        print(f"Стоимость: {item['price']/100} | Кол-во: "
              f"{item['quantity']} | Сумма: {item['sum']/100} | "
              f"Название: {item['name']}")
    #pprint.pprint(receipt_info)

