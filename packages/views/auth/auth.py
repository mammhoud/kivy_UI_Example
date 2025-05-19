from kivy.app import App

# from utils.database_Conf import Database
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ListProperty,
    ColorProperty,
    NumericProperty,
)
from kivy.clock import Clock, mainthread

from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout

Builder.load_file("views/auth/auth.kv")


class AuthSign(ModalView):
    callback = ObjectProperty(allownone=True)
    username = ""
    name = ""

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, 0.1)

    def render(self, _):
        pass

    def complete(self):
        # todo: save a log into database of doc file
        App.get_running_app().root.ids.scrn_mngr.current = "scrn_home"

        self.dismiss()  # close
        if self.callback:
            print(self.username, "--------> first")
            self.callback(self)
            # todo pass any user data into json to forms or to the base files


class Auth(BoxLayout):
    userdata = ListProperty([])  # todo check if there any data duplication

    ##############################
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def signlogs_callback(self, row):
        print(
            self.username, "--------> second loading"
        )  # todo pass the values of user data

    def signlogs(self):
        pc = AuthSign()
        pc.callback = self.signlogs_callback
        pc.open()

    def authenticate(self, username=None, password=None):
        self.username = username
        self.password = password
        # self.ids.login_button.bind(on_press=self.login())

        print(username, "--------> username Loging")
        # print(password,"--------> password")
        # Connect to the SQLite database file
        db = Database()

        row = db.select_data(
            table_name="user",
            where_clause=f"WHERE username = '{username}' AND password = '{password}'",
            fetchall=False,
        )
        db.close_connection()
        # Query the database for matching username and password

        # Check if there is a matching row
        if row is not None:
            # Display a welcome message with the user's name
            print(row, ">>>>>>>>>>>>>>> User Row")
            self.signlogs()
        else:
            pass  ######### todo  override the label of the small window to ooptimize ux
