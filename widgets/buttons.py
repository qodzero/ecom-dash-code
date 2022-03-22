from kivy.uix.button import Button
from kivy.lang import Builder

from kivy.properties import ColorProperty, ListProperty, StringProperty
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp, sp
from kivy.utils import rgba

Builder.load_string("""
<FlatButton>:
    text_size: self.size
    valign: "middle"
    halign: "center"

<IconButton>:
    canvas.after:
        Color:
            rgba: [1,1,1,1]
        Rectangle:
            pos: self.pos
            size: self.size
            source: self.source

<RoundedButton>:
    markup: True
    text_size: self.size
    halign: 'center'
    valign: 'middle'
""")
class FlatButton(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_color = [0,0,0,0]
        self.background_down = ""
        self.background_normal = ""
        self.background_disabled = ""
        self.markup = True

class IconButton(FlatButton):
    source = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)

class RoundedButton(FlatButton):
    bcolor = ColorProperty([1,1,1,0])
    radius = ListProperty([dp(1)])
    def __init__(self, **kw):
        super().__init__(**kw)

        with self.canvas.before:
            self.paint = Color(rgba=self.bcolor)
            self.draw = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

        self.bind(pos=self.update)
        self.bind(size=self.update)

    def update(self, *args):
        self.draw.pos = self.pos
        self.draw.size = self.size

    def on_radius(self, *args):
        self.draw.radius = self.radius

    def on_bcolor(self, *args):
        self.paint.rgba = self.bcolor