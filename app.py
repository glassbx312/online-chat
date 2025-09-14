from customtkinter import *
from PIL import Image
import socket
import threading

class App(CTk):
    def __init__(self):
        super().__init__()
        self.is_menu = False
        self.menu_animation = -15
        self.geometry("500x400")
        self.title('LogiTalk')
        """MENU"""
        self.menu_frame = CTkFrame(self, fg_color="#3e65f0", width=30, height=400)
        self.menu_frame.place(x=0, y=0)
        self.menu_frame.pack_propagate(False)
        # self.name_lbl = CTkLabel(self, text="Введіть ім'я", font=("Helvetica", 20, "bold"))
        self.btn_menu = CTkButton(self.menu_frame, text=">", font=("Helvetica", 20, "bold"), command=self.toggle_menu)
        self.btn_menu.place(x=0, y=0, relwidth=1)
        """SCROLL FRAME"""
        self.scroll_frame = CTkScrollableFrame(self, fg_color="#2bffa0")
        self.scroll_frame.place(x=0, y=0)
        """SEND ENTRY AND BUTTON"""
        self.msg_text_entry = CTkEntry(self, height=45, placeholder_text="Введіть текст повідомлення")
        self.msg_text_entry.place(x=0, y=0)
        self.btn_send = CTkButton(self, text=">", width=45, height=45, command=self.send_msgs)
        self.btn_send.place(x=0, y=0)

        self.adaptive_ui()

        self.name = None

    def show_menu(self):
        self.menu_frame.configure(width=self.menu_frame.winfo_width() + self.menu_animation)
        if self.is_menu and not self.menu_frame.winfo_width() >= 200:
            self.after(10, self.show_menu)
        elif not self.is_menu and self.menu_frame.winfo_width() >= 50:
            self.after(10, self.show_menu)
            if self.name_lbl and self.name_entry and self.btn_save:
                self.name_lbl.destroy()
                self.name_entry.destroy()
                self.btn_save.destroy()

    def toggle_menu(self):
        if self.is_menu:
            self.is_menu = False
            self.menu_animation *= -1
            self.btn_menu.configure(text =">")
            self.show_menu()
        else:
            self.is_menu = True
            self.menu_animation *= -1
            self.btn_menu.configure(text="<")
            self.show_menu()
            self.name_lbl = CTkLabel(self.menu_frame, text="Введіть ім'я", font=("Helvatica", 20, "bold"))
            self.name_entry = CTkEntry(self.menu_frame, width=100, placeholder_text="Введіть ім'я")
            self.btn_save = CTkButton(self.menu_frame, text = "Зберегти", command=self.save_name, font=("Helvatica", 20, "bold"))
            self.name_lbl.pack(pady=40)
            self.name_entry.pack()
            self.btn_save.pack(pady=10)

    def save_name(self):
        if self.name_entry.get():
            self.name = self.name_entry.get()
            self.name_entry.delete(0, END)
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(("7.tcp.eu.ngrok.io", 18986))
                self.sock.send(self.name.encode())
                threading.Thread(target=self.recv_msgs, daemon=True).start()
            except:
                self.add_recv_msg("Сервер не знайдено!,Перезапустіть додаток!")
                self.sock.close()

    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())
        self.scroll_frame.place(x=self.menu_frame.winfo_width())
        self.scroll_frame.configure(width=self.winfo_width() - self.menu_frame.winfo_width(), height=self.winfo_height() -70)

        self.msg_text_entry.place(x=self.menu_frame.winfo_width() + 5, y=self.menu_frame.winfo_height() - 55)
        self.msg_text_entry.configure(width=self.winfo_width() - self.menu_frame.winfo_width() - self.btn_send.winfo_width() - 15)
        self.btn_send.place(x=self.msg_text_entry.winfo_width() + self.menu_frame.winfo_width() + 10, y=self.winfo_height() - 55)

        self.after(50, self.adaptive_ui)

    def add_recv_msg(self, text): #Вивід повідомлень в чат
        msg_frame = CTkFrame(self.scroll_frame, fg_color="white")
        msg_frame.pack(pady=10, anchor="w")
        wrap_width = self.winfo_width() - self.menu_frame.winfo_width() - 40
        msg_lbl = CTkLabel(msg_frame, text=text, wraplength=wrap_width, justify="left")
        msg_lbl.pack(padx=10, pady=5)

    def add_send_msg(self, text):
        msg_frame = CTkFrame(self.scroll_frame, fg_color="white")
        msg_frame.pack(padx=10, pady=10, anchor="e")
        wrap_width = self.winfo_width() - self.menu_frame.winfo_width() - 40
        msg_lbl = CTkLabel(msg_frame, text="Я: " + text, wraplength=wrap_width, justify="left")
        msg_lbl.pack(padx=10, pady=5)

    def recv_msgs(self):
        while True:
            text = self.sock.recv(1024).decode()
            if text:
                self.add_recv_msg(text)

    def send_msgs(self):
        text=self.msg_text_entry.get()
        if text:
            try:
                self.sock.send(text.encode())
                self.msg_text_entry.delete(0, END)
                self.add_send_msg(text)
            except:
                pass

app = App()
app.mainloop()