import requests
from fake_useragent import Useragent

ua = useragent()

with open('proxies.txt', 'r') as file:
    for line in file:
        proxies = line.split(" ")
        ip, port, username, password = proxies.split(':')
        proxies = {
            'https': f'https://{username}:{password}@{ip}:{port}'
        }

def acc_creation(url):
    user_agent = ua.agent()
    headers = {'user-agent:}', user_agent}
    response = request.get(url, headers, proxies=proxies)
    return response 

for proxie in proxies:
    acc_creation('https://ubereats.com')