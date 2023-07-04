
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ListProperty, ColorProperty, NumericProperty, ObjectProperty
from threading import Thread

Builder.load_file("views/users/users.kv")


class Users(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        t1 = Thread(target= self.get_users, daemon= True)
        t1.start()
        
    def get_users(self):
        users = [
            {
                "firstName": "fist",
                "lastName": "last",
                "username": "user",
                "password": "123",
                "createdAt": "",
                "signedIn":"",
                "roles":"admin",
                "email": "mail@mail.com"
            },
            {
                "firstName": "fist1",
                "lastName": "last1",
                "username": "user1",
                "password": "123",
                "createdAt": "",
                "signedIn":"",
                "roles":"admin",
                "email": "mail@mail.com"
         
            },{
                "firstName": "fist2",
                "lastName": "last2",
                "username": "user2",
                "password": "123",
                "createdAt": "",
                "signedIn":"",
                "roles":"admin",
                "email": "mail@mail.com"
            },
        ]
        self.set_users(users)
        
    @mainthread
    def set_users(self, users:list):
        grid = self.ids.g1_users
        grid.clear_widgets()
        
        for u in users:
            ut = UserTile()
            ut.firstName = u["firstName"]
            ut.lastName = u["lastName"]
            ut.usename = u["username"]
            ut.password = u["password"]
            ut.createdAt = u["createdAt"]
            ut.signedIn = u["signedIn"]
            ut.roles = u["roles"]
            ut.email = u["email"]
            grid.add_widget(ut)


        
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
