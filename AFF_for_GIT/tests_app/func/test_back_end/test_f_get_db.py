import pytest

@pytest.mark.smoke(reason="updating 'base_factory.db' from FTP-Server.Normal.")
def test_f_get_db(app):
    res = app.f_get_db()
    assert res == 0

@pytest.mark.smoke(reason="updating 'base_factory.db' from FTP-Server. Can not find directory at FTP-Server.")
def test_f_get_db_1(helpic, app):
    tru_dir = helpic.directory_ftp
    helpic.directory_ftp = 'Wrong_place'                       # put WRONG dir
    res = app.f_get_db()
    helpic.directory_ftp = tru_dir                             # return RIGHT dir
    assert res == 1

@pytest.mark.smoke(reason="updating 'base_factory.db' from FTP-Server. Can not find 'base_factory.db' in directory")
def test_f_get_db_2(helpic, app):
    tru_file_name = helpic.file_name
    helpic.file_name = 'base_factory_other.db'          # put WRONG file_name
    res = app.f_get_db()
    helpic.file_name = tru_file_name  # return RIGHT file_name
    assert res == 2
