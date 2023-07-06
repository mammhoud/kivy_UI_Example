
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ListProperty, ColorProperty, NumericProperty, ObjectProperty
from threading import Thread
from _files.dataBase import Database

Builder.load_file("views/users/users.kv")
class Users(BoxLayout):
    users = []
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        t1 = Thread(target= self.get_users, daemon= True)
        t1.start()
        
    def get_users(self):
        data = Database()
        users = data.select_data("user", fetchall= True)
        '''        
        users = [
            {
                1: "firstName",
                2: "lastName",
                3: "userName",
                3: "*******",
                4: "createdAt",#####
                5:"signedIn",#####
                6:"role",
                7: "Email"
            },    
            ]'''
        self.set_users(users)
        
    @mainthread
    def set_users(self, users:list):
        self.ids.g1_users.clear_widgets()
        print(users)
        for u in users:
            ut = UserTile()
            ut.firstName = u[1]
            ut.lastName = u[2]
            ut.username = u[3]
            ut.password = u[4]
            ut.roles = u[5]
            ut.email = u[6]
            
            self.ids.g1_users.add_widget(ut)


        
    def add_new(self):
        md = ModUser()
        md.open()
    
class UserTile(BoxLayout):
    firstName = StringProperty("")
    lastName = StringProperty("")
    username = StringProperty("")
    password = StringProperty("")
    createdAt = StringProperty("")
    signedIn = StringProperty("")
    roles = StringProperty("")
    email = StringProperty("")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass