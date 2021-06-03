import unittest
import helpic_factory as helpic
import factory
from tkinter import *
import tkinter.ttk as ttk
import datetime


class TestFunctionConnection(unittest.TestCase):
    def setUp(self):
        self.true_server   = helpic.server
        self.true_database = helpic.database
        self.true_username = helpic.username
        self.true_password = helpic.password
        self.true_driver   = helpic.driver
        self.true_port     = helpic.port

    def test_f_connection_OK(self):
        res = factory.f_connection()
        self.assertEqual(res, 0)                        # connection is OK
        self.assertEqual(factory.flag_base_factory, True)
        for i in [factory.data_naryad, factory.data_vipusk, factory.data_tovari, factory.data_shtribs,\
                  factory.data_zayavka, factory.data_rezerv, factory.data_czeny, factory.data_karta_detaley]:
            self.assertEqual(bool(i), True, "dictionary '{}' is not empty".format(i))

    def test_f_connection_WRONG_server(self):
        helpic.server = 'server'                           #WRONG server
        res = factory.f_connection()
        helpic.server = self.true_server
        self.assertEqual(res, 1, "WRONG 'server' name")    # connection is WRONG
        self.assertEqual(factory.flag_base_factory, False)
        for i in [factory.data_naryad, factory.data_vipusk, factory.data_tovari, factory.data_shtribs,\
                  factory.data_zayavka, factory.data_rezerv]:
            self.assertEqual(bool(i), False, "dictionary '{}' is not empty".format(i))  #creating EMPTY dictionaries

    def test_f_connection_WRONG_database(self):
        helpic.database = 'database'                        #WRONG database
        res = factory.f_connection()
        helpic.database = self.true_database
        self.assertEqual(res, 1, "WRONG 'database' name" )  # connection is WRONG
        self.assertEqual(factory.flag_base_factory, False)
        for i in [factory.data_naryad, factory.data_vipusk, factory.data_tovari, factory.data_shtribs,\
                  factory.data_zayavka, factory.data_rezerv]:
            self.assertEqual(bool(i), False, "dictionary '{}' is not empty".format(i))  #creating EMPTY dictionaries

    def test_f_connection_WRONG_username(self):
        helpic.username = 'username'                        # WRONG username
        res = factory.f_connection()
        helpic.username = self.true_username
        self.assertEqual(res, 1, "WRONG 'username' name")    # connection is WRONG
        self.assertEqual(factory.flag_base_factory, False)
        for i in [factory.data_naryad, factory.data_vipusk, factory.data_tovari, factory.data_shtribs,\
                  factory.data_zayavka, factory.data_rezerv]:
            self.assertEqual(bool(i), False, "dictionary '{}' is not empty".format(i))  #creating EMPTY dictionaries

    def test_f_connection_WRONG_password(self):
        helpic.password = 'password'                         # WRONG password
        res = factory.f_connection()
        helpic.password = self.true_password
        self.assertEqual(res, 1, "WRONG 'password' name")    # connection is WRONG
        self.assertEqual(factory.flag_base_factory, False)
        for i in [factory.data_naryad, factory.data_vipusk, factory.data_tovari, factory.data_shtribs,\
                  factory.data_zayavka, factory.data_rezerv]:
            self.assertEqual(bool(i), False, "dictionary '{}' is not empty".format(i))  #creating EMPTY dictionaries

    def test_f_connection_WRONG_driver(self):
        helpic.driver = 'driver'                             # WRONG password
        res = factory.f_connection()
        helpic.password = self.true_driver
        self.assertEqual(res, 1, "WRONG 'driver' name")      # connection is WRONG
        self.assertEqual(factory.flag_base_factory, False)
        for i in [factory.data_naryad, factory.data_vipusk, factory.data_tovari, factory.data_shtribs,\
                  factory.data_zayavka, factory.data_rezerv]:
            self.assertEqual(bool(i), False, "dictionary '{}' is not empty".format(i))  #creating EMPTY dictionaries

    def test_f_connection_WRONG_port(self):
        helpic.port = 'port'                                 # WRONG port
        res = factory.f_connection()
        helpic.password = self.true_port
        self.assertEqual(res, 1, "WRONG 'port' name")        # connection is WRONG
        self.assertEqual(factory.flag_base_factory, False)
        for i in [factory.data_naryad, factory.data_vipusk, factory.data_tovari, factory.data_shtribs,\
                  factory.data_zayavka, factory.data_rezerv]:
            self.assertEqual(bool(i), False, "dictionary '{}' is not empty".format(i))  #creating EMPTY dictionaries

