import pytest

@pytest.mark.smoke(reason="connection to FTP-Server")
def test_connection_ftp_server_normal(helpic, app):
    res = app.f_connection_ftp_server(helpic.place_ftp, helpic.user_ftp, helpic.password_ftp)
    assert 1 == (1 if res else 0)       #return object ftps

@pytest.mark.smoke(reason="getting date.time.now")
def test_f_get_date_time_now(app):
    res = app.f_get_date_time_now()
    assert res != None                  # result exists

@pytest.mark.smoke(reason="time last connection to FTP-Server")
def test_f_get_time_ftp_check(app):
    res = app.f_get_time_ftp_check()
    assert bool(res) == 1                # result exists

@pytest.mark.smoke(reason="loading data from 'base_factory.db'")
def test_f_load_db(app):
    res = app.f_load_db()
    data, base_update, message_update, set_radiobuttons, set_radiobuttons_full = res
    set_radiobuttons_default    = ['МКН', 'МКС', 'ЕР', 'Code', 'Name', 'Ostatok', 'PriceEleton']
    set_radiobuttons_full_sample =  ['Дин', 'ЕР', 'Козырёк', 'Кронштейны', 'Лицевые', 'МКН', 'МКС', 'Монтажные',\
                                    'Пластины', 'Профиль', 'Прочее', 'СМ', 'Скоба', 'Стойка', 'Стойки', 'Усилитель',\
                                    'Устройства', 'Цоколя', 'Экраны', 'Ячейки']
    assert bool(res) == 1                                           # result exists
    assert len(res)  >= 5                                           # all parts of result are present
    assert set_radiobuttons_default     == set_radiobuttons         # set_radiobuttons_default
    assert set_radiobuttons_full_sample == set_radiobuttons_full    # set_radiobuttons_full







