from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Style
from tkintermapview import TkinterMapView
from random import uniform, randint
import ttkbootstrap as ttk
from shapely import wkb, Polygon

from sqlalchemy import create_engine, Sequence, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from geoalchemy2 import Geometry, functions


db_params = sqlalchemy.URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password='123',
    host='localhost',
    database='postgres',
    port=5432
)

engine = create_engine(db_params)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Military_training_ground(Base):
    __tablename__ = "Military_training_grounds"
    
    id = Column(Integer(), Sequence("user_id_seq"),primary_key=True)
    name = Column(String(100),nullable=True)
    location = Column('geom', Geometry(geometry_type='POLYGON', srid=4326), nullable=True)

    def __init__(self, name, area):
        self.name = name
        self.location = f'{area}'

class Soldier(Base):
    __tablename__ = "Soldiers"
    
    id = Column(Integer(), Sequence("user_id_seq"),primary_key=True)
    name = Column(String(100),nullable=True)
    role = Column(String(100),nullable=True)
    polygon = Column(String(100),nullable=True)
    location = Column('geom', Geometry(geometry_type='POINT', srid=4326), nullable=True)
    
    def __init__(self, name, polygon, role, location):
        self.name = name
        self.polygon = polygon
        self.role = role
        self.location = f'POINT({location[1]} {location[0]})'
        
Base.metadata.create_all(engine)

zasieg = [(uniform(49,55), uniform(14, 24)), (uniform(49,55), uniform(14, 24)), (uniform(49,55), uniform(14, 24)), (uniform(49,55), uniform(14, 24))]
obj = Military_training_ground('biedrowko', zasieg)


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
        else:
            messagebox.showerror('NOOO', 'incorrectly values!!!!')
            self.etr_login.focus()
            
    def call_friend(self):
        messagebox.showwarning("Again my Friend", "Really, you can't remember\nsuch trivial things\n\nlogin and password\nmy dear Friend")
    
    def start(self):
        self.mainloop()
        