class TestFunctions(unittest.TestCase):
    def setUp(self):
        factory.root = Tk()
        factory.d_ostatky   = helpic.d_ostatky
        factory.data_tovari = helpic.data_tovari
        factory.d_original  = helpic.d_original
        factory.d_rezerv    = helpic.d_rezerv                #for test_f_add_pr_st_zapusk
        factory.data_naryad = helpic.data_naryad             #for test_f_nezavershonnie_naryadi
        factory.data_vipusk = helpic.data_vipusk             #for test_f_nezavershonnie_naryadi

    def test_f_close(self):
        res = factory.f_close(1)
        self.assertEqual(res, 0, "f_close is OK")

    def test_f_exit(self):
        res = factory.f_exit()
        self.assertEqual(res, 0, "f_exit is OK")

    def test_f_about(self):
        res = hasattr(factory, 'f_about')
        self.assertEqual(res, True, "f_about exists")

    def test_f_oboroty_OK(self):
        factory.label_period_product = Label(factory.root)
        res = factory.f_oboroty()
        self.assertEqual(res, 0, "karta_detaley is OK")

    def test_f_add_pr_st_zapusk(self):
        res = factory.f_add_pr_st_zapusk()
        self.assertEqual(res, 0, "f_add_pr_st_zapusk is OK")

    def test_f_table_tree_inf(self):
        factory.fra_inf = Label(factory.root)
        factory.tree_inf = ttk.Treeview(factory.fra_inf)
        res = factory.f_table_tree_inf()
        self.assertEqual(res, 0, "f_table_tree_inf is OK")

    def test_f_shift_year(self):
        data = datetime.datetime(4021, 4, 21, 9, 8, 44)
        res = factory.f_shift_year(data)                # -2000 from year
        self.assertEqual(res, '2021-04-21 09:08:44', "f_table_tree_inf is OK")

    def test_f_save_store(self):
        res = factory.f_save_store()
        self.assertEqual(res, 0, "f_save_store is OK")

    def test_f_nezavershonnie_naryadi(self):
        res = factory.f_nezavershonnie_naryadi()
        self.assertEqual(res, 0, "f_nezavershonnie_naryadi is OK")

    def test_f_ostatky_ceh_mk(self):
        res = factory.f_ostatky_ceh_mk()
        self.assertEqual(res, 0, "f_ostatky_ceh_mk is OK")

    def test_f_refresh(self):
        factory.btn_refresh = Button()
        factory.label_period_product = Label()

        factory.fra_top = LabelFrame(factory.root)
        factory.tree_inf = ttk.Treeview(factory.fra_top)

        factory.fra_store = LabelFrame(factory.root)
        factory.tree_store = ttk.Treeview(factory.fra_store)

        res = factory.f_refresh()
        self.assertEqual(res, 0, "f_refresh is OK")

    def test_f_load_delta(self):
        res = factory.f_load_delta()
        self.assertEqual(res, 0, "f_load_delta is OK")

    def test_f_previous_zapusk(self):
        factory.fra_store = LabelFrame(factory.root)
        factory.tree_store = ttk.Treeview(factory.fra_store)
        res = factory.previous_zapusk()
        self.assertEqual(res, 0, "previous_zapusk is OK")

    def test_f_ostatky_kharkov(self):
        res = factory.f_ostatky_kharkov()
        self.assertEqual(res, 0, "f_ostatky_kharkov is OK")

    def test_f_shtribs(self):
        factory.data_shtribs = helpic.data_shtribs
        res = factory.f_shtribs()
        self.assertEqual(res, 0, "f_shtribs is OK")

    def test_f_zayavka(self):
        factory.data_zayavka = helpic.data_zayavka
        res = factory.f_zayavka()
        self.assertEqual(res, 0, "f_zayavka is OK")

    def test_f_rezerv(self):
        factory.data_rezerv = helpic.data_rezerv
        res = factory.f_rezerv()
        self.assertEqual(res, 0, "f_rezerv is OK")

    def test_f_report(self):
        res = factory.f_report()
        self.assertEqual(res, 0, "f_report is OK")

    def test_f_create_db(self):
        factory.flag_base_factory = False
        res = factory.f_create_db()
        self.assertEqual(res, None, "f_create_db. flag_base_factory == False  is OK")
        factory.flag_base_factory = True
        factory.data_czeny = helpic.data_czeny
        res = factory.f_create_db()
        self.assertEqual(res, 0, "f_create_db. flag_base_factory == True  is OK")

    def test_f_karta_detaley(self):
        factory.data_karta_detaley = helpic.data_karta_detaley
        res = factory.f_karta_detaley()
        self.assertEqual(res, 0, "f_karta_detaley is OK")

    def test_f_statistica(self):
        res = factory.f_statistica()
        self.assertEqual(res, 0, "f_statistica is OK")

    def test_f_message_check(self):
        factory.text_message = Text(factory.root)
        res = factory.f_message_check()
        self.assertEqual(res, 0, "f_message_check is OK")

    def test_f_message_put(self):
        factory.text_message = Text(factory.root)
        res = factory.f_message_put()
        self.assertEqual(res, 0, "f_message_put is OK")

    def test_f_main(self):
        factory.data_karta_detaley = helpic.data_karta_detaley
        factory.data_zayavka = helpic.data_zayavka
        factory.data_rezerv = helpic.data_rezerv
        factory.flag_base_factory = True
        factory.label_period_product = Label()
        res = factory.f_main()
        self.assertEqual(res, 0, "f_main is OK")

class TestFunctionEntCount(unittest.TestCase):
    def setUp(self):
        factory.root = Tk()
        factory.ent_count = Entry(factory.root)   # for test_f_store_ent
        factory.btn_count = Button(factory.root)  # for test_f_store_ent

    def test_f_store_ent(self):
        res = factory.f_store_ent(1)
        self.assertEqual(res, 0, "f_store_ent is OK")

    def test_f_store_empty(self):
        res = factory.f_store()
        self.assertEqual(res, 0, "f_store with 'empty' input is OK")

    def test_f_store_valid(self):
        factory.ent_count.insert(0, '12')
        res = factory.f_store()
        self.assertEqual(res, 0, "f_store with 'valid' input is OK")

    def test_f_store_invalid(self):
        data = ['10a-', '01', '-12', '1.987', '-.233', 'q', '-0.33', '0.23', '1']
        for i in data:
            factory.ent_count.delete(0, 'end')
            factory.ent_count.insert(0, '{}'.format(i))
            res = factory.f_store()
            self.assertEqual(res, 0, "f_store with 'invalid' inputis OK")

if __name__ == '__main__':
    unittest.main()
