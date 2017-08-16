import requests

def get_tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

session = get_tor_session()
print(session.get("http://httpbin.org/ip").text) #tor ip
print(requests.get("http://httpbin.org/ip").text) #normal ip
