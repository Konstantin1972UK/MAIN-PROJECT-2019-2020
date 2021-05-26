import requests
import pytest
from bs4 import BeautifulSoup

@pytest.fixture(name='get_groups')
def get_groups_page(url):
    URL = url
    response_get = requests.get(URL + '/groups')                            # get '/groups' without cookies
    cookies = response_get.cookies
    response_get_cookies = requests.get(URL + '/groups', cookies=cookies)   # get  '/groups' with cookies
    return cookies, response_get, response_get_cookies

@pytest.mark.smoke(reason="get '/groups' without cookies")
def test_get_groups_page(get_groups):                           # get '/groups' without cookies
    cookies, response_get, response_get_cookies = get_groups
    assert response_get.status_code == 200

@pytest.mark.smoke(reason="get '/groups' with cookies")
def test_get_groups_page_cookies(get_groups):                    # get '/groups' with cookies
    cookies, response_get, response_get_cookies = get_groups
    assert response_get_cookies.status_code == 200

@pytest.mark.smoke(reason="get '/groups'. only ONE cookies is set")
def test_get_groups_page_cookies_quantity(get_groups):           # get '/groups'. only ONE cookies is set
    cookies, response_get, response_get_cookies = get_groups
    assert len(cookies) == 1  # only ONE cookies is set

@pytest.mark.smoke(reason="get '/groups'. name 'conn_1'  cookie")
def test_get_groups_page_cookies_name(get_groups):                # get '/groups'. name 'conn_1'  cookie
    cookies, response_get, response_get_cookies = get_groups
    assert cookies.get_dict().get('conn_1', None) != None

@pytest.mark.smoke(reason="get '/groups'. 'checkbox' DEFAULT")
def test_get_groups_page_checkbox_default(get_groups):            #'checkbox' DEFAULT ['ЕР', 'МКН', 'МКС', 'Code', 'Group', 'Name', 'Ostatok','PriceEleton']
    cookies, response_get, response_get_cookies = get_groups
    l_checkbox_defaul_groups = ['ЕР', 'МКН', 'МКС']
    l_checkbox_defaul_columns = ['Code', 'Name', 'Ostatok', 'PriceEleton']
    l_checkbox_default = l_checkbox_defaul_groups + l_checkbox_defaul_columns
    html_doc = response_get.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    l_checkbox = [i['value'] for i in soup.find_all('input') if i.get('checked', None) != None]
    assert l_checkbox == l_checkbox_default

@pytest.mark.smoke(reason="get '/groups'. 'columns' DEFAULT")
def test_get_groups_page_columns_default(get_groups):            #'columns' ['Code', 'Name', 'Ostatok', 'PriceEleton', None]
    cookies, response_get, response_get_cookies = get_groups
    html_doc = response_get.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    columns_default = ['Code', 'Name', 'Ostatok', 'PriceEleton', None]
    columns = [i.string for i in soup.find('thead').find_all('th')]
    assert columns == columns_default

@pytest.mark.smoke(reason="get '/groups'. Items display in TABLE")
def test_get_groups_page_items_default(get_groups):             #'columns' ['Code', 'Name', 'Ostatok', 'PriceEleton', None]
    cookies, response_get, response_get_cookies = get_groups
    html_doc = response_get.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = [[ii.string for ii in i.find_all('td')] for i in soup.find('tbody').find_all('tr')]
    # ['7817', 'МКН 1263М IP31', '20', '3950.1', None, None, None, None, None, 'cart']
    name = [i[1] for i in table]
    set_name = set([i.split()[0] for i in name])  # {'МКС', 'ЕР', 'МКН'}
    l_checkbox_defaul_groups = ['ЕР', 'МКН', 'МКС']
    assert sorted(set_name) == sorted(l_checkbox_defaul_groups)

@pytest.mark.smoke(reason="post 'empty' '/groups' without cookies")
def test_post_groups_page(url)            :                         #post 'empty' '/groups' without cookies
    URL = url
    response_post_empty = requests.post(URL + '/groups')
    assert response_post_empty.status_code == 200

