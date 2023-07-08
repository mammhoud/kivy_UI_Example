



from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
import hashlib
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ListProperty, ColorProperty, NumericProperty, ObjectProperty
from threading import Thread
from libs.dataBase import Database
from datetime import datetime

Builder.load_string("""
<ConfirmDialog>:
	background: ""
	background_color: [0,0,0,.21]
	BackBox:
		orientation: "vertical"
		spacing: dp(12)
		padding: dp(14)
		bcolor: app.color_primary_bg
		radius: [self.height*.08]
		size_hint: [None, .7]
		width: self.height
		BoxLayout:
			size_hint_y: .6
			orientation: 'vertical'
			Text:
				text: root.title
				font_name: app.fonts.styled
				font_size: app.fonts.size.extra
				color:app.color_primary_text
				halign: 'center'
			Text:
				text: root.subtitle
				halign: 'center'
				font_size: app.fonts.size.h2
				color:app.color_primary_text
		AnchorLayout:
			BoxLayout:
				size_hint_y: .4
				spacing: dp(12)
				size_hint_y: .6
				height: dp(128)
				FlatButton:
					text: root.textCancel
					font_size: app.fonts.size.h2
					color: root.cancelColor
					bcolor: app.color_secondary_bg
                    on_release: root.cancel()
					#size_hint_y: None
				RoundedButton:
					text: root.textConfirm
					font_size: app.fonts.size.h2
					bcolor: app.color_primary
					color: root.confirmColor
					radius: [self.height*.1]
					on_release: root.complete()
				#Divider:
""")






class ConfirmDialog(ModalView):
    callback = ObjectProperty(allownone= True)
    title = StringProperty("")
    subtitle = StringProperty("")
    textConfirm = StringProperty("")
    textCancel = StringProperty("")
    confirmCallback = ObjectProperty(allownone= True)
    cancelCallback = ObjectProperty(allownone= True)
    confirmColor= ColorProperty([1,1,1,1])
    cancelColor=ColorProperty([1,1,1,1])
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)
    def render(self, _):
        pass
    def cancel(self):
        self.dismiss()
        if self.cancelCallback:
            self.cancelCallback(self)
            
    def complete(self):
        self.dismiss()
        if self.confirmCallback:
            self.confirmCallback(self)
            
