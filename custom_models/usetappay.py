import requests
url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
def paybyprime(getorderdata):
    paybyprimedata={}

    # print(getorderdata)
    paybyprimedata={
    "partner_key": "partner_bKqPoStmWHi1G8cOOAqwRUVPmfxBE4pkSDhUdJ3gXraBUGWo1QOCsbYh",
    "prime": getorderdata["prime"],
    "amount": getorderdata["order"]["price"],
    "merchant_id": "haobmbm_ESUN",
    "details": "Some item",
    "cardholder": {
        "phone_number":getorderdata["order"]["contact"]["phone"],
        "name":getorderdata["order"]["contact"]["name"],
        "email":getorderdata["order"]["contact"]["email"],
        }
    }    
    # print("paybyprimedata",paybyprimedata)

    my_headers = {"Content-Type": "application/json",
            "x-api-key": "partner_bKqPoStmWHi1G8cOOAqwRUVPmfxBE4pkSDhUdJ3gXraBUGWo1QOCsbYh"}

    r = requests.post(url, headers = my_headers,json=paybyprimedata)
    # print(r.status_code)
    return r.json()


