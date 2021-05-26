import requests
import pytest
from bs4 import BeautifulSoup

@pytest.fixture(name="Content_Main_Page")
def content_main_page(url):
    URL = url
    response = requests.get(URL)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

@pytest.mark.smoke(reason="'title' on the MAIN page")
def test_content_main_page_title(Content_Main_Page):          #'title' on the MAIN page
    soup = Content_Main_Page
    assert soup.title.string.strip() == 'ostatky ELETON'

@pytest.mark.smoke(reason="buttons ['SEND ORDER'] on the MAIN page")
def test_content_main_page_buttons(Content_Main_Page):        #buttons ['SEND ORDER'] on the MAIN page
    l_buttons_sample = ['CHECK', 'cart']
    soup = Content_Main_Page
    l_buttons = [i.text for i in soup.find_all('button') if i.text != 'cart']
    l_buttons += ['cart' if any([i.text == 'cart' for i in soup.find_all('button')]) else []]
    assert l_buttons_sample == l_buttons

@pytest.mark.smoke(reason="anchors on the MAIN page")
def test_content_main_page_anchors(Content_Main_Page):        #anchors on the MAIN page
    soup = Content_Main_Page
    l_sample_link = ['/', '/', '/map', '/partners', '/price', '/catalog', '/ostatkyxls', 'mailto:eleton.s@ukr.net', '/']
    l_link = [i.get('href') for i in soup.find_all('a')]
    assert l_sample_link == l_link

@pytest.mark.smoke(reason="checkboxes on the MAIN page")
def test_content_main_page_checkboxes(Content_Main_Page):      #checkboxes on the MAIN page
    soup = Content_Main_Page
    l_sample_checkbox = ['Дин', 'ЕР', 'Козырёк', 'Кронштейны', 'Лицевые', 'МКН', 'МКС', 'Монтажные',\
                         'Пластины', 'Профиль', 'Прочее', 'СМ', 'Скоба', 'Стойка', 'Стойки', 'Усилитель',\
                         'Устройства', 'Цоколя', 'Экраны', 'Ячейки', 'Code', 'Group', 'Name', 'Ostatok',\
                         'PriceEleton', 'PriceP', 'PriceP1', 'PriceP2', 'PriceP3']
    l_checkbox = [i['value'] for i in soup.find_all('input')]
    assert l_sample_checkbox == l_checkbox

@pytest.mark.smoke(reason="checkboxes 'checked' on the MAIN page")
def test_content_main_page_checkboxes_checked(Content_Main_Page):  #checkboxes 'checked' on the MAIN page
    soup = Content_Main_Page
    l_sample_checkbox_checked = ['ЕР', 'МКН', 'МКС', 'Code', 'Name', 'Ostatok', 'PriceEleton']
    l_checkbox_checked = [i['value'] for i in soup.find_all('input') if i.get('checked', None) != None]
    assert l_sample_checkbox_checked == l_checkbox_checked