class App(Tk):
    vertices = []
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        self.title('System to manage military training grounds')
        self.geometry("800x680+50+50")
        
        self.style = ttk.Style("darkly")

        self.create_widgets()
        self.after_idle(self.refresh)
        
    def create_widgets(self):
        ###### FRAME ######
        self.frame_list = Frame(self)
        self.frame_panel = Frame(self)
        self.frame_details = Frame(self)
        self.frame_map = Frame(self)
        self.frame_entry = Frame(self)
        self.frame_entry2 = Frame(self)
        
        self.frame_list.grid(row=0, column=0)
        self.frame_panel.grid(row=1, column=0)
        self.frame_details.grid(row=2, column=0)
        self.frame_map.grid(row=1, column=1, rowspan=2, columnspan=2)
        self.frame_entry.grid(row=0, column=1)
        self.frame_entry2.grid(row=0, column=2)
        
        ###### LIST ######
        self.lb_list_of_mtb = Listbox(self.frame_list)
        self.lb_list_of_soldier = Listbox(self.frame_list)
        self.lbl_lb_list_of_mtb = Label(self.frame_list, text='list of\nmilitary training ground')
        self.lbl_list_of_soldier = Label(self.frame_list, text='list of soldier')
        
        self.lb_list_of_mtb.grid(row=1, column=0)
        self.lb_list_of_soldier.grid(row=1, column=1)
        self.lbl_lb_list_of_mtb.grid(row=0,column=0)
        self.lbl_list_of_soldier.grid(row=0,column=1)
        
        ###### DETAILS ######
        self.lbl_mtb_name = Label(self.frame_details, text='name of polygon')
        self.lbl_mtb_number_of_soldier = Label(self.frame_details, text='number of soldier on polygon')
        self.lbl_soldier_name = Label(self.frame_details, text="soldier's name")
        self.lbl_soldier_coords = Label(self.frame_details, text="soldier's coord")
        self.lbl_soldier_role = Label(self.frame_details, text="soldier's role")
        self.lbl_mtb_name_value = Label(self.frame_details, text='...')
        self.lbl_mtb_number_of_soldier_value = Label(self.frame_details, text='...')
        self.lbl_soldier_name_value = Label(self.frame_details, text='...')
        self.lbl_soldier_coords_name_value = Label(self.frame_details, text='...')
        self.lbl_soldier_role_name_value = Label(self.frame_details, text='...')
        
        self.lbl_mtb_name.grid(row=1, column=0)
        self.lbl_mtb_name_value.grid(row=2, column=0)
        self.lbl_mtb_number_of_soldier.grid(row=3, column=0)
        self.lbl_mtb_number_of_soldier_value.grid(row=4, column=0)
        self.lbl_soldier_name.grid(row=5, column=0)
        self.lbl_soldier_name_value.grid(row=6, column=0)
        self.lbl_soldier_coords.grid(row=7, column=0)
        self.lbl_soldier_coords_name_value.grid(row=8, column=0)
        self.lbl_soldier_role.grid(row=9, column=0)
        self.lbl_soldier_role_name_value.grid(row=10, column=0)
        
        ###### ENTRY ######
        self.lbl_soldier_name2 = Label(self.frame_entry, text="soldier's name")
        self.lbl_soldier_coords2 = Label(self.frame_entry, text="soldier's coord")
        self.lbl_soldier_role2 = Label(self.frame_entry, text="soldier's role")        
        self.lbl_soldier_polygon2 = Label(self.frame_entry, text="soldier's polygon")        
        self.entry_soldier_name = Entry(self.frame_entry)
        self.lbl_soldier_coords3 = Label(self.frame_entry, text='choose one ->')
        self.cb_soldier_role = Combobox(self.frame_entry, textvariable=StringVar())
        self.cb_soldier_polygon = Combobox(self.frame_entry, textvariable=StringVar())
        self.lbl_new_soldier = Label(self.frame_entry, text="new soldier")
        self.lbl_new_mtb = Label(self.frame_entry, text="new polygon")
        self.lbl_mtb_name2 = Label(self.frame_entry, text="polygon's name")
        self.entry_mtb_name = Entry(self.frame_entry)
        self.lbl_list_of_vertices = Label(self.frame_entry2, text='list of vertices')
        self.list_of_vertices = Listbox(self.frame_entry2, width=35)
        
        self.cb_soldier_role["values"] = ('medic', 'sniper', 'commander', 'radio operator', 'rangefinder', 'gunner', 'sharpshooter', 'saper')
        
        self.lbl_new_soldier.grid(row=2, column=0, columnspan=2)
        self.lbl_soldier_name2.grid(row=3, column=0)
        self.entry_soldier_name.grid(row=3, column=1)
        self.lbl_soldier_coords2.grid(row=4, column=0)
        self.lbl_soldier_coords3.grid(row=4, column=1)
        self.lbl_soldier_role2.grid(row=5, column=0)
        self.cb_soldier_role.grid(row=5, column=1)
        self.lbl_soldier_polygon2.grid(row=6, column=0)
        self.cb_soldier_polygon.grid(row=6, column=1)
        
        self.lbl_new_mtb.grid(row=0, column=0, columnspan=2)
        self.lbl_mtb_name2.grid(row=1, column=0)
        self.entry_mtb_name.grid(row=1, column=1)
        
        self.lbl_list_of_vertices.grid(row=0, column=0)
        self.list_of_vertices.grid(row=1, column=0)
        
        ###### MAP ######
        self.map_widget = TkinterMapView(self.frame_map, width=500, height=450, corner_radius=45)
        self.map_widget.grid(row=0, column=0)
        self.map_widget.set_position(52, 19)
        self.map_widget.set_zoom(6)
        self.map_widget.add_left_click_map_command(self.take_coords)
        
        ###### PANEL ######
        self.btn_details = Button(self.frame_panel, text='details', command=self.delete_mtb)
        self.btn_create = Button(self.frame_panel, text='create', command=self.modify_mtb1)
        self.btn_delete = Button(self.frame_panel, text='delete', command=self.modify_mtb2)
        self.btn_edit = Button(self.frame_panel, text='edit', command=self.details_of_soldier)
        self.btn_refresh = Button(self.frame_panel, text='refresh', command=self.refresh)
        self.btn_clean = Button(self.frame_panel, text='clean', command=self.clean_map)
        self.btn_map = Button(self.frame_panel, text='selected', command=self.add_mtb)
        self.btn_map_all = Button(self.frame_panel, text='all soldiers', command=self.clear_entry)
        self.lbl_map = Label(self.frame_panel, text='print map of')
        
        self.btn_details.grid(row=0, column=0)
        self.btn_create.grid(row=1, column=0)
        self.btn_delete.grid(row=2, column=0)
        self.btn_edit.grid(row=0, column=1)
        self.btn_refresh.grid(row=1, column=1)
        self.btn_clean.grid(row=2, column=1)
        self.lbl_map.grid(row=0, column=2)
        self.btn_map.grid(row=1, column=2)
        self.btn_map_all.grid(row=2, column=2)

    def convert_point(self, point):
        point = wkb.loads(str(point), hex=True)
        return (point.y, point.x)
        
    def clean_map(self):
        self.map_widget.delete_all_marker()
        self.map_widget.delete_all_polygon() 

    def refresh(self):
        self.lb_list_of_mtb.delete(0,END)
        db_mtb = session.query(Military_training_ground).all()
        for idx, mtb in enumerate(db_mtb):
            self.lb_list_of_mtb.insert(idx,f'{mtb.name}')
        
        db_soldiers = session.query(Soldier).all()
        self.lb_list_of_soldier.delete(0,END)
        for idx, soldier in enumerate(db_soldiers):
            self.lb_list_of_soldier.insert(idx,f'{soldier.name} - {soldier.role}')
            
        lm = []
        for x in db_mtb:
            lm.append(x.name)
            self.cb_soldier_polygon['values'] = lm 
            
    def clear_entry(self):
        self.entry_mtb_name.delete(0, END)
        self.entry_soldier_name.delete(0, END)
        self.cb_soldier_role.delete(0, END)
        self.cb_soldier_polygon.delete(0, END)
        self.list_of_vertices.delete(0,END)
        self.vertices = []

    def take_coords(self, coords):
        self.vertices.append(coords)
        self.list_of_vertices.delete(0,END)
        for idx, vertex in enumerate(self.vertices):
            self.list_of_vertices.insert(idx,vertex)
            
    def add_soldier(self):
        i = self.list_of_vertices.index(ACTIVE)
        
        name = self.entry_soldier_name.get()
        role = self.cb_soldier_role.get()
        polygon = self.cb_soldier_polygon.get()
        location = self.vertices[i]
        add = Soldier(name, polygon, role, location)
        session.add(add)
        
        session.commit()
        self.clear_entry()
        self.refresh()
           
    def delete_soldier(self):
        i = self.lb_list_of_soldier.index(ACTIVE)
        ls =[]
        
        db_soldiers = session.query(Soldier).all()
        for soldier in db_soldiers:
            ls.append(soldier.location)
        db_soldiers = session.query(Soldier).filter(Soldier.location == ls[i])
        for soldier in db_soldiers:
            session.delete(soldier)
        
        session.commit()
        self.refresh()
     
    def modify_soldier1(self):
        i = self.lb_list_of_soldier.index(ACTIVE)
        ls = [] 
        ls1 = []
        ls2 = []
        ls3 = []
        
        db_soldiers = session.query(Soldier).all()
        for soldier in db_soldiers:
            ls.append(soldier.name)
            ls1.append(soldier.role)
            ls2.append(soldier.polygon)
            ls3.append(soldier.location)
        
        self.clear_entry()
        self.entry_soldier_name.insert(0,ls[i])
        self.cb_soldier_role.insert(0,ls1[i])
        self.cb_soldier_polygon.insert(0,ls2[i])
        self.list_of_vertices.insert(0,self.convert_point(ls3[i]))
        self.vertices.append(self.convert_point(ls3[i]))
       
    def modify_soldier2(self):
        ii = self.list_of_vertices.index(ACTIVE)
        i = self.lb_list_of_soldier.index(ACTIVE)
        ls =[]
        
        name = self.entry_soldier_name.get()
        role = self.cb_soldier_role.get()
        polygon = self.cb_soldier_polygon.get()
        location = self.vertices[ii]
        
        db_soldiers = session.query(Soldier).all()
        for soldier in db_soldiers:
            ls.append(soldier.location)
        db_soldiers = session.query(Soldier).filter(Soldier.location == ls[i])
        for soldier2 in db_soldiers:
            soldier2.name = name
            soldier2.role = role
            soldier2.polygon = polygon
            soldier2.location = f'POINT({location[1]} {location[0]})'
        
        session.commit()
        self.clear_entry()
        self.refresh()
  
    def details_of_soldier(self):
        i = self.lb_list_of_soldier.index(ACTIVE)
        ls =[]
        
        db_soldiers = session.query(Soldier).all()
        for soldier in db_soldiers:
            ls.append(soldier.location)
        db_soldiers = session.query(Soldier).filter(Soldier.location == ls[i])
        for soldier in db_soldiers:
            self.lbl_soldier_name_value.config(text=soldier.name)
            self.lbl_soldier_coords_name_value.config(text=self.convert_point(soldier.location))
            self.lbl_soldier_role_name_value.config(text=soldier.polygon)

    def add_mtb(self):
        reverso = [t[::-1] for t in self.vertices]
        
        name = self.entry_mtb_name.get()
        location = Polygon(reverso)
        add = Military_training_ground(name, location)
        session.add(add)
        
        session.commit()
        self.clear_entry()
        self.refresh()
 
    def delete_mtb(self):
        i = self.lb_list_of_mtb.index(ACTIVE)
        lm = []
        
        db_mtb = session.query(Military_training_ground).all()
        for mtb in db_mtb:
            lm.append(mtb.location)
        db_mtb = session.query(Military_training_ground).filter(Military_training_ground.location == lm[i])
        for mtb in db_mtb:
            session.delete(mtb)
        
        session.commit()
        self.refresh()
