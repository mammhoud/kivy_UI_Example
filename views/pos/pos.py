from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import rgba, QueryDict
from kivy.uix.dropdown import DropDown
from kivy.uix.modalview import ModalView
from kivy.clock import Clock, mainthread
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ListProperty,
    ColorProperty,
    NumericProperty,
)
from kivy.metrics import dp, sp
from kivy.lang import Builder
from widgets.popups import ConfirmDialog

from libs.database_Conf import Database
import secrets

Builder.load_file("views/pos/pos.kv")


class Pos(BoxLayout):
    current_total = NumericProperty(0.0)
    current_cart = ListProperty([])

    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.render, 0.1)

    def render(self, _):
        prods = []
        cats = []
        # todo select the data from the database using the implemented method
        for x in range(20):
            prod = {
                "sug2": f"Product #0{x}",
                "sug1": str(x).zfill(8),
                "sug3": secrets.SystemRandom().randint(1, 303),
                "qty": 1,
            }
            prods.append(prod)
        self.ids.ti_search.sugData = prods
        for x in range(20):
            cat = {
                "sug2": f"category #0{x}",
                "sug1": str(x).zfill(8),
                "sug3": secrets.SystemRandom().randint(1, 303),
            }
            cats.append(cat)
        self.ids.ti_search1.sugData = cats

    """
    def delete_from_view(self, ConfirmDialog):
        if self.currentUser:
            self.currentUser.parent.remove_widget(self.currentUser)
            data = Database()
            print(self.currentUser)
            data.delete_data('user', where_clause=f"WHERE username = '{self.currentUser.username}'" )
            
    def delete_product(self, user):
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
            
            """

    def qty_control(self, tile, increasing=False):
        _qty = int(tile.qty)
        if increasing:
            _qty += 1
        else:
            _qty -= 1
            if _qty <= 0:
                _qty = 0
                # todo => {ask} delete or not delete if the minus clicked

        data = {
            "name": tile.name,
            "pro_code": tile.pro_code,
            "price": tile.price,
            "qty": 1,
        }
        _id = tile.pro_code
        tgt = None
        tmp = list(self.current_cart)
        for i, x in enumerate(tmp):
            if x["pro_code"] == _id:
                tgt = i
                break
        data["qty"] = _qty
        data["price"] = data["price"]
        self.current_cart.pop(i)
        self.current_cart.insert(i, data)
        # tile.qty = _qty

    def add_cat(self, inst):
        data = {"cat_name": inst.sug2, "cat_id": inst.sug1, "cat_des": inst.sug3}

    def add_product(self, inst):
        data = {"name": inst.sug2, "pro_code": inst.sug1, "price": inst.sug3, "qty": 1}
        tmp = list(filter(lambda x: x["pro_code"] == inst.sug1, self.current_cart))

        if len(tmp) > 0:
            # update qty
            grid = self.ids.g1_products
            tgt = None
            for c in grid.children:
                if c.pro_code == tmp[0]["pro_code"]:
                    tgt = c
                    break
            if tgt:
                self.qty_control(tgt, increasing=True)

        else:
            self.current_cart.append(data)
        # self.current_total += round(float(data["price"]),2)

    def update_total(self):
        prods = self.ids.g1_receipt.children
        _total = 0
        for c in prods:
            _total += round(float(c.price) * int(c.qty), 2)

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
        pt.pro_code = product.get("pro_code", "")
        pt.name = product.get("name", "")
        pt.price = product.get("price", 0)
        pt.qty = product.get("qty", 0)
        pt.qty_callback = self.qty_control

        grid.add_widget(pt)

    def checkout(self):
        pc = ConfirmDialog()
        pc.title = "Check out"
        pc.subtitle = "are you sure to confirm"
        pc.textConfirm = "yes, confirm"
        pc.textCancel = "Cancel"
        pc.confirmColor = App.get_running_app().color_tertiary
        pc.cancelColor = App.get_running_app().color_primary
        pc.confirmCallback = self.checkout_callback
        pc.open()

    def clear_cart(self):
        self.current_cart = []

    def checkout_callback(self, posview):
        self.clear_cart()
        self.ids.ti_search.text = ""
        self.ids.ti_search.close_dropdowns()

    def add_receipt_item(self, item: dict) -> None:
        rc = ReceiptItem()
        rc.name = item["name"]
        rc.qty = item["qty"]
        rc.price = item["price"]

        self.ids.g1_receipt.add_widget(rc)


class ProductTile(BoxLayout):
    pro_code = NumericProperty(0)
    name = StringProperty("")
    qty = NumericProperty(0)
    price = NumericProperty(0)
    qty_callback = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 0.1)

    def render(self, _):
        pass


class ReceiptItem(BoxLayout):
    pro_code = NumericProperty(0)
    name = StringProperty("")
    qty = NumericProperty(0)
    price = NumericProperty(0)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 0.1)

    def render(self, _):
        pass
