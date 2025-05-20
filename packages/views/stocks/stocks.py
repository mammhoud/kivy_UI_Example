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
from db.models import Product, Category
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
        data = Product.objects.all()
        self.set_stocks(data)

    def add_stocks(self, mv):
        Product.objects.create(
            name=mv.ids.name_input.text.strip(),
            category=Category.objects.filter(
                name=mv.ids.category_input.text.strip()
            ).first(),
            description=mv.ids.description_input.text.strip(),
            price=float(mv.ids.price_input.text.strip()),
            quantity_in_stock=int(mv.ids.quantity_input.text.strip()),
            brand=mv.ids.brand_input.text.strip(),
            image=mv.ids.image_input.text.strip(),
        )
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
        p = Product.objects.get(id=self.modifyProduct.product_id)
        p.name = mv.ids.name_input.text.strip()
        p.category = Category.objects.filter(
            name=mv.ids.category_input.text.strip()
        ).first()
        p.description = mv.ids.description_input.text.strip()
        p.price = float(mv.ids.price_input.text.strip())
        p.quantity_in_stock = int(mv.ids.quantity_input.text.strip())
        p.brand = mv.ids.brand_input.text.strip()
        p.image = mv.ids.image_input.text.strip()
        p.save()
        self.get_stocks()

    @mainthread
    def set_stocks(self, stocks):
        # self.ids.g1_stocks.clear_widgets() # todo check error with this line 
        for p in stocks:
            pt = StockTile()
            pt.name = p.name
            pt.category = p.category.name if p.category else "N/A"
            pt.description = p.description or ""
            pt.price = str(p.price)
            pt.quantity = str(p.quantity_in_stock)
            pt.brand = p.brand
            pt.image_url = p.image or ""
            pt.callback = self.delete_stock
            pt.bind(on_release=self.update_stock)
            self.ids.g1_stocks.add_widget(pt)

    def add_new(self):
        md = ModStock()
        md.callback = self.add_stocks
        md.open()


class ModStock(ModalView):
    callback = ObjectProperty(allownone=True)
    name = StringProperty("")
    category = StringProperty("")
    description = StringProperty("")
    price = StringProperty("")
    quantity = StringProperty("")
    brand = StringProperty("")
    image_url = StringProperty("")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 0.1)

    def render(self, _):
        pass

    def on_name(self, inst, val):
        self.ids.name_input.text = val

    def on_category(self, inst, val):
        self.ids.category_input.text = val

    def on_description(self, inst, val):
        self.ids.description_input.text = val

    def on_price(self, inst, val):
        self.ids.price_input.text = val

    def on_quantity(self, inst, val):
        self.ids.quantity_input.text = val

    def on_brand(self, inst, val):
        self.ids.brand_input.text = val

    def on_image_url(self, inst, val):
        self.ids.image_input.text = val


class StockTile(ButtonBehavior, BoxLayout):
    product_id = NumericProperty()
    name = StringProperty("")
    category = StringProperty("")
    description = StringProperty("")
    price = StringProperty("")
    quantity = StringProperty("")
    brand = StringProperty("")
    image_url = StringProperty("")
    callback = ObjectProperty(allownone=True)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Clock.schedule_once(self.render, 0.1)

    def delete_Product(self):
        if self.callback:
            self.callback(self)

    def render(self, _):
        pass
