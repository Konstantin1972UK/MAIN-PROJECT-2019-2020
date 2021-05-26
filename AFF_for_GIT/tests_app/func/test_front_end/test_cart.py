import pytest
import requests
from bs4 import BeautifulSoup

@pytest.fixture(name='cart')
def get_to_Cart(url):
    URL = url
    # adding ONE item to CART
    response_get = requests.get(URL)
    cookies = response_get.cookies
    html_doc = response_get.text
    soup_get = BeautifulSoup(html_doc, "html.parser")
    # five items for checking
    # [['13791', 'ЕР 16104/2В', None, '9045.06', None, None, None, None, None, 'cart'],
    l_candidats = [[ii.string for ii in i.find_all('td')][:4] for i in soup_get.find('tbody').find_all('tr')][:5]

    first_item_code = l_candidats[0][0]
    data_post = {'groups': ['ЕР', 'МКН', 'МКС','Code', 'Name', 'Ostatok', 'PriceEleton'], 'cart': first_item_code, 'order': '1'}

    response_post = requests.post(URL + '/groups', cookies=cookies, data=data_post)
    html_doc = response_post.text
    soup_post = BeautifulSoup(html_doc, "html.parser")
    return soup_post, l_candidats, cookies

@pytest.mark.smoke(reason="'Cart' and 'Delete' buttons")
def test_cart_buttons(cart):                                    #"'Cart' and 'Delete' buttons"
    soup_post, l_candidats, cookies = cart
    l_buttons_sample = ['CHECK', 'DELETE', 'CONFIRM', 'Cost in  PriceEleton', 'cart']
    l_buttons = [i.text for i in soup_post.find_all('button') if i.text != 'cart']
    l_buttons += ['cart' if any([i.text=='cart' for i in soup_post.find_all('button')]) else []]
    assert l_buttons_sample == l_buttons                        # checking buttons ['SEND ORDER'] on the page

@pytest.mark.smoke(reason="'CASTOMER ORDER' on the page")
def test_cart_text_h4(cart):                                     #'CASTOMER ORDER' on the page
    soup_post, l_candidats, cookies = cart
    l_h4 = [i.string for i in soup_post.find_all('h4')]
    assert l_h4 == ['CASTOMER ORDER', 'OSTATKY ELETON']

@pytest.mark.smoke(reason="ADD FIVE items in the CART and DELETE ONE")
def test_cart_add_five_items_del_one(url, cart):                      #ADD FIVE items in the CART and DELETE ONE
    URL =url
    soup_post, l_candidats, cookies = cart
    for i in l_candidats:
        data = {'groups': ['ЕР', 'МКН', 'МКС', 'Code', 'Name', 'Ostatok', 'PriceEleton'], 'cart': i[0], 'order': '1'}
        response_post = requests.post(URL + '/groups', cookies=cookies, data=data)

    html_doc = response_post.text
    soup_post = BeautifulSoup(html_doc, "html.parser")

    # [['13791', 'ЕР 16104/2В', None, '9045.06', None, 'DELETE']]
    l_selected = [[ii.string for ii in i.find_all('td')][:4] for i in soup_post.find('tbody').find_all('tr')]
    assert sorted(l_selected, key=lambda x: x[0]) == sorted(l_candidats, key=lambda x: x[0])      #all five in the cart

    # deleting ONE items from CART
    # quantity for the list of ORDERS
    l_quantity = []
    for i in soup_post.find('tbody').find_all('tr'):
        for ii in i.find_all('td'):
            for iii in ii.find_all('input'):
                l_quantity.append(iii['value'])
    items_del = l_selected[0][0]   #FIRST item for deleting

    data_delete ={'groups': ['ЕР', 'МКН', 'МКС', 'Code', 'Name', 'Ostatok', 'PriceEleton'], 'delete': items_del, 'order': l_quantity}
    response_delete = requests.post(URL + '/groups', cookies=cookies, data=data_delete)
    html_doc = response_delete.text
    soup_del = BeautifulSoup(html_doc, "html.parser")

    l_selected_del = [[ii.string for ii in i.find_all('td')][:4] for i in soup_del.find('tbody').find_all('tr')]
    assert sorted(l_selected_del, key=lambda x: x[0]) == sorted(l_candidats[1:], key=lambda x: x[0])  # FOUR in the cart

@pytest.mark.smoke(reason="button COST")
def test_button_COST(url, cart):             #"button COST"
    URL = url
    soup_post, l_candidats, cookies = cart

    # adding FIVE items in the CART
    for i in l_candidats:
        data = {'groups': ['ЕР', 'МКН', 'МКС', 'Code', 'Name', 'Ostatok', 'PriceEleton'], 'cart': i[0], 'order': '1'}
        response_post_cost = requests.post(URL + '/groups', cookies=cookies, data=data)
    else:
        d_cart = {'order': [str(i) for i in range(1, 6)], 'cost': ''}
        data.update(d_cart)                # setting quantity for FIVE chosen items
        response_post_cost = requests.post(URL + '/groups', cookies=cookies, data=data)
        html_doc = response_post_cost.text
        soup_post_cost = BeautifulSoup(html_doc, "html.parser")

        # [['13791', 'ЕР 16104/2В', None, '9045.06', None, 'DELETE']]
        l_selected_cost = [[ii.string for ii in i.find_all('td')][:4] for i in soup_post_cost.find('tbody').find_all('tr')]

        # quantity for the list of ORDERS
        l_quantity = []

        for i in soup_post_cost.find('tbody').find_all('tr'):
            for ii in i.find_all('td'):
                for iii in ii.find_all('input'):
                    l_quantity.append(iii['value'])

        sum_count = round(sum([(float(a[3])*int(b)) for a, b in zip(l_selected_cost, l_quantity)]), 2)
        cost_from_web = soup_post_cost.find_all('h5')[0].text.split()[1]
        assert sum_count == float(cost_from_web)
