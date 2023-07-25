import pytesseract
import cv2 
import re
import fitz
import base64
import requests
from io import BytesIO
from datetime import datetime
from django_training.settings import STATIC_URL

def pymupdf(*, pdf_file: str):
    # pdf_invoice = "invoice-sample.pdf"
    response = requests.get(pdf_file)
    opened_file = fitz.open(stream=BytesIO(response.content))
    # page = opened_file.load_page(0)
    # pix = page.get_pixmap()
    # output = "invoice-sample-test.jpg"
    # pix.save(output)

    for page in opened_file:
        # a = page.firstAnnot
        # while a:
        #     ap = a._getAP()
        #     ap = ap.replace(b"\ns", b"\nn")
        #     a._setAP(ap)
        #     a = a.next
        # Matrix(zoom-x, zoom-y): zoom by direction
        # matrix = fitz.Matrix(1.21-3.6, 1.21-3.6), resolution: 720x1018 - 2142x3031
        # pix = page.getPixmap(alpha=False, matrix=fitz.Matrix(300/72, 300/72))
        pix = page.getPixmap(alpha=False, matrix=fitz.Matrix(2, 2))
        pix.save(STATIC_URL + "invoice-sample.png")

    # with open("invoice-sample.pdf", "rb") as pdf_file:
    #     encoded_string = base64.b64encode(pdf_file.read())
        
    # imgdata = base64.b64decode(encoded_string)
    # filename = 'invoice-sample-test.jpg'

    # with open(filename, 'wb') as f:
    #     f.write(imgdata)

    # img = cv2.imread("invoice-sample.jpg")
    img = cv2.imread(STATIC_URL + "invoice-sample.png")
    # cv2.imshow('ImageWindow', img)
    # cv2.waitKey()
    extracted_text = pytesseract.image_to_string(img)
    factored_text = [x for x in extracted_text.split('\n') if x not in ['', ' ']]
    date_pattern = "([0]?[1-9]|[1|2][0-9]|[3][0|1])[./-]([0]?[1-9]|[1][0-2])[./-]([0-9]{4}|[0-9]{2})$"
    amount_pattern = "Amount Due"
    id_pattern = "Invoice #"
    result = {}
    for i in factored_text:
        date = re.findall(date_pattern, i)
        amount = i if amount_pattern in i else None
        id_invoice = i if id_pattern in i else None
        if date: 
            result['date'] = '/'.join(date[0])
            result['date'] = datetime.strptime(result['date'], "%d/%m/%Y").strftime("%Y-%m-%d")
        if amount: 
            result['amount'] = i[i.index("$"):]
            result['amount'] = result['amount'].replace(",", ".")
        if id_invoice:
            result['number'] = i.split()[-1]
    return result
