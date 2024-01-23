from tkinter import *
from tkinter import messagebox
import ttkbootstrap as ttk
from dml import App
from getpass import getpass


###### LOGIN ######
class Log(Tk):
  
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        self.title('Login to the system')
        self.geometry("300x300")
        self.config(bg='pink')
        
        self.style = ttk.Style("superhero")
        
        self.create_widget()
        self.bind('<Return>', self.log_in_enter)
        self.etr_login.focus()
    
    def create_widget(self):    
        self.lbl_welcome = Label(self, text= 'Welcome back', font=("Arial", 20, 'italic'), bg='pink')
        self.lbl_login = Label(self, text= 'Enter login', font=("Arial", 15), bg='pink')
        self.lbl_password = Label(self, text= 'Enter password', font=("Arial", 15), bg='pink')
        self.etr_login = Entry(self, font=("Arial", 10))
        self.etr_password = Entry(self, show='*', font=("Arial", 10))
        self.btn_login = Button(self, text='LOG IN', command=self.log_in, font=("Arial", 12, 'bold'))
        self.btn_help = Button(self, text='Call a friend?', command=self.call_friend, font=("Arial", 12))
        
        self.lbl_welcome.pack(pady=5)
        self.lbl_login.pack(pady=5)
        self.etr_login.pack(pady=5)
        self.lbl_password.pack(pady=5)
        self.etr_password.pack(pady=5)
        self.btn_login.pack(pady=5)
        self.btn_help.pack(pady=5)
        
    def log_in(self):
        login = self.etr_login.get()
        password = self.etr_password.get()
        if (login == 'login') and (password == 'password'):
            app = App()
            app.start()
        else:
            messagebox.showerror('NOOO', 'hihihihi\nincorrectly values!!!!')
            self.etr_login.focus()
    
    def log_in_enter(self, event):
        login = self.etr_login.get()
        password = self.etr_password.get()
        if (login == 'login') and (password == 'password'):
            app = App()
            app.start()
            pass
        else:
            messagebox.showerror('NOOO', 'incorrectly values!!!!')
            self.etr_login.focus()
            
    def call_friend(self):
        messagebox.showwarning("Again my Friend", "Really, you can't remember\nsuch trivial things\n\nlogin and password\nmy dear Friend")
    
    def start(self):
        self.mainloop()

###### LOGIN_CMD ######

def login_win():
    while True:
        login = input('Enter login: ')
        password = getpass('Enter password: ')
        if (login == 'login') and (password == 'password'):
            app = App()
            app.start()
            break
        else:
            print('\nNOOO\nincorrectly values!!!!\n')
           