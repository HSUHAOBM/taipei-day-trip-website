import requests

import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

partnerkey=config.get('tappay', 'partner_key')   
# print("partnerkey",partnerkey)




url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
def paybyprime(getorderdata):
    paybyprimedata={}

    # print(getorderdata)
    paybyprimedata={
    "partner_key": partnerkey,
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
            "x-api-key": partnerkey}

    r = requests.post(url, headers = my_headers,json=paybyprimedata)
    # print(r.status_code)
    return r.json()


