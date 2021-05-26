import pytest
import requests
from bs4 import BeautifulSoup

@pytest.fixture(name='confirm')
def button_CONFIRM(url):
    URL = url
    # getting cookies
    response_get = requests.get(URL)
    cookies = response_get.cookies
    html_doc = response_get.text
    soup_get = BeautifulSoup(html_doc, "html.parser")
    # getting FIVE items for checking
    # [['13791', 'ЕР 16104/2В', None, '9045.06', None, None, None, None, None, 'cart'],
    l_candidats = [[ii.string for ii in i.find_all('td')][:4] for i in soup_get.find('tbody').find_all('tr')][:5]

    # adding FIVE items in the CART
    for i in l_candidats:
        data = {'groups': ['ЕР', 'МКН', 'МКС', 'Code', 'Name', 'Ostatok', 'PriceEleton'], 'cart': i[0], 'order': '1'}
        response_post_cost = requests.post(URL + '/groups', cookies=cookies, data=data)

    d_cart = {'order': [str(i) for i in range(1, 6)], 'confirm': '1'}
    data.update(d_cart)                # setting quantity for FIVE chosen items
    response_post_confirm = requests.post(URL + '/groups', cookies=cookies, data=data)

    # l_order = [
    # (['13791', 'ЕР 16104/2В', None, '9045.06'], '1'),
    # (['14750', 'ЕР 16106/2В', None, '9923.28'], '2'),
    # (['14751', 'ЕР 16124/2В', None,'10221.3'], '3'),
    # (['14752', 'ЕР 16126/2В', None, '11141.28'], '4'),
    # (['11694', 'ЕР 1664/1', '3', '6178.44'], '5')]
    l_order = [(a, b) for a, b in zip(l_candidats, d_cart.get('order', None))]

    html_doc = response_post_confirm.text
    soup_post_confirm = BeautifulSoup(html_doc, "html.parser")
    return soup_post_confirm, cookies, l_order

@pytest.fixture(name='send_order')
def test_confirm_send_order(confirm, url):
    URL = url
    soup_post_confirm, cookies, l_order = confirm
    data = {'customer': 'customer_TEST', 'address_to': 'elet@ele.com.ua', 'comment': 'Comment_TEST_Comment'}
    response_post_send = requests.post(URL + '/send', cookies=cookies, data=data)

    html_doc = response_post_send.text
    soup_post_send = BeautifulSoup(html_doc, "html.parser")
    return response_post_send, soup_post_send

@pytest.mark.smoke(reason="text ['ORDER', 'COMMENTS'] on the CONFIRMATION page")
def test_confirm_text_h4(confirm):                                       #text ['ORDER', 'COMMENTS'] on the CONFIRMATION page
    soup_post_confirm, cookies, l_order = confirm
    l_h4_sample = ['ORDER', 'COMMENTS']
    l_h4 = [i.text for i in soup_post_confirm.find_all('h4')]
    assert  l_h4_sample == l_h4

@pytest.mark.smoke(reason="'input' ['customer', 'address_to'] on the CONFIRMATION page")
def test_confirm_input(confirm):                          # 'input' ['customer', 'address_to'] on the CONFIRMATION page
    soup_post_confirm, cookies, l_order = confirm
    l_input_name_sample = ['customer', 'address_to']
    l_input_name = [i['name'] for i in soup_post_confirm.find_all('input')]
    assert l_input_name_sample == l_input_name

@pytest.mark.smoke(reason="columns ['Item', 'Order'] on the CONFIRMATION page")
def test_confirm_columns(confirm):                          #columns ['Item', 'Order'] on the CONFIRMATION page
    soup_post_confirm, cookies, l_order = confirm
    l_column_sample = ['Item', 'Order']
    l_column = [i.text for i in soup_post_confirm.find('table').find('thead').find('tr').find_all('th')]
    assert l_column_sample == l_column


    l_items_sample = [[i[0][1], i[1]] for i in l_order]
    # [['ЕР 16104/2В', '1'], ['ЕР 16106/2В', '2'], ['ЕР 16124/2В', '3'], ['ЕР 16126/2В', '4'], ['ЕР 1664/1', '5']]
    l_items = [[ii.text for ii in i.find_all('td')] for i in soup_post_confirm.find('table').find('tbody').find_all('tr') ]
    assert l_items_sample == l_items

@pytest.mark.smoke(reason="button ['SEND ORDER'] on the CONFIRMATION page")
def test_confirm_button_send(confirm):                      #button ['SEND ORDER'] on the CONFIRMATION page
    soup_post_confirm, cookies, l_order = confirm
    l_buttons_sample = ['SEND ORDER']
    l_buttons = [i.text for i in soup_post_confirm.find_all('button')]
    assert l_buttons_sample == l_buttons

@pytest.mark.smoke(reason="textarea ['comment'] on the CONFIRMATION page")
def test_confirm_textarea(confirm):                         #textarea ['comment'] on the CONFIRMATION page
    soup_post_confirm, cookies, l_order = confirm
    l_textarea_sample = ['comment']
    l_textarea = [i['name'] for i in soup_post_confirm.find_all('textarea')]
    assert l_textarea_sample == l_textarea

@pytest.mark.smoke(reason="send ORDER from the CONFIRMATION page. status_code")
def test_confirm_send_order_status_code(send_order):        #send ORDER from the CONFIRMATION page. status_code
    response_post_send, soup_post_send = send_order
    assert response_post_send.status_code == 200

@pytest.mark.smoke(reason="send ORDER from the CONFIRMATION page. flash")
def test_confirm_send_order_flash(send_order):              # send ORDER from the CONFIRMATION page. flash
    response_post_send, soup_post_send = send_order
    l_text_confirm = [i.string.strip() for i in soup_post_send.find('header').find_all('div')]
    assert l_text_confirm[0]      == '!!!  Your ORDER was SENT  !!!'
    assert l_text_confirm[1][:35] == 'Ostatky was successfully updated on'
    assert l_text_confirm[1][57:] == 'We have used cookies for your identification.'
