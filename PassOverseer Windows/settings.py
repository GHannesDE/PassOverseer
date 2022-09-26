import tkinter as tk
from PIL import Image, ImageTk
from win32api import GetSystemMetrics

root = tk.Tk()
w = GetSystemMetrics(0) / 100 * 67
w = str(w).split(".")
w = w[0]
h = GetSystemMetrics(1) / 100 * 94
h = str(h).split(".")
h = h[0]
ofs = GetSystemMetrics(0) / 100 * 32.5
ofs = str(ofs).split(".")
ofs = ofs[0]
geo = str(w) + "x" + str(h) + "+" + ofs + "+0"
root.geometry(geo)
root.resizable(False, False)
root.configure(bg="#1e272e")
root.wm_title("Settings")
root.iconbitmap("design\settings-icon.ico")

top_bar = tk.Frame(bg="#1e272e")
logo = Image.open("design/settings-logo.png")
size = 1000, 1000
logo.thumbnail(size, Image.ANTIALIAS)
img = ImageTk.PhotoImage(logo)
label1 = tk.Label(top_bar, image=img, bg="#1e272e")
label1.image = img
label1.pack()
top_bar.pack()


def main():
    def reset_settings():
        with open("settings", "w", encoding="UTF-8") as settings_c:
            global restore_other_table, pw_gen_len
            settings_c.write("restore_other_table=True #Here you can choose whether the address \"other\" should be restored automatically and you can decide between \"True\"(on) and \"False\"(off)\npw_gen_len=10 #Here you can choose what length your generated passwords should have")
            restore_other_table = "True"
            pw_gen_len = 10
        reload_all()

    global restore_other_state
    with open("settings", "r", encoding="UTF-8") as get_restore_other_state:
        restore_other_state = get_restore_other_state.readline()
    restore_other_state = restore_other_state.replace(" #Here you can choose whether the address \"other\" should be restored automatically and you can decide between \"True\"(on) and \"False\"(off)", "")
    restore_other_state = restore_other_state.replace("restore_other_table=", "")
    restore_other_state = restore_other_state.replace("\n", "")
    if restore_other_state == "True":
        restore_other_state = True
    elif restore_other_state == "False":
        restore_other_state = False
    else:
        reset_settings()


    def switch_setting_1_checkbox(e):
        str(e)
        global switch
        if switch is True:
            switch = False
            setting_1_checkbox.config(text=" Off ", bg="#ff3f34", activebackground="#ff3f34")
        elif switch is False:
            switch = True
            setting_1_checkbox.config(bg="#0be881", activebackground="#0be881", text="  On  ")

    global setting_1_frame, setting_2_frame, bottom_bar_table, info_frame, buttons, switch

    setting_1_frame = tk.Frame(root, bg="#0fbcf9", height="2")
    setting_1_name = tk.Label(setting_1_frame, text="Restore \"other\" Address", width=33, height=2, bg="#0fbcf9", anchor="w", justify="left")
    setting_1_checkbox = tk.Label(setting_1_frame, bg="#0be881", activebackground="#0be881", text="  On  ")
    if restore_other_state is True:
        setting_1_checkbox.config(bg="#0be881", activebackground="#0be881", text="  On  ")
        switch = True
    elif restore_other_state is False:
        setting_1_checkbox.config(text=" Off ", bg="#ff3f34", activebackground="#ff3f34")
        switch = False
    setting_1_frame.pack(pady=5, padx=100, fill="x")
    setting_1_name.pack(side="left", anchor="center", padx=10)
    setting_1_checkbox.pack(side="right", anchor="center", padx=50)
    setting_1_checkbox.bind("<Button-1>", switch_setting_1_checkbox)

    setting_2_frame = tk.Frame(root, bg="#0fbcf9", height="2")
    setting_2_name = tk.Label(setting_2_frame, text="Generated Password length", width=33, height=2, bg="#0fbcf9", anchor="w", justify="left")
    setting_2_entry = tk.Entry(setting_2_frame, borderwidth=0, width=5, justify='center')
    setting_2_frame.pack(pady=5, padx=100, fill="x")
    setting_2_name.pack(side="left", anchor="center", padx=10)
    setting_2_entry.pack(side="right", anchor="center", padx=50)

    with open("key", "rb") as key_rb:
        key_rb_var = key_rb.read()
    setting_3_frame = tk.Frame(root, bg="#0fbcf9", height="2")
    setting_3_name = tk.Label(setting_3_frame, text="Encryption Key", width=33, height=2, bg="#0fbcf9", anchor="w", justify="left")
    setting_3_entry = tk.Entry(setting_3_frame, borderwidth=0, width=48, justify='center')
    setting_3_frame.pack(pady=5, padx=100, fill="x")
    setting_3_name.pack(side="left", anchor="center", padx=10)
    setting_3_entry.pack(side="right", anchor="center", padx=50)
    setting_3_entry.insert("end", key_rb_var)

    def save():
        to_write_settings = "restore_other_table=" + str(switch) + " #Here you can choose whether the address \"other\" should be restored automatically and you can decide between \"True\"(on) and \"False\"(off)\n" + "pw_gen_len=" + setting_2_entry.get() + " #Here you can choose what length your generated passwords should have"
        with open("settings", "w", encoding="UTF-8") as save_write_settings:
            save_write_settings.write(to_write_settings)
        with open("key", "w") as save_write_key:
            save_write_key.write(setting_3_entry.get())

        with open("key_history", "r") as check_last_key:
            all_keys = check_last_key.read()
        last_key = all_keys.split("\n")
        if last_key[0] == setting_3_entry.get():
            pass
        else:
            new_all_keys = setting_3_entry.get() + "\n" + all_keys
            with open("key_history", "w") as write_history:
                write_history.write(new_all_keys)

        info.config(text="Saved!", fg="#0be881")

    bottom_bar_table = tk.Frame(root, bg="#1e272e")
    info_frame = tk.Frame(bottom_bar_table, bg="#1e272e")
    buttons = tk.Frame(bottom_bar_table, bg="#1e272e")
    info = tk.Label(info_frame, text="", borderwidth=0, bg="#1e272e", fg="#0be881")
    save_btn = tk.Button(buttons, text="Save", font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881", command=save)
    reset_btn = tk.Button(buttons, text="Reset Settings", font="Ubuntu", borderwidth=0, bg="#0be881", activebackground="#0be881", command=reset_settings)
    bottom_bar_table.pack(pady=5, anchor="s", side="bottom", fill="x")
    info_frame.pack()
    buttons.pack()
    info.pack()
    save_btn.pack(side="left", anchor="center", padx=5)
    reset_btn.pack(side="left", anchor="center", padx=5)


    with open("settings", "r", encoding="UTF-8") as get_pw_length:
        pw_length = get_pw_length.read()
    pw_length = pw_length.split("\n")
    pw_length = pw_length[1]
    pw_length = pw_length.replace(" #Here you can choose what length your generated passwords should have", "")
    pw_length = pw_length.replace("pw_gen_len=", "")
    setting_2_entry.insert("end", pw_length)


def reload_all():
    try:
        setting_1_frame.forget()
    except NameError:
        pass
    try:
        bottom_bar_table.forget()
    except NameError:
        pass
    try:
        info_frame.forget()
    except NameError:
        pass
    try:
        buttons.forget()
    except NameError:
        pass
    try:
        setting_2_frame.forget()
    except NameError:
        pass
    main()

main()
root.mainloop()