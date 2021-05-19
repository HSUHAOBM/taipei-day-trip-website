import requests

def apiget(id):
    url="http://3.18.249.2:3000/api/attraction/"+str(id)
    list_of_dicts = requests.get(url, verify=False).json()
    apigetdata={"id": id
          ,"name":list_of_dicts['data']['name']
          ,"address":list_of_dicts['data']['address']
          ,"image":"http://" +list_of_dicts['data']['images'][0].split('http://')[1].split(',')[0]}
    return apigetdata

