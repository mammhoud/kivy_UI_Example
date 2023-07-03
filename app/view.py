
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class MainWindow(BoxLayout):
    username = StringProperty('user ---')
    role = StringProperty('admin ---')
    def __init__(self, **kw):
        super().__init__(**kw)