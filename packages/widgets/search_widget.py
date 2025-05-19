from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.clock import Clock, mainthread
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.properties import ColorProperty, ListProperty, ObjectProperty, StringProperty,NumericProperty
from kivy.core.window import Window
from kivy.metrics import dp, sp
from random import randint
from widgets.textfields import FlatField

Builder.load_string("""
<SuggestionWidget>:    
    BackBox:
    	bcolor: app.color_secondary_text
        canvas.before:
            Color: 
                rgba: app.color_tertiary
            Rectangle:
                pos: self.pos
                size: [self.size[0], dp(2)]
        Image: 
            source: 'assets/imgs/back.png' #todo add the image secuance for the app/products
            height: dp(24)
            size_hint_x: None
            width: self.height
            halign: "left"
            valign: "middle"	
            anchor_x: "center"
        BoxLayout:
            height: self.height
            canvas.after:
                Color: 
                    rgba: app.color_tertiary
                Rectangle:
                    pos: self.pos
                    size: [self.size[0], dp(2)]
            BackBox:
                size_hint_y: None
                height: dp(48)
                spacing: dp(4)
                padding: [dp(12),dp(2)]
                bcolor: app.color_primary
                canvas.before:
                    Color: 
                        rgba: app.color_tertiary
                    Rectangle:
                        pos: self.pos
                        size: [self.size[0], dp(2)]
                Text:
                    text: str(int(root.sug1)) #catched error !
                    color: app.color_primary_text
                    font_size: app.fonts.size.h4
                    font_name: app.fonts.body
                    size_hint_x: .3
                Text:
                    text: str(root.sug2)
                    color: app.color_primary_text
                    font_size: app.fonts.size.h4
                    font_name: app.fonts.body
                    size_hint_x: .3
                Text:
                    text: "$%s"%str(round(root.sug3,2))
                    color: app.color_primary_text
                    font_size: app.fonts.size.h4
                    font_name: app.fonts.body
                    size_hint_x: .2       
""")     
class SuggestionWidget(ButtonBehavior, BoxLayout):
    sug1= NumericProperty(0)
    sug2= StringProperty("")
    sug3= NumericProperty(0)
class SearchBar(FlatField):
    choices = ListProperty([])
    sugData = ListProperty([])
    suggestion_widget= ObjectProperty(allownone=True)
    callback= ObjectProperty(alownone=True)
    def __init__(self, **kw):
        super().__init__(**kw)
        self.multiline= False
        self.dropdown=None
    def on_text(self, inst, text):
        try:
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
                
            self.show_suggestions(text)
            
        except Exception as e:
            print(e,'on_text method')
        
    def keyboard_on_key_down(self, window,kc, text, modifiers):
        try:
        # if len(self.text) == 1 or not text:
            if self.dropdown:
                self.dropdown.dismiss()
                self.dropdown = None
            
            super().keyboard_on_key_down(window,kc,text,modifiers)
        except Exception as e:
            print(e+ "keyboard_on_key_down method")
    
    
    def show_suggestions(self, suggestion):
            try:
                suggestions = self.sugData
                self.choices.clear()####
                self.choices= suggestions
            except Exception as e:
                print(e+ "show_suggestions")
    
    def on_choices(self, inst, choices):
        try: 
            # get the suggestions 
            self.dropdown = DropDown()
            self.dropdown.autowidth= False
            self.dropdown.size_hint_x = None
            self.dropdown.width = Window.width*.4

            x:int = 0
            for c in self.choices:
                b= SuggestionWidget()
                b.sug1= c['sug1']
                b.sug2 = c['sug2']
                b.sug3= c['sug3']
                
                b.size_hint_y = None
                b.height = dp(54)
                b.width= self.width
                b.bind(on_release= self.suggest)
                
                self.dropdown.add_widget(b)
                x+= 1
            if x> 0:
                self.dropdown.open(self)
        except Exception as e:
            print(e,"on_choices method")
            
    def suggest(self,inst):
        if self.callback:
            self.callback(inst)
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None
    
    def close_dropdowns(self):
        if self.dropdown:
            self.dropdown.dismiss()
            self.dropdown = None             
    def open_dropdown(self, *args):
        if self.dropdown:
            self.dropdown.open(self)

