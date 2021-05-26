import requests
import pytest
from bs4 import BeautifulSoup

@pytest.mark.smoke(reason="get '/send' without cookies")
def test_send_get(url):                                                      # get '/send' without cookies
    URL = url
    response_get = requests.get(URL + '/send')
    cookies = response_get.cookies
    assert response_get.status_code == 200

@pytest.mark.smoke(reason="get  '/send' with cookies")
def test_send_get_cookies(url):                                              # get  '/send' with cookies
    URL = url
    response_get = requests.get(URL + '/send')
    cookies = response_get.cookies
    response_get_cookies = requests.get(URL + '/send', cookies=cookies)
    assert response_get_cookies.status_code == 200

@pytest.mark.smoke(reason="post 'empty' data '/send' without cookies")
def test_send_post(url):                                                      #post 'empty' data '/send' without cookies
    URL = url
    response_post_empty = requests.post(URL + '/send')
    assert response_post_empty.status_code == 200

@pytest.mark.smoke(reason="post 'empty' data '/send' with cookies")
def test_send_post_cookies(url):  # post 'empty' data '/send' without cookies
    URL = url
    response_get = requests.get(URL + '/send')
    cookies = response_get.cookies
    response_post_empty_cookies = requests.post(URL + '/send', cookies=cookies)# post 'empty' data '/send' with cookies
    assert response_post_empty_cookies.status_code == 200