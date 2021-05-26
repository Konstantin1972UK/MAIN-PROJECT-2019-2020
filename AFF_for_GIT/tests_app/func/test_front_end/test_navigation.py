import requests
import pytest


@pytest.mark.smoke(reason="Open the MAIN page '/' ")
def test_open_main_page(url):
    URL = url
    print('url = ', url)
    response_main   = requests.get(URL)
    assert response_main.status_code   == 200

@pytest.mark.smoke(reason="Open the MAIN page '/groups' ")
def test_open_main_page_groups(url):
    URL = url
    response_groups = requests.get(URL + '/groups')
    assert response_groups.status_code == 200

@pytest.mark.smoke(reason="Open the MAP page '/map' ")
def test_open_map_page(url):
    URL = url
    response = requests.get(URL + '/map')
    assert response.status_code == 200

@pytest.mark.smoke(reason="Open the PARTNERS page '/partners' ")
def test_open_partners_page(url):
    URL = url
    response = requests.get(URL + '/partners')
    assert response.status_code == 200

@pytest.mark.smoke(reason="Download 'CATALOG' '/catalog' ")  # checking https://mega.nz/folder/qxknFQhB#31uULMJB8IP9QZ0cLtIcww
def test_download_catalog(url):
    URL = url
    response = requests.get(URL + '/catalog')
    assert response.status_code == 200

@pytest.mark.smoke(reason="Download 'Price' '/price' ")
def test_download_price(url):
    URL = url
    response = requests.get(URL + '/price')
    assert response.status_code == 200

@pytest.mark.smoke(reason="Download  OSTATKY '/ostatkyxls' ")
def test_download_ostatky(url):
    URL = url
    response = requests.get(URL + '/ostatkyxls')
    assert response.status_code == 200

@pytest.mark.smoke(reason="link to 'https://mega.nz/folder/qxknFQhB#31uULMJB8IP9QZ0cLtIcww' ")
def test_download_catalog_link():
    response = requests.get('https://mega.nz/folder/qxknFQhB#31uULMJB8IP9QZ0cLtIcww')
    assert response.status_code == 200

@pytest.mark.smoke(reason="Download  STAISTIC '/keyhole'")
def test_statistic(url, helpic):
    URL = url
    for i in [helpic.clue_1, helpic.clue_2, helpic.clue_3]:
        data = {helpic.statistic: i}
        response = requests.get(URL + '/keyhole', data)
        assert response.status_code == 200