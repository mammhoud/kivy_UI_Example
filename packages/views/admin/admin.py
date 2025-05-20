from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
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


Builder.load_file("views/admin/admin.kv")


class Admin(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
