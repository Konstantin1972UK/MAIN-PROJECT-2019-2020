import requests
import pytest
from bs4 import BeautifulSoup

@pytest.fixture(name="Content_Partner_Page")
def content_text_map_page(url):
    URL= url
    response = requests.get(URL + '/partners')
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

@pytest.mark.smoke(reason="'title' on the PARTNER page")
def test_content_partner_page_title(Content_Partner_Page):                #'title' on the PARTNER page
    soup = Content_Partner_Page
    assert soup.title.string.strip() == 'partner ELETON'

@pytest.mark.smoke(reason="text '<p></p>' on the PARTNER page")
def test_content_partner_page_text_p(Content_Partner_Page):         #text '<p></p>' on the PARTNER page
    soup = Content_Partner_Page
    l_sample_text_p = ['Для роботи з постійними покупцями ТОВ "ЕЛЕТОН" використовує "Модуль ПАРТНЕР для 1С".', 'Ми пропонуємо нашим покупцям скористатися можливістю:', None, None]
    l_text_p = [i.string for i in soup.find_all('p')]
    assert l_text_p == l_sample_text_p

@pytest.mark.smoke(reason="text '<h2></h2>' on the PARTNER page")
def test_content_partner_page_text_h2(Content_Partner_Page):        # text '<h2></h2>' on the PARTNER page
    soup = Content_Partner_Page
    l_sample_text_h2 = ['Програма "ПАРТНЕР"', 'Участники програми:']
    l_text_h2 = [i.string for i in soup.find_all('h2')]
    assert l_text_h2 == l_sample_text_h2

@pytest.mark.smoke(reason="text '<li></li>' on the PARTNER page")
def test_content_partner_page_text_li(Content_Partner_Page):        # text '<li></li>' on the PARTNER page
    soup = Content_Partner_Page
    l_sample_text_li = [None, None, None, "Download 'price.zip'", 'Download CATALOG', "Download 'ostatky.xls'",\
                        ' eleton.s@ukr.net', 'Info', 'доступ до інформації про залишки товару в реальному часі по основному складу металоконструкцій',\
                        'доступ до інформації по своєму підприємству: рахунки-фактури, видаткові накладні',\
                        'можливість формувати рахунки-фактури та "резервувати" по ним металоконструкції',\
                        'заносити в "заявку на виробництво" товар, якого немає на складі', None, None]
    l_text_li = [i.string for i in soup.find_all('li')]
    assert l_text_li == l_sample_text_li

@pytest.mark.smoke(reason="links on the PARTNER page")
def test_content_partner_page_text_li(Content_Partner_Page):        # links on the PARTNER page
    soup = Content_Partner_Page
    l_sample_link = ['/', '/', '/map', '/partners', '/price', '/catalog', '/ostatkyxls', 'mailto:eleton.s@ukr.net', '/',\
                     '/partner_info', 'mailto:eleton.s@ukr.net', '/partner_info_eliton', '/partner_info_lina']
    l_link = [i.get('href') for i in soup.find_all('a')]
    assert l_link == l_sample_link

@pytest.mark.smoke(reason="parner's links are available on the PARTNER page")
def test_content_partner_page_text_li(url):                         #parner's links are available on the PARTNER page
    l_partner_link = ['/partner_info_eliton', '/partner_info_lina']
    for i in l_partner_link:
        URL = url
        response_link = requests.get(URL + i)
        if i != '/partner_info_eliton':                   # exceptions
            assert response_link.status_code == 200
        else:
            assert response_link.status_code == 403

