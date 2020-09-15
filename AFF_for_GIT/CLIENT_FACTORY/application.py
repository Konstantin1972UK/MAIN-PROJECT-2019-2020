from flask import Flask, render_template, redirect, request, send_file, flash, make_response, jsonify
from flask_mail import Mail, Message

import sqlite3
from datetime import datetime, timedelta
from ftplib import FTP_TLS
import pandas as pd
import helpic_client_factory as helpic   # for special data
import re
import xlwt                                   #for *.xls
import os.path
from threading import Thread

# for creating EMPTY TABLE 'connection'
# conn = sqlite3.connect("info_connection.db")
# c = conn.cursor()
# c.execute("CREATE TABLE connection (\
#                        code INTEGER PRIMARY KEY NOT NULL,\
#                        conn_ VARCHAR(30) NOT NULL,\
#                        date_time VARCHAR(20) NOT NULL,\
#                        remoute_addr VARCHAR(20) NOT NULL,\
#                        remoute_port VARCHAR(5) NOT NULL,\
#                        action VARCHAR(20) NOT NULL)")

# https://medium.com/nuances-of-programming/%D0%BE%D0%B2%D0%BB%D0%B0%D0%B4%D0%B5%D0%B9-python-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%B2%D0%B0%D1%8F-%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-%D1%87%D0%B0%D1%81%D1%82%D1%8C-4-60e016f18422

# heroku create YourName

# requirements.txt   pip gunicorn / pip list /          pip list > requirements.txt
                                                         # pip freeze

# Procfile           web: gunicorn mainscript:app
# runtime.txt        python-3.7.1

#         !!!!!!     app.debug =     !!!!!!

# !!!!  pip install  gunicorn #for NEW !!!!

#!!!  Убедитесь, что находитесь в той же директории, !!!!!!!!!  где лежит ваш файл Python !!!!!!!!!!!

#Убедитесь, что находитесь в той же директории, !!!!!!!!!  где лежит ваш файл Python !!!!!!!!!!!
#Убедитесь, что вы залогинены в heroku                    // heroku login
#Вызовите свое приложение                                 // heroku git:remote --app YourName
#Инициализируйте git, чтобы загрузить все файлы           // git init
#Добавьте все файлы (это точка в конце, что означает все) // git add .
#Теперь, зафиксируйте все добавленные файлы на сервер     // git commit -m    / example - "First upload"
#Запушьте все в master branch                             // git push heroku master

# git config core.autocrlf true  ???

# error: RPC failed; curl 56 OpenSSL SSL_read: Connection was reset, errno 10054
# It might be because of the large size of repository and default buffer size of git
# so by doing above(on git bash), git buffer size will get increase.
# git config http.postBuffer 524288000


app = Flask(__name__)
# app.debug = True
# statistic_flag = False                # for writing statistic to 'info_connection.db'
statistic_flag   = True                 # for writing statistic to 'info_connection.db'
connection_flag  = False                # connection to DATABASE   'info_connection.db'
app.secret_key = helpic.key if helpic.key else 'key'


l_columns_full = ['Code', 'Group', 'Name', 'Ostatok', 'PriceEleton', 'PriceP', 'PriceP1', 'PriceP2', 'PriceP3']

# for SMPT-Server
app.config['MAIL_SERVER']     = helpic.mail_server
app.config['MAIL_PORT']       = helpic.mail_port
app.config['MAIL_USERNAME']   = helpic.mail_username
app.config['MAIL_PASSWORD']   = helpic.mail_password
app.config['MAIL_USE_TLS']    = False
app.config['MAIL_USE_SSL']    = True

mail = Mail(app)

# connection to FTP-Server
def f_connection_ftp_server(place, login, password):
    print('Connection to FTP-Server')
    try:
        ftps = FTP_TLS(place, login, password)
        print("Connection is OK")
    except Exception as e:
        print(e)
        print('Can not connect to FTP-Server')
        return None  # for prevent doing next code
    return ftps

