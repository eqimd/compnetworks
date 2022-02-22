### Задание 1
1. Мой браузер использует HTTP1.1, сервер тоже
2. Accept-Language: en-US,en. Так же предоставляются доступные кодировки,
в принципе доступные форматы (text/html, application/xhtml+xml, ...),
и user-agent, конечно, по которому можно определить браузер и даже устройство
3. Internet Protocol Version 4, Src (мой): 192.168.0.170, Dst (сервера): 128.119.245.12
4. 200 OK со страницы, и еще 404 Not Found с /favicon.ico
5. Last-Modified: Tue, 22 Feb 2022 06:59:01 GMT
6. File Data: 128 bytes и еще File Data: 209 bytes которые в /favicon.ico

![task 1 screenshot](task1_screen.png)

### Задание 2
1. Нет, этой строчки нету
2. Да, он вернулся явно, потому что есть Line-based text data
3. If-Modified-Since: Tue, 22 Feb 2022 06:59:01 GMT, это значение Last-Modified
4. 304 Not Modified; нет, не вернул

Чтоб не чистить куки в основном Firefox браузере, я просто скачал Chromium,
поэтому там другой User-Agent :)

![task 2 screenshot](task2_screen.png)

### Задание 3
1. Один GET-запрос. 34-й пакет содержит сообщение GET.
2. 36-й пакет.
3. 2 Reassembled TCP Segments
4. Есть информация о номерах пакетов, в которых содержится контент, и размер контента в пакете.

![task 3 screenshot](task3_screen.png)

### Задание 4
1. Три GET-запроса
    * GET /wireshark-labs/HTTP-wireshark-file4.html

        Host: gaia.cs.umass.edu

    * GET /pearson.png

        Host: gaia.cs.umass.edu

    * GET /8E_cover_small.jpg

        Host: kurose.cslash.net

2. Последовательно, потому что GET к первой картинке был в 8м пакете, ответ был
получен в 10 пакете, и при этом следующий GET ко второй картинке был в 16м пакете,
т.е. сначала ожидался ответ от первого GET-а, а уже потом формировался второй.

![task 4 screenshot](task4_screen.png)

### Задание 5
1. 401 Unathorized
2. Authorization: Basic d2lyZXNoYXJrLXN0dWRlbnRzOm5ldHdvcms=
    Credentials: wireshark-students:network

![task 5 screenshot](task5_screen.png)