import pytest
import sqlite3

l_columns_full = ['Code', 'Group', 'Name', 'Ostatok', 'PriceEleton', 'PriceP', 'PriceP1', 'PriceP2', 'PriceP3']
set_radiobuttons_group = ['МКН', 'МКС', 'ЕР']
set_radiobuttons_columns = ['Code', 'Name', 'Ostatok', 'PriceEleton']
set_radiobuttons = set_radiobuttons_group + set_radiobuttons_columns

conn = sqlite3.connect("base_factory.db")
cursor = conn.cursor()
data = cursor.execute("SELECT * FROM prices ORDER BY name ASC")
data = data.fetchall()
conn.close()

identity_table = []
item_new_quantity = []

data_input = [[l_columns_full[:i], data] for i in range(1, 1+len(l_columns_full))]

@pytest.mark.smoke(reason="creating columns for table")
@pytest.mark.parametrize('creating_columns', data_input)
def test_f_creating_columns(creating_columns, app):
    set_radiobuttons, data =  creating_columns
    res = app.f_creating_columns(set_radiobuttons, data)
    assert bool(res) == 1  # result exists

    l_columns, data_for_row, data_for_row_order = res
    l_radiobuttons = [i for i in set_radiobuttons if i in l_columns_full]
    assert l_columns == l_radiobuttons


