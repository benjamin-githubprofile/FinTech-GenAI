import requests
from fake_useragent import Useragent

ua = useragent()

with open('proxies.txt', 'r') as file:
    for line in file:
        host, port, username, password = line.strip().split(" ")
        ip, port, username, password = proxies.split(':')
        proxies = f"http://{username}:{password}@{host}:{port}"
        
        proxy = {
            "http": proxies,
            "https": proxies
        }

def acc_creation(url):
    user_agent = ua.agent()
    headers = {'user-agent:}', user_agent}
    response = request.get(url, headers, proxies=proxies)
    return response 

for proxie in proxies:
    acc_creation('https://ubereats.com')