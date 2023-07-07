
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ListProperty, ColorProperty, NumericProperty, ObjectProperty
from threading import Thread
from _files.dataBase import Database

Builder.load_file("views/users/users.kv")
class Users(BoxLayout):

    callback = ObjectProperty(allownone=True)
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)


    def render(self, _):
        t1 = Thread(target= self.get_users, daemon= True)
        t1.start()
        
    def get_users(self):
        data = Database()
        '''        users = [
            {
                1: "firstName",
                2: "lastName",
                3: "username",
                4: "*******",
                5: "createdAt",#####
                6: "signedIn",#####
                7: "role",
                8: "Email"
            },    
            ]'''
        self.set_users(data.select_data("user", fetchall= True))
    
    def add_users(self,mv):
        firstName = mv.ids.firstName
        lastName = mv.ids.lastName
        username = mv.ids.username
        pwd = mv.ids.pwd
        cpwd = mv.ids.cpwd
        
        if len(firstName.text.strip()) < 3:
            return
        _pwd = pwd.text.strip()
        upass = hashlib.sha256(_pwd.encode()).hexdigest()
        now = datetime.now()
        _now = datetime.strftime(now, "%Y/%m/%d %H:%M")
        
        user = {
                "firstName": firstName.text.strip(),
                "lastName": lastName.text.strip(),
                "username": username.text.strip(),
                "password": upass,
                "createdAt": _now,
                "signedIn": _now,
            },  
        self.set_users([user])
    
    def update_user(self, user):
        mv = ModUser()
        mv.firstName = user.firstName
        mv.lastName = user.lastName
        mv.username = user.username
        mv.callback = self.set_update
        mv.open()
    def set_update(self, mv):
        print("update")
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
            ut.createdAt = u[5]
            ut.signedIn = u[6]
            ut.roles = u[7]
            ut.email = u[8]
            ut.bind(on_release= self.update_user)
            self.ids.g1_users.add_widget(ut)


        
    def add_new(self):
        md = ModUser()
        md.open()
    

class DeleteConfirm(ModalView):
    callback = ObjectProperty(allownone= True)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)
    def render(self, _):
        prods = []
    def complete(self):
        # to-do: print the receipt and make a record in database for the orderd item and isigtes
        self.dismiss()
        if self.callback:
            self.callback(self)
            
class ModUser(ModalView):
    callback = ObjectProperty(allownone=True)
    firstName = StringProperty("")
    lastName = StringProperty("")
    username = StringProperty("")
    createdAt = StringProperty("")
    roles = StringProperty("")
    email = StringProperty("")
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass
    def on_first_name(self, inst, fname):
        self.ids.firstName.text = firstName
        self.ids.subtitle = "Enter your Details below"
        self.ids.btn_confirm.text = "Update User"
        self.ids.title = "update User"

    def on_last_name(self, inst, lname):
        self.ids.lname.text = lastname
    def on_username(self, inst, username):
        self.ids.user.text = username
    
    
    def delete_user(self, user):
        dc = DeleteConfirm()
        dc.open()
class UserTile(ButtonBehavior, BoxLayout):
    firstName = StringProperty("")
    lastName = StringProperty("")
    username = StringProperty("")
    password = StringProperty("")
    createdAt = StringProperty("")
    signedIn = StringProperty("")
    roles = StringProperty("")
    email = StringProperty("")
    callback = ObjectProperty(allownone=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        pass