import cryptography.fernet
import mysql.connector
import tkinter as tk
import pyperclip
import webbrowser
import string
import random
import os
from cryptography.fernet import Fernet
from PIL import Image, ImageTk
from win32api import GetSystemMetrics


root = tk.Tk()
w = GetSystemMetrics(0) / 100 * 33
w = str(w).split(".")
w = w[0]
h = GetSystemMetrics(1) / 100 * 94
h = str(h).split(".")
h = h[0]
ofs = GetSystemMetrics(0) / 100 * -0.4
ofs = str(ofs).split(".")
ofs = ofs[0]
geo = str(w) + "x" + str(h) + "+" + ofs + "+0"
root.geometry(geo)

wd = os.path.dirname(os.path.realpath(__file__))
os.chdir(wd)

with open("settings", "r") as get_colors:
    all_colors = get_colors.read()
all_colors = all_colors.split("\n")
prime = all_colors[2]
prime = prime.replace("prime_color=", "")
background = all_colors[3]
background = background.replace("background_color=", "")
secondary = all_colors[4]
secondary = secondary.replace("secondary_color=", "")
secondary_sec = all_colors[5]
secondary_sec = secondary.replace("secondary_color_sec=", "")
third = all_colors[6]
third = third.replace("third_color=", "")
third_sec = all_colors[7]
third_sec = third.replace("third_color=", "")

root.resizable(False, False)
root.configure(bg=background)
root.wm_title("PassOverseer")
root.iconbitmap("design\icon.ico")

help_link = "https://www.youtube.com/watch?v=0wDUNz6ZuWs"


def reset_settings():
    with open("settings", "w", encoding="UTF-8") as settings_c:
        global restore_other_table, pw_gen_len
        settings_c.write("restore_other_table=True #Here you can choose whether the address \"other\" should be restored automatically and you can decide between \"True\"(on) and \"False\"(off)\npw_gen_len=10 #Here you can choose what length your generated passwords should have")
        restore_other_table = "True"
        pw_gen_len = 10
try:
    with open("settings", "r", encoding="UTF-8") as settings_r:
        restore_other_table = settings_r.readline()
        pw_gen_len = settings_r.readline()
except FileNotFoundError:
    reset_settings()

restore_other_table = restore_other_table.replace("restore_other_table=", "")
restore_other_table = restore_other_table.split("#")
restore_other_table = restore_other_table[0]
pw_gen_len = pw_gen_len.replace("pw_gen_len=", "")
pw_gen_len = pw_gen_len.split("#")
try:
    pw_gen_len = int(pw_gen_len[0])
except ValueError:
    reset_settings()



