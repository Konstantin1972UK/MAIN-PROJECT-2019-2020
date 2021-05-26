import pytest
import helpic_client_factory as helpic
import application as app
import os

URL = 'http://127.0.0.1:5000/'          #local
# URL = 'http://eleton.herokuapp.com/'    #prod

@pytest.fixture(name='url')
def get_url():
    return URL

@pytest.fixture(name='helpic')
def get_data_helpic_statistic():
    return helpic

@pytest.fixture(name='app')
def get_app():
    return app





