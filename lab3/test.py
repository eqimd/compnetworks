from requests import Request
from concurrent.futures import ThreadPoolExecutor

from time import sleep, time

start_time = time()


def do_some_job(n):
    print(n, time()-start_time)
    sleep(2)
    print(n, time()-start_time)


pool = ThreadPoolExecutor(3)
for i in range(3):
    res = pool.submit(do_some_job, (i))


req = '''GET /?1pm = sample & 2pm = &3pm = &4pm = &5pm = HTTP/1.1
Host: localhost: 50000
User-Agent: Mozilla/5.0 (Windows NT 6.1
                         WOW64
                         rv: 11.0) Gecko/20100101 Firefox/11.0
Accept: text/html, application/xhtml+xml, application/xml
q = 0.9, */*
q = 0.8
Accept-Language: en-us, en
q = 0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Referer: http: // localhost: 50000 /?1pm = sample & 2pm = &3pm = &4pm = &5pm =
'''

from urllib.parse import parse_qs

print(parse_qs(req))
