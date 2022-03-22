
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.properties import StringProperty

class MainWindow(BoxLayout):
    username = StringProperty("Samuel M")
    avatar = StringProperty("assets/imgs/avatar.jpg")
    def __init__(self, **kw):
        super().__init__(**kw)

class NavTab(ToggleButtonBehavior, BoxLayout):
    text = StringProperty("")
    icon = StringProperty("")
    icon_active = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)
