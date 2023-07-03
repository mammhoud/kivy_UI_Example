from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import rgba, QueryDict
from kivy.uix.dropdown import DropDown
from kivy.uix.modalview import ModalView
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty,ObjectProperty, ListProperty, ColorProperty, NumericProperty
from kivy.metrics import dp, sp
from kivy.lang import Builder
from random import randint

Builder.load_file("views/pos/pos.kv")
class Pos(BoxLayout):
    current_total = NumericProperty(0.0)
    current_cart = ListProperty([])
    def __init__(self, **kw):
    
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        prods = []
        
        for x in range(100):
            prod= { 
                   "name": f"Product #0{x}",
                   "pcode": str(x).zfill(8),
                   "price": randint(30000, 300000),
                   "qty": 1}
            prods.append(prod)
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
        for i, x in enumerate(tmp):
            if x["pcode"] == _id:
                tgt = i
                break
                
           
        data["qty"] = _qty
        data["price"] = (data["price"])
        self.current_cart.pop(i)
        self.current_cart.insert(i, data)
        #tile.qty = _qty
    
    
    
    
    def add_product(self,inst):
        data = { 
                "name": inst.name,
                "pcode": inst.pcode,
                "price": inst.price,
                "qty": 1}
        tmp = list(filter(lambda x: x["pcode"]==inst.pcode, self.current_cart))
       
        if len(tmp)>0:
            #update qty 
            grid = self.ids.g1_products
            tgt = None
            for c in grid.children:
                if c.pcode == tmp[0]['pcode']:
                    tgt = c
                    break
            if tgt:
                self.qty_control(tgt,increasing=True)

        else:
            self.current_cart.append(data)
        #self.current_total += round(float(data["price"]),2)
        
    def update_total(self):
        prods = self.ids.g1_receipt.children
        _total = 0
        for c in prods:
            _total += round(float(c.price)* int(c.qty),2)
            
        self.current_total = _total
    def on_current_cart(self, inst, cart):
        
        self.ids.g1_receipt.clear_widgets()
        self.ids.g1_products.clear_widgets()
        
        for f in cart:
            self._add_product(f)
            self.add_receipt_item(f)
        self.update_total()
            
            
    def _add_product(self, product: dict): 
       grid = self.ids.g1_products
       
       pt = ProductTile()
       pt.pcode = product.get("pcode", "")
       pt.name = product.get("name", "")
       pt.price = product.get("price", 0)
       pt.qty = product.get("qty", 0)
       pt.qty_callback = self.qty_control
       
       grid.add_widget(pt)
    def checkout(self):
        pc = PosCheckout()
        pc.callback = self.checkout_callback
        pc.open()
    def clear_cart(self):
        self.current_cart= []
        
    
    def checkout_callback(self, posview):
        self.clear_cart()
        self.ids.ti_search.text= ""
        self.ids.ti_search.close_dropdowns()

    def add_receipt_item(self, item:dict) -> None:
        rc = ReceiptItem()
        rc.name = item["name"]
        rc.qty = item["qty"]
        rc.price = item["price"]
        
        self.ids.g1_receipt.add_widget(rc)

       
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
    

class ReceiptItem(BoxLayout):
    pcode = StringProperty("")
    name = StringProperty("")
    qty = NumericProperty(0)    
    price = NumericProperty(0)
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, .1)
    def render(self, _):
        pass 
    
class PosCheckout(ModalView):
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
            