@pytest.mark.smoke(reason="post 'empty' '/groups' with cookies")
def test_post_groups_page_cookies(url, get_groups):                  #post 'empty' '/groups' with cookies
    URL = url
    cookies, response_get, response_get_cookies = get_groups
    response_post_empty_cookies = requests.post(URL + '/groups')
    assert response_post_empty_cookies.status_code == 200

@pytest.mark.smoke(reason="post checkbox variants with cookies")
def test_post_groups_page_checkbox_variant(url, get_groups):         #post checkbox variants with cookies
    URL = url
    cookies, response_get, response_get_cookies = get_groups
    l_product = ['Дин', 'ЕР', 'Козырёк', 'Кронштейны', 'Лицевые', 'МКН', 'МКС', 'Монтажные', 'Пластины', 'Профиль',\
                 'Прочее', 'СМ', 'Скоба', 'Стойка', 'Стойки', 'Усилитель', 'Устройства', 'Цоколя', 'Экраны', 'Ячейки']
    l_param = ['Code', 'Group', 'Name', 'Ostatok', 'PriceEleton', 'PriceP', 'PriceP1', 'PriceP2', 'PriceP3']

    data_prod = []
    for prod in l_product:  # ['Дин', 'ЕР', 'Козырёк', 'Кронштейны', 'Лицевые', 'МКН', 'МКС', 'Монтажные', 'Пластины', 'Профиль', 'Прочее', 'СМ', 'Скоба', 'Стойка', 'Стойки', 'Усилитель', 'Устройства', 'Цоколя', 'Экраны', 'Ячейки']
        data_prod.append(prod)
        data_col = []
        for col in l_param:  # ['Code', 'Group', 'Name', 'Ostatok', 'PriceEleton', 'PriceP', 'PriceP1', 'PriceP2', 'PriceP3']
            data_col.append(col)
            data_post = (data_prod + data_col)
            data = {'groups': [i for i in data_post]}
            # ['Дин', 'Code', 'Group']
            # ['Дин', 'Code', 'Group', 'Name']
            # ['Дин', 'Code', 'Group', 'Name', 'Ostatok']
            # ['Дин', 'Code', 'Group', 'Name', 'Ostatok', 'PriceEleton']
            # ['Дин', 'Code', 'Group', 'Name', 'Ostatok', 'PriceEleton', 'PriceP']
            # ['Дин', 'Code', 'Group', 'Name', 'Ostatok', 'PriceEleton', 'PriceP', 'PriceP1']
            # ['Дин', 'Code', 'Group', 'Name', 'Ostatok', 'PriceEleton', 'PriceP', 'PriceP1', 'PriceP2']
            # ['Дин', 'Code', 'Group', 'Name', 'Ostatok', 'PriceEleton', 'PriceP', 'PriceP1', 'PriceP2', 'PriceP3']
            response_post_cookies = requests.post(URL + '/groups', cookies=cookies, data=data)
            html_doc = response_post_cookies.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            l_checkbox_var = [i['value'] for i in soup.find_all('input') if i.get('checked', None) != None]
            # content chekboxes
            assert sorted(l_checkbox_var) == sorted(data_post)  # Content 'checkbox'
            # content 'columns'
            columns_var = [i.string for i in soup.find('thead').find_all('th') if i.string]
            assert sorted(data_col) == sorted(columns_var)
            # # Chosen items displays in TABLE
            table = [[ii.string for ii in i.find_all('td')] for i in soup.find('tbody').find_all('tr')]
            # ['7817', 'МКН', 'МКН 1263М IP31', '20', '3950.1', None, None, None, None, None, 'cart']
            if 'Group' in data_col:
                name = [i[1] for i in table]                # 'Group'
                set_name_var = set([i.split()[0] for i in name])
                assert sorted(set_name_var) == sorted(data_prod)  # Chosen items displays in TABLE  'Group'