def login():
    global login_frame, host_entry, database_entry, user_entry, passwd_entry, error_label

    def clear_login():
        host_entry.delete(0, "end")
        database_entry.delete(0, "end")
        user_entry.delete(0, "end")
        passwd_entry.delete(0, "end")

    def connect_btn():
        e = "e"
        connect(e)

    def connect(e):
        str(e)
        global host, database, user, password, db, port
        host = host_entry.get()
        port = port_entry.get()
        database = database_entry.get()
        user = user_entry.get()
        password = passwd_entry.get()
        n_fail = False
        port_fail = False
        db_fail = False

        with open("last_login", "w", encoding="UTF-8") as login_data_w:
            to_insert = "host=" + host + "\nport=" + port + "\ndatabase=" + database + "\nuser=" + user
            login_data_w.write(to_insert)


        if database == "":
            db_fail = True
        else:
            try:
                db = mysql.connector.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database
                )
                n_fail is False
                port_fail is False
            except mysql.connector.errors.ProgrammingError:
                n_fail = True
            except mysql.connector.errors.InterfaceError:
                port_fail = True
            except mysql.connector.errors.DatabaseError:
                port_fail = True

        if db_fail is True:
            error_label.config(text="No Database selected!")
        elif n_fail is True:
            error_label.config(text="Something in your Login Data is wrong or the Server is down!")
            passwd_entry.delete(0, "end")
        elif port_fail is True:
            error_label.config(text="Wrong Port!")
        else:
            main()

    def help():
        webbrowser.open(help_link)


    login_frame = tk.Frame(root, height="100", width="1000", bg="#485460")
    header_label = tk.Label(login_frame, text="Login", bg="#485460", fg=prime, font="Ubuntu")
    host_frame = tk.Frame(login_frame, bg=third)
    host_label = tk.Label(host_frame, text="Host: ", bg=third)
    host_entry = tk.Entry(host_frame, width=27, borderwidth="0", bg=third_sec)
    port_frame = tk.Frame(login_frame, bg=secondary)
    port_label = tk.Label(port_frame, text="Port: ", bg=secondary)
    port_entry = tk.Entry(port_frame, width=27, borderwidth="0", bg=secondary_sec)
    database_frame = tk.Frame(login_frame, bg=third)
    database_label = tk.Label(database_frame, text="Database: ", bg=third_sec)
    database_entry = tk.Entry(database_frame, width=27, borderwidth="0", bg="#ffc048")
    user_frame = tk.Frame(login_frame, bg="#0fbcf9")
    user_label = tk.Label(user_frame, text="Username: ", bg="#0fbcf9")
    user_entry = tk.Entry(user_frame, width=27, borderwidth="0", bg="#4bcffa")
    passwd_frame = tk.Frame(login_frame, bg="#ffa801")
    passwd_label = tk.Label(passwd_frame, text="Password: ", bg="#ffa801")
    passwd_entry = tk.Entry(passwd_frame, width=27, borderwidth="0", bg="#ffc048", show="•")
    bottom_bar_login = tk.Frame(login_frame, bg="#05c46b")
    help_frame = tk.Frame(bottom_bar_login)
    help_btn = tk.Button(help_frame, text="Help", width="48", borderwidth="0", bg="#ffd32a", command=help, activebackground="#ffd32a")
    clear_login_btn = tk.Button(bottom_bar_login, text="Clear", width="23", borderwidth="0", bg="#0fbcf9", activebackground="#00d8d6", command=clear_login)
    connect_btn = tk.Button(bottom_bar_login, text="Connect", width="24", borderwidth="0", bg="#05c46b", activebackground="#05c46b", command=connect_btn)
    error_label = tk.Label(login_frame, text="", fg="#ff3f34", bg="#485460")

    login_frame.pack(side="left", anchor="center", padx="140")
    header_label.pack(padx="150", pady="10")
    host_frame.pack(pady="5", padx="5", fill="x")
    host_label.pack(side="left", padx="10", pady="2.5")
    host_entry.pack(side="right", padx="10")
    port_frame.pack(pady="5", padx="5", fill="x")
    port_label.pack(side="left", padx="10", pady="2.5")
    port_entry.pack(side="right", padx="10")
    database_frame.pack(pady="5", padx="5", fill="x")
    database_label.pack(side="left", padx="10", pady="2.5")
    database_entry.pack(side="right", padx="10")
    user_frame.pack(pady="5", padx="5", fill="x")
    user_label.pack(side="left", padx="10", pady="2.5")
    user_entry.pack(side="right", padx="10")
    passwd_frame.pack(pady="5", padx="5", fill="x")
    passwd_label.pack(side="left", padx="10", pady="2.5")
    passwd_entry.pack(side="right", padx="10")
    bottom_bar_login.pack(fill="x", padx="5", pady="10")
    help_frame.pack(fill="x")
    help_btn.pack(side="left")
    clear_login_btn.pack(side="left")
    connect_btn.pack(side="left")
    error_label.pack()

    try:
        with open("last_login", "r", encoding="UTF-8") as login_data_r:
            host_insert = login_data_r.readline()
            host_insert = host_insert.replace("\n", "")
            port_insert = login_data_r.readline()
            port_insert = port_insert.replace("\n", "")
            database_insert = login_data_r.readline()
            database_insert = database_insert.replace("\n", "")
            user_insert = login_data_r.readline()
            user_insert = user_insert.replace("\n", "")
    except FileNotFoundError:
        with open("last_login", "w", encoding="UTF-8") as login_data_c:
            login_data_c.write("host=\nport=\ndatabase=\nuser=")
            host_insert = ""
            port_insert = ""
            database_insert = ""
            user_insert = ""


    host_insert = host_insert.replace("host=", "")
    port_insert = port_insert.replace("port=", "")
    database_insert = database_insert.replace("database=", "")
    user_insert = user_insert.replace("user=", "")
    host_entry.insert("end", host_insert)
    port_entry.insert("end", port_insert)
    database_entry.insert("end", database_insert)
    user_entry.insert("end", user_insert)
    host_entry.bind('<Return>', connect)
    port_entry.bind('<Return>', connect)
    database_entry.bind('<Return>', connect)
    user_entry.bind('<Return>', connect)
    passwd_entry.bind('<Return>', connect)

    if host_entry.get() == "":
        host_entry.focus()
    elif port_entry.get() == "":
        port_entry.focus()
    elif database_entry.get() == "":
        database_entry.focus()
    elif user_entry.get() == "":
        user_entry.focus()
    else:
        passwd_entry.focus()


def main_key(e):
    str(e)
    main()


