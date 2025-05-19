from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.modalview import ModalView
import hashlib
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
from threading import Thread

from utils.database_Conf import Database
from datetime import datetime
from widgets.popups import ConfirmDialog

Builder.load_file("views/stocks/stocks.kv")


class Stocks(BoxLayout):
    callback = ObjectProperty(allownone=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 0.1)
        self.currentProduct = None
        self.modifyProduct = None

    def render(self, _):
        t1 = Thread(target=self.get_stocks, daemon=True)
        t1.start()

    def get_stocks(self):
        """stocks = [
        {
            1: "productName",
            2: "productCode",
            3: "productName",
            4: "*******",
            5: "productInStock",#####
            6: "productDiscount",#####
            7: "role",
            8: "Email"
        },
        ]"""
        data = Database()

        self.set_stocks(data.select_data("stock", fetchall=True))

    def add_stocks(self, mv):
        _now = datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M")

        stock = [
            mv.ids.productName_input.text.strip(),
            mv.ids.productCode_input.text.strip(),
            mv.ids.productName_input.text.strip(),
            mv.ids.email_input.text.strip(),
            upass,
            _now,
            _now,
            mv.ids.role_input.text.strip(),
        ]
        data = Database()

        data.insert_data("stock", stock)
        self.get_stocks()

    def delete_from_view(self, ConfirmDialog):
        if self.currentProduct:
            self.currentProduct.parent.remove_widget(self.currentProduct)
            data = Database()
            print(self.currentProduct)
            data.delete_data(
                "stock",
                where_clause=f"WHERE productName = '{self.currentProduct.productName}'",
            )

    def delete_stock(self, stock):
        self.currentProduct = stock
        dc = ConfirmDialog()
        try:
            dc.title = f"Delete Stock: {stock.productName}"
        except Exception as e:
            print(e)
        finally:
            print(stock)
            dc.subtitle = "are you sure to Delete"
            dc.textConfirm = "yes, Delete"
            dc.textCancel = "Cancel"
            dc.confirmColor = App.get_running_app().color_tertiary
            dc.cancelColor = App.get_running_app().color_primary
            dc.confirmCallback = self.delete_from_view
            dc.open()

    def update_stock(self, stock):
        self.modifyProduct = stock
        mv = ModStock()
        mv.productName = stock.productName
        mv.productCode = stock.productCode
        mv.productName = stock.productName
        mv.email = stock.email
        mv.callback = self.set_update

        mv.open()

    def set_update(self, mv):
        pwd = mv.ids.productCategory_input.text
        if len(mv.ids.productName_input.text.strip()) < 3:
            return
        _pwd = pwd.strip()
        upass = hashlib.sha256(_pwd.encode()).hexdigest()
        now = datetime.now()
        _now = datetime.strftime(now, "%Y/%m/%d %H:%M")

        stock = [
            mv.ids.productName_input.text.strip(),
            mv.ids.productCode_input.text.strip(),
            mv.ids.productName_input.text.strip(),
            mv.ids.email_input.text.strip(),
            upass,
            _now,
            _now,
            mv.ids.role_input.text.strip(),
        ]

        for i, a in enumerate(stock):
            if a == None:
                stock[i] = "None"
        data = Database()
        data.update_data(
            "stock",
            stock,
            where_clause=f"WHERE productName = '{self.modifyProduct.productName}'",
        )
        self.get_stocks()

    @mainthread
    def set_stocks(self, stocks: list):
        self.ids.g1_stocks.clear_widgets()
        for u in stocks:
            u = list(u)
            ut = StockTile()
            ut.productName = u[1]
            ut.productCode = u[2]
            ut.productName = u[3]
            ut.email = u[4]
            ut.productCategory = u[5]
            ut.productInStock = u[6]
            ut.productDiscount = u[7]
            ut.roles = u[8]
            ut.callback = self.delete_stock
            ut.bind(on_release=self.update_stock)
            self.ids.g1_stocks.add_widget(ut)

    def add_new(self):
        md = ModStock()
        md.callback = self.add_stocks
        md.open()


class ModStock(ModalView):
    callback = ObjectProperty(allownone=True)
    productName = StringProperty("")
    productCode = StringProperty("")
    productName = StringProperty("")
    productCategory = StringProperty("")
    productInStock = StringProperty("")
    productDiscount = StringProperty("")
    roles = StringProperty("")
    email = StringProperty("")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 0.1)

    def render(self, _):
        pass

    def on_productName(self, inst, productName):
        self.ids.productName_input.text = productName
        self.ids.subtitle.text = "Enter your Details below"
        self.ids.btn_confirm.text = "Update Stock"
        self.ids.title.text = "update Stock"

    def on_productCode(self, inst, productCode):
        self.ids.productCode_input.text = productCode

    def on_productName(self, inst, productName):
        self.ids.productName_input.text = productName

    def on_email(self, inst, email):
        self.ids.email_input.text = email


class StockTile(ButtonBehavior, BoxLayout):
    productName = StringProperty("")
    productCode = StringProperty("")
    productPrice = StringProperty("")
    productCategory = StringProperty("")
    productInStock = StringProperty("")
    productDiscount = StringProperty("")
    roles = StringProperty("")
    email = StringProperty("")
    callback = ObjectProperty(allownone=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 0.1)

    def delete_Product(self):
        if self.callback:
            self.callback(self)

    def render(self, _):
        pass
