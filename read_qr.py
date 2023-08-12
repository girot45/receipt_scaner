import cv2
from pyzbar.pyzbar import decode

def decode_qr_code(image_path):
    # Преобразование изображения в оттенки серого
    print(image_path)
    gray_image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2GRAY)

    # Поиск QR-кодов на изображении
    decoded_object = decode(gray_image)
    print(decoded_object)
    if len(decoded_object) != 1:
        return None
    else:
        return decoded_object[0].data.decode('utf-8')



