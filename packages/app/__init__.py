from kivy.app import App
from kivy.utils import QueryDict, rgba
from kivy.metrics import dp, sp
from kivy.properties import ColorProperty, ListProperty

from .view import MainWindow


class MainApp(App):
    theme = "light"
    color_primary = ColorProperty(rgba("#9ab2bf"))
    color_secondary = ColorProperty(rgba("#a8a8a8"))
    color_tertiary = ColorProperty(rgba("#4b4745"))
    color_alternate = ColorProperty(rgba("#f5f7ff"))
    color_primary_bg = ColorProperty(rgba("#f9f8f8"))
    color_secondary_bg = ColorProperty(rgba("#f0eeee"))
    color_primary_text = ColorProperty(rgba("#000000"))
    color_secondary_text = ColorProperty(rgba("#edf0f0"))
    fonts = QueryDict()
    fonts.size = QueryDict()
    fonts.size.extra = dp(54)
    fonts.size.h1 = dp(24)
    fonts.size.h2 = dp(22)
    fonts.size.h3 = dp(18)
    fonts.size.h4 = dp(16)
    fonts.size.h5 = dp(14)
    fonts.size.h6 = dp(12)
    fonts.heading = "assets/fonts/Roboto/Roboto-Black.ttf"
    fonts.subheading = "assets/fonts/Roboto/Roboto-Bold.ttf"
    fonts.body = "assets/fonts/Roboto/Roboto-Medium.ttf"
    fonts.styled = "assets/fonts/Lobster/Lobster-Regular.ttf"

    def build(self):
        return MainWindow()

    def toggle_theme(self):
        if self.theme == "dark":
            self.color_primary = ColorProperty(rgba("#4E2FE3"))
            self.color_secondary = ColorProperty(rgba("#3FD0B6"))
            self.color_tertiary = ColorProperty(rgba("#E35588"))
            self.color_alternate = ColorProperty(rgba("#BF2FE3"))
            self.color_primary_bg = ColorProperty(rgba("#fffdf0"))
            self.color_secondary_bg = ColorProperty(rgba("#3B3947"))
            self.color_primary_text = ColorProperty(rgba("#3B3947"))
            self.color_secondary_text = ColorProperty(rgba("#EFEFEF"))
        else:
            color_primary = ColorProperty(rgba("#3B0BFB"))
            color_secondary = ColorProperty(rgba("#1e8a49"))
            color_tertiary = ColorProperty(rgba("#F27373"))
            color_alternate = ColorProperty(rgba("#EFF9FF"))
            color_primary_bg = ColorProperty(rgba("#fffdf0"))
            color_secondary_bg = ColorProperty(rgba("#EFEFEF"))
            color_primary_text = ColorProperty(rgba("#000000"))
            color_secondary_text = ColorProperty(rgba("#626262"))
