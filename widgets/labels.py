from kivy.lang import Builder
from kivy.uix.label import Label

Builder.load_string("""
<Text>:
    text_size: self.size
    valign: "middle"
    font_name: app.fonts.subheading
    shorten_from: "right"
    shorten: True
    color: [0,0,0, 1]
    markup: True
""")
class Text(Label):
    def __init__(self, **kw):
        super().__init__(**kw)