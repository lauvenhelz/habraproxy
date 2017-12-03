# Habraproxy

Ivelum #1 task: https://github.com/ivelum/job/blob/master/code_challenges/python.md

HTTP-proxy-server to modify Habrahabr pages: after each 6-letter word insert «™» sign.

To start server (127.0.0.1:8232): 

`uwsgi --ini uwsgi.ini`

Habrahabr link: http://habrahabr.ru/company/dsec/blog/258457/

The same page with «™» modifications: http://127.0.0.1:8232/company/dsec/blog/258457/