def main():
    refresh_forget()

    db_cursor = db.cursor()
    db_cursor.execute("SHOW TABLES;")
    global tables, tableD
    tables = db_cursor.fetchall()
    contD = {}
    cont1D = {}
    tableD = {}
    linesD = {}
    copyD = {}

    global top_bar, label1
    top_bar = tk.Frame(bg="#1e272e")
    logo = Image.open("design/Logo.png")
    size = 530, 100
    logo.thumbnail(size, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(logo)
    label1 = tk.Label(top_bar, image=img, bg="#1e272e")
    label1.image = img
    label1.pack()
    top_bar.pack(pady=20)

    with open("key", "rb") as key_file:
        key = key_file.read()

    keystr = str(key)
    keystr = keystr[2:]
    keystr = keystr[:-1]
    if keystr == "":
        key = Fernet.generate_key()
        with open("key", "wb") as keyH:
            keyH.write(key)


    def help():
        webbrowser.open(help_link)

    def open_link(e):
        str(e)
        webbrowser.open("https://www.youtube.com/watch?v=YHtWb64iWvc")

    def change_key_quit_key(e):
        str(e)
        change_key_quit()

    def change_key_quit():
        key_frame.forget()
        info_address.config(text="")

    def change_key_save_key(e):
        str(e)
        change_key_save()

    def change_key_save():
        key_e = key_entry.get()
        if key_e == "":
            info_address.config(text="Key is empty!", fg="#ff3f34")
        else:
            key_frame.forget()

            try:
                with open("key", "r", encoding="UTF-8") as key_Hr:
                    history = key_Hr.read()
                with open("key", "w", encoding="UTF-8") as key_Hw:
                    key_Hw.write(key_e + "\n" + history)

            except FileNotFoundError:
                with open("key", "w", encoding="UTF-8") as key_Create:
                    key_Create.write("")
                with open("key", "r", encoding="UTF-8") as key_Hr:
                    history = key_Hr.read()
                with open("key", "w", encoding="UTF-8") as key_Hw:
                    key_Hw.write(key_e + "\n" + history)

    def change_key():
        global key_frame, key_entry
        key_frame = tk.Frame(root, pady=5, padx=5, bg="#485460")
        key_frame1 = tk.Frame(key_frame, bg="#0fbcf9")
        key_frame1_1 = tk.Frame(key_frame, bg="#0fbcf9")
        key_frame2 = tk.Frame(key_frame)
        key_frame2_1 = tk.Frame(key_frame2)
        key_frame2_2 = tk.Frame(key_frame2)
        key_1 = tk.Label(key_frame1, text="Key: ", width=6, bg="#0fbcf9", anchor="w", justify="left")
        key_entry = tk.Entry(key_frame1, width=33, bg="#4bcffa", borderwidth=0)
        warning = tk.Label(key_frame1_1, text="Before you change the key click me!!!", bg="#ffd32a", fg="black", height=2)
        quit_btn = tk.Button(key_frame2_1, text="Quit", borderwidth=0, bg="#ff3f34", activebackground="#ff3f34", width=19, command=change_key_quit)
        save_btn = tk.Button(key_frame2_2, text="Change", borderwidth=0, bg="#05c46b", activebackground="#05c46b", width=19, command=change_key_save)

        key_frame.pack(pady=40, padx=5, anchor="n")
        key_frame1.pack(fill="x")
        key_frame1_1.pack(fill="x")
        key_frame2.pack(fill="x")
        key_frame2_1.pack(side="left", anchor="center")
        key_frame2_2.pack(side="right", anchor="center")
        key_1.pack(side="left", anchor="center", pady="5")
        key_entry.pack(side="left", anchor="center", padx="15")
        warning.pack(anchor="center", fill="x")
        quit_btn.pack()
        save_btn.pack()
        key_entry.bind("<Escape>", change_key_quit_key)
        key_entry.bind("<Return>", change_key_save_key)
        warning.bind("<Button-1>", open_link)


    def add_table_quit_key(e):
        str(e)
        add_table_quit()

    def add_table_quit():
        add_table_frame.forget()
        info_address.config(text="")

    def add_table_save_key(e):
        str(e)
        add_table_save()

    def add_table_save():
        name = to_add_table.get()
        if name == "":
            info_address.config(text="No Address has been provided!", fg="#ff3f34")
        elif name == " ":
            info_address.config(text="No Address has been provided!", fg="#ff3f34")
        else:
            try:
                name = name.replace(" ", "_1_SPACE_1_")
                name = name.replace(".", "_2_DOT_2_")
                name = name.replace("@", "_3_AT_3_")
                name = name.replace("-", "_4_HYPHEN_4_")
                sql = f'CREATE TABLE {name}(service LONGTEXT, passwd LONGTEXT)'
                db_cursor.execute(sql)
                db.commit()
                main()
                info_address.config(text="Success!", fg="#05c46b")
            except mysql.connector.errors.ProgrammingError:
                info_address.config(text="An error has occurred!", fg="#ff3f34")

    def add_table():
        global add_table_frame, to_add_table
        add_table_frame = tk.Frame(root, pady=5, padx=5, bg="#485460")
        add_table_frame1 = tk.Frame(add_table_frame, bg="#0fbcf9")
        add_table_frame2 = tk.Frame(add_table_frame)
        add_table_frame2_1 = tk.Frame(add_table_frame2)
        add_table_frame2_2 = tk.Frame(add_table_frame2)
        label_1 = tk.Label(add_table_frame1, text="Address: ", width=6, bg="#0fbcf9", anchor="w", justify="left")
        to_add_table = tk.Entry(add_table_frame1, width=33, bg="#4bcffa", borderwidth=0)
        quit_btn = tk.Button(add_table_frame2_1, text="Quit", borderwidth=0, bg="#ff3f34", activebackground="#ff3f34", width=19, command=add_table_quit)
        save_btn = tk.Button(add_table_frame2_2, text="Add", borderwidth=0, bg="#05c46b", activebackground="#05c46b", width=19, command=add_table_save)

        add_table_frame.pack(pady=40, padx=5, anchor="n")
        add_table_frame1.pack(fill="x")
        add_table_frame2.pack(fill="x")
        add_table_frame2_1.pack(side="left", anchor="center")
        add_table_frame2_2.pack(side="right", anchor="center")
        label_1.pack(side="left", anchor="center", pady="5")
        to_add_table.pack(side="left", anchor="center", padx="15")
        quit_btn.pack()
        save_btn.pack()
        to_add_table.bind("<Escape>", add_table_quit_key)
        to_add_table.bind("<Return>", add_table_save_key)
        to_add_table.focus()

    def remove_table_quit_key(e):
        str(e)
        remove_table_quit()

    def remove_table_quit():
        remove_table_frame.forget()
        info_address.config(text="")

    def remove_table_save_key(e):
        str(e)
        remove_table_save()

    def remove_table_save():
        address = to_remove_table.get()
        if address == "":
            info_address.config(text="No Address has been provided", fg="#ff3f34")
        else:
            address = address.replace(" ", "_1_SPACE_1_")
            address = address.replace(".", "_2_DOT_2_")
            address = address.replace("@", "_3_AT_3_")
            address = address.replace("-", "_4_HYPHEN_4_")
            sql = f'DROP TABLE IF EXISTS {address}'
            db_cursor.execute(sql)
            db.commit()
            info_address.config(text="Success!", fg="#05c46b")
            main()

    def remove_table():
        global remove_table_frame, to_remove_table
        remove_table_frame = tk.Frame(root, pady=5, padx=5, bg="#485460")
        remove_table_frame1 = tk.Frame(remove_table_frame, bg="#0fbcf9")
        remove_table_frame2 = tk.Frame(remove_table_frame)
        remove_table_frame2_1 = tk.Frame(remove_table_frame2)
        remove_table_frame2_2 = tk.Frame(remove_table_frame2)
        label_1 = tk.Label(remove_table_frame1, text="Address: ", width=6, bg="#0fbcf9", anchor="w", justify="left")
        to_remove_table = tk.Entry(remove_table_frame1, width=33, bg="#4bcffa", borderwidth=0)
        quit_btn = tk.Button(remove_table_frame2_1, text="Quit", borderwidth=0, bg="#ff3f34", activebackground="#ff3f34", width=19, command=remove_table_quit)
        save_btn = tk.Button(remove_table_frame2_2, text="Remove", borderwidth=0, bg="#05c46b", activebackground="#05c46b", width=19, command=remove_table_save)

        remove_table_frame.pack(pady=40, padx=5, anchor="n")
        remove_table_frame1.pack(fill="x")
        remove_table_frame2.pack(fill="x")
        remove_table_frame2_1.pack(side="left", anchor="center")
        remove_table_frame2_2.pack(side="right", anchor="center")
        label_1.pack(side="left", anchor="center", pady="5")
        to_remove_table.pack(side="left", anchor="center", padx="15")
        quit_btn.pack()
        save_btn.pack()
        to_remove_table.bind("<Escape>", remove_table_quit_key)
        to_remove_table.bind("<Return>", remove_table_save_key)
        to_remove_table.focus()

    global tables1
    tables1 = tk.Frame(root, bg="#1e272e")
    tables1.pack()

    if restore_other_table == "True":
        try:
            sql_add_other = f'CREATE TABLE other(service LONGTEXT, passwd LONGTEXT)'
            db_cursor.execute(sql_add_other)
            db.commit()
        except mysql.connector.errors.ProgrammingError:
            pass
    else:
        pass

    for one_table in tables:
        def table(this_table=one_table):
            global var
            var = str(this_table)
            var = var.replace("\'", "")
            var = var.replace(",", "")
            var = var.replace("(", "")
            var = var.replace(")", "")
            sql = f'SELECT * FROM {var}'
            db_cursor.execute(sql)
            data = db_cursor.fetchall()
            bottom_bar_main.forget()
            for t in tables:
                for d in data:
                    str(d)
                    tableD["table{0}".format(t)].forget()
            try:
                add_table_frame.forget()
            except NameError:
                pass
            try:
                remove_table_frame.forget()
            except NameError:
                pass
            try:
                error_label.forget()
            except NameError:
                pass

            def start_command(e):
                str(e)
                for y in data:
                    contD["cont{0}".format(y)].forget()
                top_bar.forget()
                bottom_bar_table.forget()
                try:
                    add_data_frame.forget()
                except NameError:
                    pass
                try:
                    update_data_frame.forget()
                except NameError:
                    pass
                try:
                    remove_data_frame.forget()
                except NameError:
                    pass
                try:
                    nothing_found_frame.forget()
                except NameError:
                    pass
                try:
                    error_label.forget()
                except NameError:
                    pass
                main()

            def add_data_gen_pw():
                characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
                random.shuffle(characters)
                gen_password = []
                for i in range(pw_gen_len):
                    gen_password.append(random.choice(characters))
                random.shuffle(gen_password)
                gen_password = "".join(gen_password)
                entry_2.delete(0, "end")
                entry_2.insert("end", gen_password)



            def add_data_quit_key(e):
                str(e)
                info_table.config(text="")
                add_data_quit()

            def add_data_quit():
                add_data_frame.forget()

            def add_data_save_key(e):
                str(e)
                add_data_save()

            def add_data_save():
                address = str(var)
                service = entry_1.get()
                passwd = entry_2.get()

                def load_key_en():
                    return open("key", "rb").read()
                to_encode = passwd.encode()
                key_en = load_key_en()
                f_en = Fernet(key_en)
                encoded = f_en.encrypt(to_encode)
                encoded = str(encoded)[:-1]
                encoded = encoded[2:]
                service = service.replace("\\", "(-BACKSLASH-)")
                if address == "":
                    info_table.config(text="No Address has been provided!", fg="#ff3f34")
                elif service == "":
                    info_table.config(text="No Service has been provided!", fg="#ff3f34")
                elif passwd == "":
                    info_table.config(text="No Password has been provided!", fg="#ff3f34")
                else:
                    dat = f'"{service}", "{encoded}"'
                    sql_add_data = f'INSERT INTO {address} VALUE ({dat})'
                    db_cursor.execute(sql_add_data)
                    db.commit()
                    info_table.config(text="Success!", fg="#05c46b")
                    add_data_quit()
                    refresh_data_command()

            def add_data():
                global add_data_frame, entry_1, entry_2
                add_data_frame = tk.Frame(root, pady=5, padx=5, bg="#485460")
                add_data_frame1 = tk.Frame(add_data_frame, bg="#0fbcf9")
                add_data_frame2 = tk.Frame(add_data_frame, bg="#ffa801")
                add_data_frame3 = tk.Frame(add_data_frame)
                add_data_frame4 = tk.Frame(add_data_frame)
                add_data_frame4_1 = tk.Frame(add_data_frame4)
                add_data_frame4_2 = tk.Frame(add_data_frame4)
                label_1 = tk.Label(add_data_frame1, text="Service: ", width=6, bg="#0fbcf9", anchor="w", justify="left")
                entry_1 = tk.Entry(add_data_frame1, width=33, bg="#4bcffa", borderwidth=0)
                label_2 = tk.Label(add_data_frame2, text="Password: ", bg="#ffa801")
                entry_2 = tk.Entry(add_data_frame2, bg="#ffc048", borderwidth=0, width=33)
                gen_pw_btn = tk.Button(add_data_frame3, text="Generate Password", borderwidth=0, bg="#ffd32a", activebackground="#ffd32a", command=add_data_gen_pw)
                quit_btn = tk.Button(add_data_frame4_1, text="Quit", borderwidth=0, bg="#ff3f34", activebackground="#ff3f34", width=19, command=add_data_quit)
                save_btn = tk.Button(add_data_frame4_2, text="Save", borderwidth=0, bg="#05c46b", activebackground="#05c46b", width=19, command=add_data_save)
                add_data_frame.pack(pady=40, padx=5, anchor="n")
                add_data_frame1.pack(fill="x")
                add_data_frame2.pack(fill="x")
                add_data_frame3.pack(fill="x")
                add_data_frame4.pack(fill="x")
                add_data_frame4_1.pack(side="left", anchor="center")
                add_data_frame4_2.pack(side="right", anchor="center")
                label_1.pack(side="left", anchor="center", pady="5")
                entry_1.pack(side="left", anchor="center", padx="15")
                label_2.pack(side="left", anchor="center", pady="5")
                entry_2.pack(side="left", anchor="center")
                gen_pw_btn.pack(fill="x")
                quit_btn.pack()
                save_btn.pack()
                entry_1.bind("<Escape>", add_data_quit_key)
                entry_1.bind("<Return>", add_data_save_key)
                entry_2.bind("<Escape>", add_data_quit_key)
                entry_2.bind("<Return>", add_data_save_key)
                entry_1.focus()


            def update_data_quit_key(e):
                str(e)
                update_data_quit()

            def update_data_quit():
                info_table.config(text="")
                update_data_frame.forget()

            def update_data_save_key(e):
                str(e)
                update_data_save()

            def update_data_save():
                address = str(var)
                old_service = to_update_service.get()
                new_service = to_set_service.get()
                new_passwd = to_set_passwd.get()
                no_old_service = False
                no_new_both = False
                no_new_service = False
                no_new_passwd = False
                succ = False

                def load_key_en():
                    return open("key", "rb").read()
                new_passwd = new_passwd.encode()
                key_en = load_key_en()
                f_en = Fernet(key_en)
                new_passwd = f_en.encrypt(new_passwd)
                new_passwd = str(new_passwd)[:-1]
                new_passwd = new_passwd[2:]

                old_service = old_service.replace("\\", "(-BACKSLASH-)")
                new_service = new_service.replace("\\", "(-BACKSLASH-)")

                if old_service == "":
                    no_old_service = True
                elif new_service == "" and new_passwd == "":
                    no_new_both = True
                elif new_service == "":
                    new_service = old_service
                    no_new_service = True
                elif new_passwd == "":
                    sql_ud = f'SELECT * FROM {var}'
                    db_cursor.execute(sql_ud)
                    dat = db_cursor.fetchall()
                    for v in dat:
                        if v[0] == old_service:
                            new_passwd = v[1]
                    no_new_passwd = True
                if old_service != "" and new_service != "" and new_passwd != "":
                    sql_remove_data_1 = f'UPDATE {address} SET service = \'{new_service}\' WHERE service = \'{old_service}\''
                    sql_remove_data_2 = f'UPDATE {address} SET passwd = \'{new_passwd}\' WHERE service = \'{new_service}\''
                    db_cursor.execute(sql_remove_data_1)
                    db_cursor.execute(sql_remove_data_2)
                    db.commit()
                    succ = True
                else:
                    info_table.config(text="Unknown Error!", fg="#ff3f34")

                if no_old_service is True:
                    info_table.config(text="No Service to edit has been provided!", fg="#ff3f34")
                elif no_new_both:
                    info_table.config(text="No new Service and Password has been provided!", fg="#ff3f34")
                elif no_new_service is True:
                    info_table.config(text="Password has been edited and Service stayed the same!", fg="#05c46b")
                elif no_new_passwd is True:
                    info_table.config(text="Service has been edited and Password stayed the same!", fg="#05c46b")
                elif succ is True:
                    info_table.config(text="Success!", fg="#05c46b")

                update_data_quit()
                refresh_data_command()



            def update_data():
                global update_data_frame, to_update_service, to_set_service, to_set_passwd
                update_data_frame = tk.Frame(root, pady="2.5", padx="2.5", bg="#485460")
                update_data_frame_old = tk.Frame(update_data_frame)
                update_data_frame_new = tk.Frame(update_data_frame)
                update_data_frame_old_1 = tk.Frame(update_data_frame_old, bg="#0fbcf9")
                update_data_frame_old_2 = tk.Frame(update_data_frame_old, bg="#0fbcf9")
                update_data_frame_new_1 = tk.Frame(update_data_frame_new, bg="#ffa801")
                update_data_frame_new_2 = tk.Frame(update_data_frame_new, bg="#ffa801")
                update_data_frame_new_3 = tk.Frame(update_data_frame_new, bg="#ffa801")
                update_data_frame_btn = tk.Frame(update_data_frame_new)
                update_data_frame_btn_1 = tk.Frame(update_data_frame_btn)
                update_data_frame_btn_2 = tk.Frame(update_data_frame_btn)
                now_label = tk.Label(update_data_frame_old_1, text="Old:", bg="#0fbcf9")
                now_service = tk.Label(update_data_frame_old_2, text="Service: ", width=8, bg="#0fbcf9", anchor="w", justify="left")
                to_update_service = tk.Entry(update_data_frame_old_2, width=33, bg="#4bcffa", borderwidth=0)
                new_label = tk.Label(update_data_frame_new_1, text="New:", bg="#ffa801")
                new_service = tk.Label(update_data_frame_new_2, text="Service: ", width=8, bg="#ffa801", anchor="w", justify="left")
                to_set_service = tk.Entry(update_data_frame_new_2, width=33, bg="#ffc048", borderwidth=0)
                new_passwd = tk.Label(update_data_frame_new_3, text="Password: ", width=8, bg="#ffa801", anchor="w", justify="left")
                to_set_passwd = tk.Entry(update_data_frame_new_3, width=33, bg="#ffc048", borderwidth=0)
                quit_btn = tk.Button(update_data_frame_btn_1, text="Quit", borderwidth=0, bg="#ff3f34", activebackground="#ff3f34", width=20, command=update_data_quit)
                update_btn = tk.Button(update_data_frame_btn_2, text="Update", borderwidth=0, bg="#05c46b", activebackground="#05c46b", width=20, command=update_data_save)
                update_data_frame.pack(pady=10, padx=5, anchor="n")
                update_data_frame_old.pack(fill="x", pady="2.5", padx="2.5")
                update_data_frame_new.pack(fill="x", pady="2.5", padx="2.5")
                update_data_frame_old_1.pack(fill="x")
                update_data_frame_old_2.pack(fill="x")
                update_data_frame_new_1.pack(fill="x")
                update_data_frame_new_2.pack(fill="x")
                update_data_frame_new_3.pack(fill="x")
                update_data_frame_btn.pack(fill="x")
                update_data_frame_btn_1.pack(side="left", anchor="center")
                update_data_frame_btn_2.pack(side="right", anchor="center")
                now_label.pack(pady="5")
                now_service.pack(side="left", anchor="center", pady="5")
                to_update_service.pack(side="left", anchor="center", padx="15", pady="5")
                new_label.pack(pady="5")
                new_service.pack(side="left", anchor="center", pady="5")
                to_set_service.pack(side="left", anchor="center", padx="15", pady="5")
                new_passwd.pack(side="left", anchor="center", pady="5")
                to_set_passwd.pack(side="left", anchor="center", padx="15", pady="15")
                quit_btn.pack()
                update_btn.pack()
                to_update_service.bind("<Escape>", update_data_quit_key)
                to_update_service.bind("<Return>", update_data_save_key)
                to_set_service.bind("<Escape>", update_data_quit_key)
                to_set_service.bind("<Return>", update_data_save_key)
                to_set_passwd.bind("<Escape>", update_data_quit_key)
                to_set_passwd.bind("<Return>", update_data_save_key)
                to_update_service.focus()


            def remove_data_quit_key(e):
                str(e)
                remove_data_quit()

            def remove_data_quit():
                remove_data_frame.forget()

            def remove_data_remove_key(e):
                str(e)
                remove_data_remove()

            def remove_data_remove():
                address = str(var)
                dat = to_remove.get()
                dat = dat.replace("\\", "(-BACKSLASH-)")
                if address == "":
                    info_table.config(text="No Address has been provided!", fg="#ff3f34")
                elif dat == "":
                    info_table.config(text="No Service has been provided!", fg="#ff3f34")
                else:
                    sql_remove_data = f'DELETE FROM {address} WHERE service=\"{dat}\"'
                    db_cursor.execute(sql_remove_data)
                    db.commit()
                    info_table.config(text="Success!", fg="#05c46b")
                refresh_data_command()

            def remove_data():
                global remove_data_frame, to_remove
                remove_data_frame = tk.Frame(root, pady=5, padx=5, bg="#485460")
                remove_data_frame1 = tk.Frame(remove_data_frame, bg="#0fbcf9")
                remove_data_frame2 = tk.Frame(remove_data_frame)
                remove_data_frame2_1 = tk.Frame(remove_data_frame2)
                remove_data_frame2_2 = tk.Frame(remove_data_frame2)
                label_1 = tk.Label(remove_data_frame1, text="Service: ", width=6, bg="#0fbcf9", anchor="w", justify="left")
                to_remove = tk.Entry(remove_data_frame1, width=33, bg="#4bcffa", borderwidth=0)
                quit_btn = tk.Button(remove_data_frame2_1, text="Quit", borderwidth=0, bg="#ff3f34", activebackground="#ff3f34", width=19, command=remove_data_quit)
                remove_btn = tk.Button(remove_data_frame2_2, text="Remove", borderwidth=0, bg="#05c46b", activebackground="#05c46b", width=19, command=remove_data_remove)

                remove_data_frame.pack(pady=40, padx=5, anchor="n")
                remove_data_frame1.pack(fill="x")
                remove_data_frame2.pack(fill="x")
                remove_data_frame2_1.pack(side="left", anchor="center")
                remove_data_frame2_2.pack(side="right", anchor="center")
                label_1.pack(side="left", anchor="center", pady="5")
                to_remove.pack(side="left", anchor="center", padx="15")
                quit_btn.pack()
                remove_btn.pack()
                to_remove.bind("<Escape>", remove_data_quit_key)
                to_remove.bind("<Return>", remove_data_remove_key)
                to_remove.focus()

            global list1
            list1 = tk.Frame(root, bg="#1e272e")
            list1.pack()

            cd = str(data)
            if cd == "[]":
                for m in tables:
                    tableD["table{0}".format(m)].forget()
                global nothing_found_frame
                nothing_found_frame = tk.Frame(bg="#1e272e")
                nothing_found_img_open = Image.open("design/404.png")
                size_img = 400, 400
                nothing_found_img_open.thumbnail(size_img, Image.ANTIALIAS)
                nothing_found_img = ImageTk.PhotoImage(nothing_found_img_open)
                label2 = tk.Label(nothing_found_frame, image=nothing_found_img, bg="#1e272e")
                label2.image = nothing_found_img
                label2.pack()
                nothing_found_frame.pack(pady=20)
            else:
                show_table = tk.Frame(list1, bg="#0be881")
                table_name = var
                table_name = table_name.replace("_1_SPACE_1_", " ")
                table_name = table_name.replace("_2_DOT_2_", ".")
                table_name = table_name.replace("_3_AT_3_", "@")
                table_name = table_name.replace("_4_HYPHEN_4_", "-")
                show_table_lab = tk.Label(show_table, text=table_name, width=66, height=2, bg="#0be881")
                show_table.pack(pady=5, padx=5, fill="x")
                show_table_lab.pack()


            count = 0
            for x in data:
                count = count + 1

                try:
                    def load_key():
                        return open("key", "rb").read()

                    to_decode = str(x[1])
                    to_decode = "b\'" + to_decode + "\'"
                    to_decode = to_decode[2:]
                    to_decode = to_decode[:-1]
                    to_decode = to_decode.encode()
                    key_de = load_key()
                    bytes(key_de)
                    f = Fernet(key_de)
                    decoded = f.decrypt(to_decode)
                except cryptography.fernet.InvalidToken:
                    decoded = str(x[1])

                decoded = str(decoded)
                decoded = decoded.replace("\\xc3\\xb6", "ö")
                decoded = decoded.replace("\\xc3\\xa4", "ä")
                decoded = decoded.replace("\\xc3\\xbc", "ü")
                decoded = decoded.replace("\\xc2\\xb4", "´")
                decoded = decoded.replace("\\xc2\\xb0", "°")
                decoded = decoded.replace("\\xc2\\xb5", "µ")
                decoded = decoded.replace("\\xe2\\x82\\xac", "€")
                decoded = decoded.replace("\\xc2\\xb2", "²")
                decoded = decoded.replace("\\xc2\\xb3", "³")
                decoded = decoded[2:][:-1]

                service_ins = x[0]
                service_ins = service_ins.replace("(-BACKSLASH-)", "\\")

                def copy(to_copy=str(decoded)):
                    tc = to_copy
                    tc = tc[2:]
                    tc = tc[:-1]
                    pyperclip.copy(tc)

                contD["cont{0}".format(x)] = tk.Frame(list1, bg="#0fbcf9")
                linesD["lines0{0}".format(x)] = tk.Label(contD["cont{0}".format(x)], text="Service: " + service_ins, width=33, height=1, bg="#0fbcf9", anchor="w", justify="left")
                cont1D["cont1{0}".format(x)] = tk.Frame(contD["cont{0}".format(x)], bg="#ffa801")
                linesD["lines1{0}".format(x)] = tk.Label(cont1D["cont1{0}".format(x)], text="Password: ", width=7, bg="#ffa801")
                linesD["lines2{0}".format(x)] = tk.Entry(cont1D["cont1{0}".format(x)], width=25, bg="#ffc048", borderwidth=0)
                copyD["copy{0}".format(x)] = tk.Button(cont1D["cont1{0}".format(x)], height=1, width=5, bg="#ffc048", activebackground="#ffc048", borderwidth=0, text="copy", command=copy)

                if count <= 17:
                    contD["cont{0}".format(x)].pack(pady=5, padx=5, fill="x")
                    linesD["lines0{0}".format(x)].pack(side="left", anchor="center")
                    cont1D["cont1{0}".format(x)].pack(fill="x")
                    linesD["lines1{0}".format(x)].pack(side="left", anchor="center", padx=10)
                    linesD["lines2{0}".format(x)].pack(side="left", anchor="center", padx=20)
                    linesD["lines2{0}".format(x)].insert("end", decoded)
                    copyD["copy{0}".format(x)].pack(side="left", anchor="center")


            global bottom_bar_table
            bottom_bar_table = tk.Frame(root, bg="#1e272e")
            info_frame = tk.Frame(bottom_bar_table, bg="#1e272e")
            buttons = tk.Frame(bottom_bar_table, bg="#1e272e")
            info_table = tk.Label(info_frame, text="", borderwidth=0, bg="#1e272e", fg="#05c46b")
            add_data = tk.Button(buttons, text="Add Service", command=add_data, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
            update_data = tk.Button(buttons, text="Update Service", command=update_data, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
            remove_data = tk.Button(buttons, text="Remove Service", command=remove_data, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
            refresh_data = tk.Button(buttons, text="Refresh", command=refresh_data_command, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
            bottom_bar_table.pack(pady=5, anchor="s", side="bottom", fill="x")
            info_frame.pack()
            buttons.pack()
            info_table.pack()
            add_data.pack(side="left", anchor="center", padx=5)
            update_data.pack(side="left", anchor="center", padx=5)
            remove_data.pack(side="left", anchor="center", padx=5)
            refresh_data.pack(side="left", anchor="center", padx=5)
            label1.bind("<Button-1>", start_command)


        text = str(one_table[0])
        text = text.replace("_1_SPACE_1_", " ")
        text = text.replace("_2_DOT_2_", ".")
        text = text.replace("_3_AT_3_", "@")
        text = text.replace("_4_HYPHEN_4_", "-")
        tableD["table{0}".format(one_table)] = tk.Button(root, text=text, command=table, width=60, height=3, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
        tableD["table{0}".format(one_table)].pack(pady=5, padx=5)

    global bottom_bar_main
    bottom_bar_main = tk.Frame(root, bg="#1e272e")
    bottom_bar_1 = tk.Frame(bottom_bar_main, bg="#1e272e")
    bottom_bar_2 = tk.Frame(bottom_bar_main, bg="#1e272e")
    bottom_bar_3 = tk.Frame(bottom_bar_main, bg="#1e272e")
    info_address = tk.Label(bottom_bar_1, text="", bg="#1e272e", fg="#05c46b")
    help = tk.Button(bottom_bar_2, text="Help", command=help, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
    change_key = tk.Button(bottom_bar_2, text="Change Key", command=change_key, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
    add_address = tk.Button(bottom_bar_2, text="Add Address", command=add_table, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
    remove_address = tk.Button(bottom_bar_2, text="Remove Address", command=remove_table, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
    refresh = tk.Button(bottom_bar_3, text="Refresh", command=main, font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881")
    bottom_bar_main.pack(pady=20, anchor="s", side="bottom")
    bottom_bar_1.pack(pady="5")
    bottom_bar_2.pack(side="left", anchor="center")
    bottom_bar_3.pack(side="left", anchor="center")
    info_address.pack(side="left", anchor="center")
    help.pack(side="left", anchor="center", padx=5)
    change_key.pack(side="left", anchor="center", padx=5)
    add_address.pack(side="left", anchor="center", padx=5)
    remove_address.pack(side="left", anchor="center", padx=5)
    refresh.pack(side="left", anchor="center", padx=5)


    def refresh_data_command():
        main()
        table(this_table=var)


def refresh_forget():
    try:
        top_bar.forget()
    except NameError:
        pass
    try:
        bottom_bar_main.forget()
    except NameError:
        pass
    try:
        tables1.forget()
    except NameError:
        pass
    try:
        add_table_frame.forget()
    except NameError:
        pass
    try:
        remove_table_frame.forget()
    except NameError:
        pass
    try:
        add_data_frame.forget()
    except NameError:
        pass
    try:
        update_data_frame.forget()
    except NameError:
        pass
    try:
        remove_data_frame.forget()
    except NameError:
        pass
    try:
        nothing_found_frame.forget()
    except NameError:
        pass
    try:
        list1.forget()
    except NameError:
        pass
    try:
        bottom_bar_table.forget()
    except NameError:
        pass
    try:
        login_frame.forget()
    except NameError:
        pass
    try:
        error_label.forget()
    except NameError:
        pass
    try:
        for t in tables:
            tableD["table{0}".format(t)].forget()
    except NameError:
        pass



login()
root.mainloop()
