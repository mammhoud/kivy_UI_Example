
BoxLayout:
    BoxLayout:
        TextInput:
            id: username
    BoxLayout:
        TextInput:
            id: password
    Button:
        on_press: app.check_login(username.text, password.text)

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class LoginScreen(BoxLayout):
    def check_login(self, username, password):
        if result:
            # show a success popup
            popup = Popup(title='Success', content=Label(text='You have logged in!'), size_hint=(None, None), size=(300, 200))
            popup.open()
        else:
            # show an error popup
            popup = Popup(title='Error', content=Label(text='Invalid username or password!'), size_hint=(None, None), size=(300, 200))
            popup.open()


class LoginApp(App):
    def build(self):
        # load the kv file
        self.load_kv('login.kv')
        
        # return an instance of LoginScreen
        return LoginScreen()