# updating 'base_factory.db' from FTP-Server
def f_get_db():
    # connection to FTP-Server
    ftps = f_connection_ftp_server(helpic.place_ftp, helpic.user_ftp, helpic.password_ftp)

    try:
        ftps.cwd(helpic.directory_ftp)

    except Exception as e:
        print("Can not find directory '{}' at FTP-Server".format(helpic.directory_ftp))
        return None           # for preventing doing next code

    try:
        file_name = 'base_factory.db'
        with open(file_name, 'wb') as f:
            ftps.retrbinary('RETR ' + file_name, f.write)     # rewriting 'base_factory.db'

    except Exception as e:
        print("Can not find 'base_factory.db' in directory '{}' at FTP-Server".format(helpic.directory_ftp))
        return None           # for preventing doing next code

    ftps.quit()
    print('Information in your base WAS UPDATED')

    # time last connection to FTP-Server
    # 'hours=3' - difference time between heroku-server and Ukraine
    time_ftp_check = (datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect("base_factory.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO prices_info VALUES(?,?)", (2, time_ftp_check))
        conn.commit()
    except sqlite3.IntegrityError as err:
        print("\033[031mSomething WRONG with 'prices_info' in 'base_factory.db'\n", err)
    finally:
        conn.close()

    return 0

# time last connection to FTP-Server
def f_get_time_ftp_check():
    conn = sqlite3.connect("base_factory.db")
    cursor = conn.cursor()
    time_ftp_check = cursor.execute("SELECT info FROM prices_info WHERE code=2")
    time_ftp_check = time_ftp_check.fetchone()
    conn.close()
    return time_ftp_check[0]

# loading data from 'base_factory.db'
def f_load_db():

    conn = sqlite3.connect("base_factory.db")
    cursor = conn.cursor()

    data = cursor.execute("SELECT * FROM prices ORDER BY name ASC")
    data = data.fetchall()

    base_update =cursor.execute("SELECT info FROM prices_info WHERE code=1")
    base_update = base_update.fetchall()

    conn.close()
    # getting actual time of updating 'base_factory.db'
    base_update = base_update[0][0]

    # elements for radiobuttons
    l_columns_start = ['Code', 'Name', 'Ostatok', 'PriceEleton']         # for first filling index.html
    set_radiobuttons_full = sorted(set([i[1].split()[0] for i in data]))
    set_radiobuttons = [i for i in set_radiobuttons_full] + l_columns_start

    return data, base_update, set_radiobuttons, set_radiobuttons_full

# creating columns for table
def f_creating_columns(set_radiobuttons, data, identity_table=None, item_new_quantity=[]):
    global l_columns_full

    # data_order
    if identity_table == None:
        data_order = []
    else:
        data_order = f_get_data_order(identity_table)          # data_order

        if not item_new_quantity:
            item_new_quantity = [i[-1] for i in data_order]
        else:
            item_new_quantity = item_new_quantity if len(item_new_quantity) == len(data_order) else item_new_quantity + ['1'] * (len(data_order) - len(item_new_quantity))
        # data_order = [(8624, 'Дин рейка', 'Др2-54 Д.Дин-рейка.', 33, 41.34, 34.26, 34.26, 35.1, 0, 1),
        for num, i in enumerate(data_order):
            new_quantity = int(item_new_quantity[num])
            tmp = i[:-1] + ((new_quantity,))
            data_order[num] = tmp

            conn = sqlite3.connect('orders.db')
            cur = conn.cursor()
            quary = "UPDATE {table} SET order_item={new_quantity} WHERE code_item={code_item}"
            # print(quary)
            cur.execute(quary.format(table=identity_table, new_quantity=new_quantity, code_item=i[0]))
            conn.commit()
            conn.close()


    # creating columns = CHECK flags
    # l_columns_full = ['Code', 'Group', 'Name', 'Ostatok', 'PriceEleton', 'PriceP', 'PriceP1', 'PriceP2', 'PriceP3']
    data_for_row       = []
    for i in data:
        tmp_data = []
        for num, columns in enumerate(l_columns_full):
            if columns in set_radiobuttons:
                tmp_data.append(i[num])
        data_for_row.append(tmp_data)

    data_for_row_order = []

    for num_, i in enumerate(data_order):
        tmp_data_order = []
        for num, columns in enumerate(l_columns_full):
            if columns in set_radiobuttons:
                tmp_data_order.append(i[num])
        tmp_data_order.append(i[-1])           # new_quantity
        data_for_row_order.append(tmp_data_order)

    l_columns = [i for i in l_columns_full if i in set_radiobuttons]

    return l_columns, data_for_row, data_for_row_order

#info_connection.db
def f_connection_info(res, action):
    global connection_flag
    print("start f_connection_info(res, action) connection_flag = ", connection_flag)
    # for info_connection.db
    # 'hours=3' - difference time between heroku-server and Ukraine
    date_time = (datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S:%f')  # 2020-07-06 17:17:02:399211
    # date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')  # 2020-07-06 17:17:02:399211 # For LOCAL TESTING ONLY

    # date_time = date_time[:-7]        ????????????????

    remoute_addr = request.environ['REMOTE_ADDR']
    print('remoute_addr = ', remoute_addr)
    remoute_port = int(request.environ['REMOTE_PORT'])

    ftps = f_connection_ftp_server(helpic.place_ftp, helpic.user_ftp, helpic.password_ftp)
    print(1)
    # contoll existing directory 'helpic.directory_ftp'
    try:
        ftps.cwd(helpic.directory_ftp)
    except Exception as e:
        print("Can not find directory '{}' at FTP-Server".format(helpic.directory_ftp), e)
        return res             # for preventing doing next code
    print(2)
    # contoll existing  'info_connection.db' in directory 'helpic.directory_ftp'
    file_name = 'info_connection.db'

    if file_name not in ftps.nlst():           #  ['info_connection.db', '.', '..', 'base_factory.db']
        print("\033[31mCan not find 'info_connection.db' in directory '{}' at FTP-Server\033[0m".format(helpic.directory_ftp))
        return res   # for preventing doing next code
    print(3)
    try:
        # 1. Copy 'info_connection.db' from FTP-Server to HEROKU
        with open(file_name, 'wb') as f:

            ftps.retrbinary('RETR ' + file_name, f.write)  # rewriting 'info_connection.db'
        # 2. Add to 'info_connection.db' new information
        # info_connection.db/connection # code-int, conn_-varchar(30), date_time-varchar(20), remoute_addr-varchar(20), remoute_port-varchar(5), action-varchar(20)

        # controll SIZE  'info_connection.db'

        file_size = os.path.getsize(file_name)
        print('file_size = ', file_size)
        if file_size < 1000:
            print("It seems that 'info_connection.db' very small")
            return res

        conn = sqlite3.connect(file_name)
        cursor = conn.cursor()

        # controll existing table 'connection' in "info_connection.db"
        result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = result.fetchall()   # getting tables in "info_connection.db"
        print(5)
        if not any([i[0] == "connection" for i in tables]):
            conn.close()                                      # close connection before RETURN
            os.remove(file_name)  # deleting EMPY 'info_connection.db' (without table)
            print("\033[31mCan not find table 'connection' in 'info_connection.db'\033[0m")
            return res                                        # for preventing doing next code
        conn.close()
        # identificator = 20200812181316817485
        identificator = request.cookies.get('conn_')
        print(6)
        if not identificator:
            conn_ = re.sub('[ :-]', '', date_time)
            res.set_cookie('conn_', conn_, max_age=60 * 60 * 24 * 365)
            identificator = conn_
            print('identificator = ', identificator)
            action = 'New GUEST-{}'.format(action)
            print("NEW GUEST 'You are WELCOME.................'")

        conn = sqlite3.connect(file_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO connection VALUES(?, ?, ?, ?, ?, ?)",
                               (None, identificator, date_time, remoute_addr, remoute_port, action))
        conn.commit()
        conn.close()
        print(7, 'action = ', action )
         # 3. Copy 'info_connection.db' from HEROKU to FTP-Server

        if os.path.exists(file_name):
            ftps.storbinary('STOR ' + file_name, open('info_connection.db', '+rb'))  # загрузка файла НА FTP-Server
            print("Information in 'info_connection.db' at FTP-Server WAS UPDATED")
            connection_flag = True
            print("7 end OK f_connection_info(res, action) connection_flag = ", connection_flag)
            return res      # All is OK
        #for ALL SITUATIONS
        connection_flag = True
        print("end OK f_connection_info(res, action) connection_flag = ", connection_flag)
        return res  # All is OK

    except Exception as e:
        print("\033[31mSomething WRONG with connection to DATABASE'\033[0m")
        ftps.quit()
        print("end NOT OK f_connection_info(res, action) connection_flag = ", connection_flag)
        return res                                      # for preventing doing next code

#rewriting 'info_connection.db' on HEROKU
def f_getting_info_connection():
    global connection_flag
    # connection to FTP-Server
    ftps = f_connection_ftp_server(helpic.place_ftp, helpic.user_ftp, helpic.password_ftp)
    try:
        ftps.cwd(helpic.directory_ftp)
    except Exception as e:
        ftps.quit()
        print(e)
        print("Can not find directory '{}' at FTP-Server".format(helpic.directory_ftp))
        return None  # for preventing doing next code
    try:
        file_name = 'info_connection.db'
        # 1. Copy 'info_connection.db' from FTP-Server to HEROKU
        with open(file_name, 'wb') as f:
            ftps.retrbinary('RETR ' + file_name, f.write)  # rewriting 'info_connection.db'

    except Exception as e:
        ftps.quit()
        connection_flag = False
        print(e)
        print("Can not find 'base_factory.db' in directory '{}' at FTP-Server".format(helpic.directory_ftp))
        return None  # for preventing doing next code

    ftps.quit()
    connection_flag = True
    print('f_getting_info_connection() = ', 'file_name = ', os.path.getsize(file_name))
    print("Information in 'info_connection.db' WAS UPDATED from FTP-Server")
    return 1

# data_order
def f_get_data_order(identity_table):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    quary = "SELECT * FROM {table}"
    data_order = [i[1:] for i in cur.execute(quary.format(table=identity_table))]  # code INTEGER PRIMARY KEY AUTOINCREMENT
    conn.close()
    return  data_order

# keyhole
@app.route('/keyhole')
def keyhole():
    global connection_flag

    connection_flag = False   # before checking "f_getting_info_connection()"

    clue = request.args.get(helpic.statistic)

    if not f_getting_info_connection():            #rewriting 'info_connection.db' on HEROKU
        return jsonify("Something has happend WRONG")

    if not connection_flag:                        # get from    f_getting_info_connection()
        return "<p>Something WRONG 'with info_connection.db'</p>\
                <p>if not connection_flag = {} </p>".format(connection_flag)

    # because of "app[web.1]: sqlite3.OperationalError: no such table: connection"
    try:
        conn = sqlite3.connect("info_connection.db")
        cursor = conn.cursor()
        data = cursor.execute("SELECT * FROM connection")
        data = data.fetchall()
        columns = [desc[0] for desc in cursor.description]  # for Excell-file
        conn.close()
    except sqlite3.OperationalError as e:
        conn.close()
        os.remove("info_connection.db")
        connection_flag = False
        print("Exception during opening DB 'info_connection.db'", e, sep='\n')
        return jsonify("Exception during opening DB 'info_connection.db'")

    if clue == helpic.clue_1:
        # sql-data to Excell
        writer = pd.ExcelWriter('statistic.xls')
        df = pd.DataFrame(data, columns=columns)
        df.to_excel(writer, sheet_name='statistic')
        writer.save()
        return send_file('statistic.xls', as_attachment=True)

    elif clue == helpic.clue_2:
        # data = (118, '20200706174754855616', '2020-07-07 13:39:47', '127.0.0.1', '57356', 'index_page')
        l = sorted(set([(i[2][:10], i[1]) for i in data]), key=lambda x: x[0])
        return ''.join(['<p>' + '------'.join(i) + '</p>' for i in l])

    elif clue == helpic.clue_3:
        # data = (118, '20200706174754855616', '2020-07-07 13:39:47', '127.0.0.1', '57356', 'index_page')
        l = sorted(data, key=lambda x: x[2])
        return ''.join( ['<p>' + ' --- '.join(i[1:]) + '</p>' for i in l] )

    else:
        return jsonify(False)


@app.route('/')
def index():
    """ Show ostatky sklad MK"""
    f_get_db()                                                               # updating 'base_factory.db' from FTP-Server
    time_ftp_check = f_get_time_ftp_check()                                  # time last connection to FTP-Server
    data, base_update, set_radiobuttons, set_radiobuttons_full = f_load_db() # loading data from 'base_factory.db'
    l_columns, data_for_row, data_for_row_order = f_creating_columns(set_radiobuttons, data)     # creating data with filtered columns
    # flash-messege about 'base_update'
    messege_ost     = 'Ostatky was successfully updated on {}.'.format(base_update)
    flash('{} We have used cookies for your identification.'.format(messege_ost))


    action = 'index_page'
    res = make_response(render_template('index.html', items=data_for_row, base_update=base_update, time_ftp_check=time_ftp_check, \
                        set_radiobuttons=set_radiobuttons, set_radiobuttons_full=set_radiobuttons_full, \
                        l_columns_full=l_columns_full, l_columns=l_columns, l_order=data_for_row_order))

    return f_connection_info(res, action) if statistic_flag else res

@app.route('/map')
def map():
    action = 'map_page'
    res = make_response(render_template('map.html'))
    return f_connection_info(res, action) if statistic_flag else res

@app.route('/partners')
def partner():
    action = 'partners_page'
    res = make_response(render_template('partners.html'))
    return f_connection_info(res, action) if statistic_flag else res

@app.route('/partner_info')
def partner_info():
    action = 'partner_info'
    res = send_file('partner_info.docx', as_attachment=True)
    return f_connection_info(res, action) if statistic_flag else res

@app.route('/partner_info_eliton')
def partner_info_eliton():
    action = 'partner_info_eliton'
    res = redirect('http://eliton.com.ua/')
    return f_connection_info(res, action) if statistic_flag else res

@app.route('/partner_info_lina')
def partner_info_lina():
    action = 'partner_info_lina'
    res = redirect('http://www.lina.com.ua/')
    return f_connection_info(res, action) if statistic_flag else res

@app.route('/partner_info_pa')
def partner_info_pa():
    action = 'partner_info_pa'
    res = redirect('https://www.pa.ua/')
    return f_connection_info(res, action) if statistic_flag else res

@app.route('/send', methods=["GET", "POST"])
def send():
    adress_to = request.form.getlist('adress_to')
    identity = request.cookies.get('conn_')       # current user
    identity_table = 'order_' + identity

    if request.method == "POST" and adress_to:
        castomer = request.form.getlist('castomer')
        comment  = request.form.getlist('comment')
        action = 'send_order'
        greeting = 'Hello FRIEND! I am HEROKU and I have found an ORDER!'

        l_text_order = []
        data_order = f_get_data_order(identity_table)

        counter = 1
        for i in data_order:
            quantity  = str(i[-1])
            item      = i[2]
            l_text_order.append('{: <2d} {:<30} {:<5}'.format(counter, item, quantity))
            counter += 1

        text_warning = 'DO NOT REPLY to this address. I am a BOT.'  + '\n'
        text_order    = '- ' * 10 + 'ORDER'     + '- ' * 10 + '\n' + '\n'.join(l_text_order) + '\n'
        text_castomer = '- ' * 9  + 'CASTOMER ' + '- ' * 9 +  '\n' + castomer[0] + '\n'
        text_email    = '- ' * 10 + 'E-MAIL '   + '- ' * 9 +  '\n' + adress_to[0] + '\n'
        text_comment  = '- ' * 10 + 'COMMENT'   + '- ' * 9 +  '\n' + comment[0]

        msg = Message(greeting, sender=helpic.mail_username)
        msg.recipients = [helpic.mail_my_personal, helpic.mail_alexandr]         # for PRODUCTION
        # msg.recipients = [helpic.mail_my_personal]                             # for TESTING ONLY

        # # copy for CASTOMER
        if adress_to:                     # preventing from sending without e-mail
            msg.add_recipient(adress_to[0])

        msg.body =  text_warning + text_order + text_castomer + text_email + text_comment

        # OLD VARIANT
        # res = mail.send(msg)
        # res = f_connection_info(res, action) if statistic_flag else res

        #NEW VARIANT
        # thr = Thread(target=f_send, args=((mail, msg, action,)))
        # thr.start()

        #THIRD VARIANT
        print("Sending 111..............")
        with app.app_context():
            print("Sending contest.............")
            res = mail.send(msg)
            f_connection_info(res, action)
            print("was sent 1111................")


        flash('!!!  Your ORDER was SENT  !!!')
        # deleting info in TABLE after sending
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        quary = "DELETE FROM {table}"
        cur.execute(quary.format(table=identity_table))
        conn.commit()
        conn.close()
        return index()

# SENDING by THREAD
def f_send(mail, msg, action):
    print("Sending..............")
    # STATISTIC creates ERROR. SEE LATER
    # if statistic_flag:
    #     f_connection_info(1, action)
    with app.app_context():
        mail.send(msg)

    print("was sent................")



@app.route('/groups', methods=["GET", "POST"])
def groups():
    global l_columns_full
    time_ftp_check = f_get_time_ftp_check()   # time last connection to FTP-Server

    # Database 'orders.db' creating TABLES
    identity = request.cookies.get('conn_')  # current user

    if identity:
        # creating "orders.db" if it does not exist
        conn = sqlite3.connect('orders.db')
        cur = conn.cursor()
        quary = "CREATE TABLE  IF NOT EXISTS {table}  (code INTEGER PRIMARY KEY AUTOINCREMENT, \
                          code_item INTEGER NOT NULL,\
                          group_item VARCHAR(50) NOT NULL,\
                          name VARCHAR(50) NOT NULL,\
                          ostatok_mk INTEGER NOT NULL,\
                          price NUMERIC(2) NOT NULL,\
                          priceP NUMERIC(2) NOT NULL,\
                          priceP1 NUMERIC(2) NOT NULL,\
                          priceP2 NUMERIC(2) NOT NULL,\
                          priceP3 NUMERIC(2) NOT NULL,\
                          order_item INTEGER NOT NULL)"
        identity_table = 'order_' + identity
        cur.execute(quary.format(table=identity_table))
        conn.commit()
        conn.close()

    # data_order = [(227, 'МКН ', 'МКН 432М IP31', 72, 607.86, 461.94, 474.12, 486.24, 1), (499, 'МКН ', 'МКН 55.25М IP31', 29, 1150.02, 874.02, 897, 919.98, 1)]
    # data_order 'type' = 'tuple'
    data_order = f_get_data_order(identity_table)


    """ Show ostatky sklad MK using selected radiobuttons"""
    if request.method == "GET":
        data, base_update, set_radiobuttons, set_radiobuttons_full = f_load_db()  # loading data from 'base_factory.db'
        l_columns, data_for_row, data_for_row_order = f_creating_columns(set_radiobuttons, data)
        return render_template('index.html', items=data_for_row, base_update=base_update, time_ftp_check=time_ftp_check, \
                               set_radiobuttons=set_radiobuttons, set_radiobuttons_full=set_radiobuttons_full,\
                               l_columns_full=l_columns_full, l_columns=l_columns)

    else:
        data, base_update, set_radiobuttons, set_radiobuttons_full = f_load_db()  # loading data from 'base_factory.db'
        set_radiobuttons  = request.form.getlist('groups')
        item_code         = request.form.getlist('cart')       # adding to 'l_orders'
        item_delete       = request.form.getlist('delete')     # deleting from 'l_orders'
        item_new_quantity = request.form.getlist('order')      # getting 'new_quantity'item for changing the quantity of orders in 'data_order'
        confirmation      = request.form.getlist('confirm')    # getting 'confirm'

        # print('item_new_quantity _up = ', item_new_quantity)
        # print('data_order = ', data_order)


        #  column 'Code' must be oh the screen
        set_radiobuttons = set_radiobuttons if 'Code' in set_radiobuttons else ['Code'] + set_radiobuttons

        # data = [('00000013791', 'ЕР ', 'ЕР 16104/2В', '', 5892.96, 4773.3, 4891.14, 5008.98, 0), , ]
        # creating row = CHECK flags
        data = [i for i in data if i[1].split()[0] in set_radiobuttons]          # creating data with filtered rows

        action = 'check_button'

        if confirmation:
            action = 'confirmation'
            # data_order = [(14776, 'Козырёк водоотливной', 'ВК4.15 Козырёк водоотливной', '', 140.16, 116.28, 116.28, 119.1, 0),
            #  (14993, 'Козырёк водоотливной', 'ВК4.25 Козырёк водоотливной', 6, 218.52, 181.32, 181.32, 185.7, 0)]
            # item_new_quantity = ['12', '13']
            l_columns = ['Item', 'Order']
            # l_order = [('ВК4.25 Козырёк водоотливной', '12'), ('ВК4.15 Козырёк водоотливной', '13'),
            # ('Др2-54 Д.Дин-рейка.', '1'), ('ВК42 Козырёк водоотливной', '2')]
            l_order   = [(a[2], b) for a, b in zip(data_order, item_new_quantity)]
            res = make_response(render_template('confirmation.html', l_columns=l_columns, l_order=l_order))
            return f_connection_info(res, action)

        # removing items to the 'data_order'
        if item_delete:
            action = 'delete'
            item_delete = item_delete[0]                    # item_delete =  ['14776']   get 'item code'  type = <class 'str'>
            # item_new_quantity
            index = 0
            for i in data_order:
                if i[0] == int(item_delete):
                    break
                else:
                    index += 1
            item_new_quantity.pop(index)

            conn = sqlite3.connect('orders.db')
            cur = conn.cursor()
            quary = "DELETE FROM {table} WHERE code_item={item_delete}"
            cur.execute(quary.format(table=identity_table, item_delete=item_delete))
            conn.commit()
            conn.close()

        # adding items to the 'data_order'
        if item_code and (int(item_code[0]) not in [i[0] for i in data_order]):  # preventing adding duplicats to 'data_order'
            action = 'cart'

            item_code = item_code[0]        # get 'item code'
            for i in data:
                # (14776, 'Козырёк водоотливной', 'ВК4.15 Козырёк водоотливной', '', 140.16, 116.28, 116.28, 119.1, 0)
                if item_code == str(i[0]):
                    code_item, group_item, name, ostatok_mk, price, priceP, priceP1, priceP2, priceP3 = i
                    conn = sqlite3.connect('orders.db')
                    cur = conn.cursor()
                    quary = "INSERT INTO {table} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    cur.execute(quary.format(table=identity_table),(code_item, group_item, name, ostatok_mk, price, priceP, priceP1, priceP2, priceP3, 1))
                    conn.commit()
                    conn.close()
                    break

        l_columns, data_for_row, data_for_row_order = f_creating_columns(set_radiobuttons, data, identity_table, item_new_quantity)  # creating data with filtered columns

        res = make_response(render_template('index.html', items=data_for_row, base_update=base_update, time_ftp_check=time_ftp_check, \
                            set_radiobuttons=set_radiobuttons, set_radiobuttons_full=set_radiobuttons_full, \
                            l_columns_full=l_columns_full, l_columns=l_columns, l_order=data_for_row_order))
        return f_connection_info(res, action) if statistic_flag else res

# DOWNLOAD price.zip from SECOND FTP-Server
@app.route('/price')
def price():
    print('downloading price..................')
    ftps = f_connection_ftp_server(helpic.place_ftp, helpic.user_ftp, helpic.password_ftp)
    ftps.cwd(helpic.path_price_ftp)
    file_name = 'price.zip'
    with open(file_name, 'wb') as f:
        ftps.retrbinary('RETR ' + file_name, f.write)  # rewriting 'base_factory.db'

    # return send_file('price.zip', as_attachment=True)
    action = 'download_price'
    res = send_file('price.zip', as_attachment=True)
    print('/price')
    return f_connection_info(res, action) if statistic_flag else res

# DOWNLOAD CatalogEleton from HEROKU
@app.route('/catalog')
def catalog():
    print('downloading CATALOG..................')
    # return send_file('Catalog_Eleton.zip', as_attachment=True)  # catalog ELETON on HEROKU
    # return redirect('https://mega.nz/folder/qxknFQhB#31uULMJB8IP9QZ0cLtIcww')
    action = 'download_catalog'
    res = redirect('https://mega.nz/folder/qxknFQhB#31uULMJB8IP9QZ0cLtIcww')
    return f_connection_info(res, action) if statistic_flag else res

# Update OSTATKY
@app.route('/update')
def update():
    return redirect('/')

# DOWNLOAD 'ostatky.txt' from HEROKU
@app.route('/ostatkyxls')
def ostatkyxlsx():
    conn = sqlite3.connect("base_factory.db")
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM prices")
    data = data.fetchall()
    #cursor.description - list with column's names
    columns = [desc[0] for desc in cursor.description]  # for Excell-file

    base_update = cursor.execute("SELECT info FROM prices_info WHERE code=1")
    base_update = base_update.fetchall()[0][0]
    print('base_update = ', base_update)

    conn.close()

    # sql-data to Excell
    writer = pd.ExcelWriter('ostatky.xls')
    for i in ' -:':
        base_update = base_update.replace(i,'_')
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(writer, sheet_name=base_update)
    writer.save()

    # return send_file('ostatky.xls', as_attachment=True)
    action = 'download_ostatky'
    res = send_file('ostatky.xls', as_attachment=True)
    return f_connection_info(res, action) if statistic_flag else res

if __name__ == '__main__':
     app.run()