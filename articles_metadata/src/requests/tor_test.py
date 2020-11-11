import requests
import json
from stem import Signal
from stem.control import Controller
from lxml.html import fromstring
import requests
from itertools import cycle
import traceback


""" def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9150',
                       'https': 'socks5://127.0.0.1:9150'}
    return session

session = get_tor_session()
print(session.get("http://dx.doi.org/10.1093/llc/fqq027").text)
# Make a request through the Tor connection
# IP visible through Tor
# signal TOR for a new connection 
def renew_connection():
    with Controller.from_port(port = 9151) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM) """

""" url = 'https://httpbin.org/ip'
proxies = {
    "http": 'http://209.50.52.162:9050', 
    "https": 'http://209.50.52.162:9050'
}
response = requests.get(url,proxies=proxies)
print(response.json()) """

# not working! proxies added manually
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


#If you are copy pasting proxy ips, put in the list below
proxies = ['111.92.164.249:47612', '1.32.59.217:47045', '195.7.8.10:80', '81.12.119.169:8080', '161.202.226.194:8123', '157.230.32.137:8080', '128.0.179.234:41258']
# proxies = get_proxies()
proxy_pool = cycle(proxies)

url = 'https://httpbin.org/ip'
for i in range(1,11):
    #Get a proxy from the pool
    proxy = next(proxy_pool)
    print(proxy)
    print("Request #%d"%i)
    try:
        response = requests.get(url,proxies={"http": proxy, "https": proxy})
        print(response.json())
    except:
        #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
        #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
        print("Skipping. Connnection error")