import requests
import pytest
from bs4 import BeautifulSoup

@pytest.fixture(name="Content_Map_Page")
def content_map_page(url):
    URL = url
    response = requests.get(URL + '/map')
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

@pytest.mark.smoke(reason="'title' on the MAP page")
def test_content_map_page_title(Content_Map_Page):               #'title' on the MAP page
    soup = Content_Map_Page
    assert soup.title.string.strip() == 'map ELETON'

@pytest.mark.smoke(reason="text '<p></p>' on the MAP page")
def test_content_map_page_text_p(Content_Map_Page):              #text '<p></p>' on the MAP page
    soup = Content_Map_Page
    l_sample_text_p = ['Пн Вт Ср Чт Пт ', '8.00 - 12.00 | обідня перерва | 13.00 - 17.00', 'з 12:00 до 13:00', 'з 8:30 до 11:45', 'з 13:00 до 16:45', None]
    l_text_p = [i.string for i in soup.find_all('p')]
    assert l_text_p == l_sample_text_p

@pytest.mark.smoke(reason="text '<h2></h2>' on the MAP page")
def test_content_map_page_text_h2(Content_Map_Page):               #text '<h2></h2>' on the MAP page
    soup = Content_Map_Page
    l_sample_text_h2 = ['ТОВ "ЕЛЕТОН"']
    l_text_h2 = [i.string for i in soup.find_all('h2')]
    assert l_text_h2 == l_sample_text_h2

@pytest.mark.smoke(reason="text '<h4></h4>' on the MAP page")
def test_content_map_page_text_h4(Content_Map_Page):                #text '<h4></h4>' on the MAP page
    soup = Content_Map_Page
    l_sample_text_h4 = ['Обідня перерва', 'Час відвантаження зі складу']
    l_text_h4 = [i.string for i in soup.find_all('h4')]
    assert l_text_h4 == l_sample_text_h4

@pytest.mark.smoke(reason="'GOOGLE map' on the MAP page")
def test_content_map_page_text_map(Content_Map_Page):                 #'GOOGLE map' on the MAP page
    soup = Content_Map_Page
    address_sample = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2543.469933916664!2d30.48455091594241!3d50.39507909923392!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x40d4c8d072586b3b%3A0xa159b1d8caf1bc71!2z0JXQm9CV0KLQntCdINCi0J7Qkg!5e0!3m2!1sru!2sua!4v1597213571726!5m2!1sru!2sua"
    address = soup.find_all('iframe')[0]['src']
    assert address == address_sample

@pytest.mark.smoke(reason="'GOOGLE map' is available on the MAP page")
def test_content_map_page_text_map_available(Content_Map_Page):       #'GOOGLE map' is available on the MAP page
    soup = Content_Map_Page
    address = soup.find_all('iframe')[0]['src']
    response_address = requests.get(address)
    print(address)
    assert response_address.status_code == 200