## WORK DONE TOP 
    def modify_mtb1(self):
        i = self.lb_list_of_mtb.index(ACTIVE)
        lm = []
        lm1 = []
        
        db_mtb = session.query(Military_training_ground).all()
        for mtb in db_mtb:
            lm.append(mtb.name)
            lm1.append(mtb.location)
        
        self.clear_entry()
        self.entry_mtb_name.insert(0,lm[i])
        self.list_of_vertices.insert(0,'old geometry', 'leave or set a new one')
    
    def modify_mtb2(self):
        i = self.lb_list_of_mtb.index(ACTIVE)
        lm = []
        
        name = self.entry_mtb_name.get()
        
        db_mtb = session.query(Military_training_ground).all()
        for mtb in db_mtb:
            lm.append(mtb.location)
        db_mtb = session.query(Military_training_ground).filter(Military_training_ground.location == lm[i])
        for mtb2 in db_mtb:
            mtb2.name = name
            if self.list_of_vertices.size() != 2:
                reverso = [t[::-1] for t in self.vertices]
                location = Polygon(reverso)
                mtb2.location = location
            
        session.commit()    
        self.clear_entry()
        self.refresh()
    
    def create_random_polygon(self):
        number_of_vertices = randint(3,10)
        list_of_vertices = []
        for vertex in range(number_of_vertices):
            vertex = [uniform(49,55), uniform(14, 24)]
            list_of_vertices.append(vertex)
        self.map_widget.set_polygon(list_of_vertices, border_width=2, outline_color='black')
    
    def create_soldier_marker(self):
        i = self.lb_list_of_soldier.index(ACTIVE)
        db_soldiers = session.query(Soldier).all()
        
    
        # x = db_soldiers[i].loc
        # y = db_soldiers[i].loc[1]
        # marker = self.map_widget.set_marker(x, y)
        # print(x)

    def create_random_markers(self):
        number_of_markers = randint(1,34)
        for marker in range(number_of_markers):
            marker = self.map_widget.set_marker(uniform(50,54), uniform(14.5,23.5))
    
    def details_of_mtb(self):
        pass
    
    def start(self):
        self.mainloop()

# if __name__ == "__main__":   
#     log_app = Log()
#     log_app.start()

if __name__ == "__main__":   
    app = App()
    app.start()