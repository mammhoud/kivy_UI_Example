from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
import hashlib
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.clock import Clock, mainthread
from kivy.properties import (
    StringProperty,
    ListProperty,
    ColorProperty,
    NumericProperty,
    ObjectProperty,
)
from threading import Thread

from utils.database_Conf import Database
from datetime import datetime
from widgets.popups import ConfirmDialog

Builder.load_file("views/users/users.kv")


class Users(BoxLayout):
    callback = ObjectProperty(allownone=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 0.1)
        self.currentUser = None
        self.modifyUser = None

    def render(self, _):
        t1 = Thread(target=self.get_users, daemon=True)
        t1.start()

    def get_users(self):
        """users = [
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
        ]"""
        data = Database()

        self.set_users(data.select_data("user", fetchall=True))

    def add_users(self, mv):
        # cpwd = mv.ids.cpwd

        if len(mv.ids.firstName_input.text.strip()) < 3:
            return
        upass = hashlib.sha256(mv.ids.password_input.text.strip().encode()).hexdigest()
        _now = datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M")

        user = [
            mv.ids.firstName_input.text.strip(),
            mv.ids.lastName_input.text.strip(),
            mv.ids.username_input.text.strip(),
            mv.ids.email_input.text.strip(),
            upass,
            _now,
            _now,
            mv.ids.role_input.text.strip(),
        ]
        data = Database()

        data.insert_data("user", user)
        self.get_users()

    def delete_from_view(self, ConfirmDialog):
        if self.currentUser:
            self.currentUser.parent.remove_widget(self.currentUser)
            data = Database()
            print(self.currentUser)
            data.delete_data(
                "user", where_clause=f"WHERE username = '{self.currentUser.username}'"
            )

    def delete_user(self, user):
        self.currentUser = user
        dc = ConfirmDialog()
        try:
            dc.title = f"Delete User: {user.username}"
        except Exception as e:
            print(e)
        finally:
            print(user)
            dc.subtitle = "are you sure to Delete"
            dc.textConfirm = "yes, Delete"
            dc.textCancel = "Cancel"
            dc.confirmColor = App.get_running_app().color_tertiary
            dc.cancelColor = App.get_running_app().color_primary
            dc.confirmCallback = self.delete_from_view
            dc.open()

    def update_user(self, user):
        self.modifyUser = user
        mv = ModUser()
        mv.firstName = user.firstName
        mv.lastName = user.lastName
        mv.username = user.username
        mv.email = user.email
        mv.callback = self.set_update

        mv.open()

    def set_update(self, mv):
        pwd = mv.ids.password_input.text
        # cpwd = mv.ids.cpwd
        if len(mv.ids.firstName_input.text.strip()) < 3:
            return
        _pwd = pwd.strip()
        upass = hashlib.sha256(_pwd.encode()).hexdigest()
        now = datetime.now()
        _now = datetime.strftime(now, "%Y/%m/%d %H:%M")

        user = [
            mv.ids.firstName_input.text.strip(),
            mv.ids.lastName_input.text.strip(),
            mv.ids.username_input.text.strip(),
            mv.ids.email_input.text.strip(),
            upass,
            _now,
            _now,
            mv.ids.role_input.text.strip(),
        ]

        for i, a in enumerate(user):
            if a == None:
                user[i] = "None"
        data = Database()
        data.update_data(
            "user", user, where_clause=f"WHERE username = '{self.modifyUser.username}'"
        )
        self.get_users()

    @mainthread
    def set_users(self, users: list):
        self.ids.g1_users.clear_widgets()
        for u in users:
            u = list(u)
            ut = UserTile()
            ut.firstName = u[1]
            ut.lastName = u[2]
            ut.username = u[3]
            ut.email = u[4]
            ut.password = u[5]
            ut.createdAt = u[6]
            ut.signedIn = u[7]
            ut.roles = u[8]
            ut.callback = self.delete_user
            ut.bind(on_release=self.update_user)
            self.ids.g1_users.add_widget(ut)

    def add_new(self):
        md = ModUser()
        md.callback = self.add_users
        md.open()


class ModUser(ModalView):
    callback = ObjectProperty(allownone=True)
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
        Clock.schedule_once(self.render, 0.1)

    def render(self, _):
        pass

    def on_firstName(self, inst, firstName):
        self.ids.firstName_input.text = firstName
        self.ids.subtitle.text = "Enter your Details below"
        self.ids.btn_confirm.text = "Update User"
        self.ids.title.text = "update User"

    def on_lastName(self, inst, lastName):
        self.ids.lastName_input.text = lastName

    def on_username(self, inst, username):
        self.ids.username_input.text = username

    def on_email(self, inst, email):
        self.ids.email_input.text = email


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
        Clock.schedule_once(self.render, 0.1)

    def delete_user(self):
        if self.callback:
            self.callback(self)

    def render(self, _):
        pass
