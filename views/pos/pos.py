from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import rgba, QueryDict
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty,ObjectProperty, ListProperty, ColorProperty, NumericProperty
from kivy.metrics import dp, sp
from kivy.lang import Builder
from random import randint

Builder.load_file('views/pos/pos.kv')
class Pos(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)
        
    def render(self, _):
        for x in range(3):
            pcode = randint(1000000,7000000)
            prod= {
                
                "name": f"product {x}",
                "qty": 7,
                "price": 200.23,
                "pcode": str(pcode)
            } 
            self.add_product(prod)
       
    def qty_control(self, tile, increasing=False):
        _qty = int(tile.qty)
        if increasing:
            _qty += 1
        else:
            _qty -= 1
            if _qty < 0: 
                # to:do => {ask} delete or not delete if the minus clicked
                _qty = 0
        tile.qty = _qty
    
    def add_product(self, product: dict): 
       grid = self.ids.g1_products
       pt = ProductTile()
       pt.pcode = product.get('pcode', "123")
       pt.name = product.get("name", "test")
       pt.price = product.get("price", 0)
       pt.qty = product.get("qty", 0)
       pt.qty_callback = self.qty_control
       grid.add_widget(pt)
       
class ProductTile(BoxLayout):
    pcode = StringProperty("")
    name = StringProperty("")
    qty = NumericProperty(0)    
    price = NumericProperty(0)
    qty_callback = ObjectProperty(allownone=True)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)
        
    def render(self, _):
        pass 
    
    
