import pytest
import os

@pytest.mark.smoke(reason="NORMAL work")
def test_f_transmissing_info_db_normal(app):
    res = app.f_transmissing_info_db()
    assert res == 0

@pytest.mark.smoke(reason="existng directory 'helpic.directory_ftp")
def test_f_transmissing_info_db_wrong_dir(helpic, app):
    tru_dir = helpic.directory_ftp
    helpic.directory_ftp = 'fail'                   #put in wrong name of the directory
    res = app.f_transmissing_info_db()
    helpic.directory_ftp = tru_dir                   #return old name of the directory
    assert res == 1

@pytest.mark.smoke(reason="existng file 'info_connection_heroku.db' on HEROKU")
def test_f_transmissing_info_db_no_file(app):
    print(os.getcwd())
    os.rename('info_connection_heroku.db', 'test')   #chenging fale name
    res = app.f_transmissing_info_db()
    os.rename('test', 'info_connection_heroku.db')   #return old file name
    assert res == 2







