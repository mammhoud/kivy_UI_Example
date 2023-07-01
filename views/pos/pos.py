from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import rgba, QueryDict
from kivy.uix.dropdown import DropDown

from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty,ObjectProperty, ListProperty, ColorProperty, NumericProperty
from kivy.metrics import dp, sp
from kivy.lang import Builder
from random import randint

Builder.load_file('views/pos/pos.kv')
class Pos(BoxLayout):
    current_total = NumericProperty(0.0)
    current_cart = ListProperty([])
    def __init__(self, **kwargs):
        
        #Clock.schedule_once(self.render, .6)
        super().__init__(**kwargs)
        
    def render(self, _):
        prods = []
        
        for x in range(6):
            prod= { 
                   'name': f"Product #0",
                   'pcode': str(x).zfill(8),
                   'price': randint(2, 25),
                   'qty': 1}
            prods.append(prod)
            print(prods)
            print(self.ids.ti_search.products)
        self.ids.ti_search.products = prods
        
        
    def qty_control(self, tile, increasing=False):
        _qty = int(tile.qty)
        if increasing:
            _qty += 1
        else:
            _qty -= 1
            if _qty < 0: 
                # to:do => {ask} delete or not delete if the minus clicked
                _qty = 0
        data = { 
        "name": tile.name,
        "pcode": tile.pcode,
        "price": tile.price,
        "qty": 1
        }
         
        _id = tile.pcode
        tgt = None
        tmp = list(self.current_cart)
        for i,x in enumerate(tmp):
            if x['pcode'] == _id:
                tgt = i
                break
                
           
        data['qty'] = _qty
        data['price'] = (data['price']* _qty)
        self.current_cart.pop(i)
        self.current_cart.insert(i,data)
        #tile.qty = _qty
    
    
    
    
    def add_product(self,inst):
        data = { 
                "name": inst.name,
                "pcode": inst.pcode,
                "price": inst.price,
                "qty": 1}
        tmp = list(filter(lambda x: ['pcode']==inst.pcode, self.current_cart))
        if len(tmp)>0:
            #update qty 
            self.qty_control(inst,increasing=True)
        else:
            self.surrent_cart.append(data)
        #self.current_total += round(float(data['price']),2)
        
        self.current_cart.append(data)
    def update_total(self):
        prods = self.ids.g1_receipt.children
        _total = 0
        for c in prods:
            _total += round(float(c.price),2)
        self.current_total = _total
    def on_current_cart(self, inst, cart):
        self.ids.g1_receipt.clear_widgets()
        self.ids.g1_products.clear_widgets()
        
        for f in cart:
            self.add_product(f)
            self.add_receipt_item(f)
        self.update_total()
            
            
    def _add_product(self, product: dict): 
       grid = self.ids.g1_products
       pt = ProductTile()
       pt.pcode = product.get('pcode', "")
       pt.name = product.get("name", "")
       pt.price = product.get("price", 0)
       pt.qty = product.get("qty", 0)
       pt.qty_callback = self.qty_control
       
       grid.add_widget(pt)
       
    def add_receipt_item(self, item:dict):
        rc = ReceiptItem()
        rc.name = item['name']
        rc.qty = item['qty']
        rc.price = item['price']
        
        self.ids.g1_receipt.add_widget(rc)

       
class ProductTile(BoxLayout):
    pcode = StringProperty("")
    name = StringProperty("")
    qty = NumericProperty(0)    
    price = NumericProperty(0)
    qty_callback = ObjectProperty(allownone=True)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Clock.schedule_once(self.render, .1)
        
    def render(self, _):
        pass 
    
    
class ReceiptItem(BoxLayout):
    pcode = StringProperty("")
    name = StringProperty("")
    qty = NumericProperty(0)    
    price = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Clock.schedule_once(self.render, .1)
        
    def render(self, _):
        pass 
    
    
