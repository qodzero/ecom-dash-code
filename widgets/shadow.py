from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior
from PIL import Image, ImageDraw, ImageFilter
import kivy.properties as props
from kivy.clock import Clock

kv = """
<ShadowBox>:
    canvas.before:
        Color:
            rgba: 1,1,1,1
        RoundedRectangle:
            size: self.shadow_size1
            pos: self.shadow_pos1
            texture: self.shadow_texture1
            radius: self.radius
        RoundedRectangle:
            size: self.shadow_size2
            pos: self.shadow_pos2
            texture: self.shadow_texture2
            radius: self.radius
    BoxLayout:
        id: main
        orientation: root.orientation
        canvas.before:
            Color:
                rgba: root.bcolor
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: root.radius
"""


RAD_MULT = 0.25 #  PIL GBlur seems to be stronger than Chrome's so I lower the radius

Builder.load_string(kv)
class ShadowBox(ButtonBehavior, BoxLayout):
    radius = props.ListProperty([1])
    shadow_texture1 = props.ObjectProperty(None)
    shadow_pos1 = props.ListProperty([0, 0])
    shadow_size1 = props.ListProperty([0, 0])
    bcolor = props.ColorProperty([1,1,1,1])

    shadow_texture2 = props.ObjectProperty(None)
    shadow_pos2 = props.ListProperty([0, 0])
    shadow_size2 = props.ListProperty([0, 0])

    elevation = props.NumericProperty(1)
    _shadow_clock = None

    _shadows = {
        1: (1, 3, 0.12, 1, 2, 0.24),
        2: (3, 6, 0.16, 3, 6, 0.23),
        3: (10, 20, 0.19, 6, 6, 0.23),
        4: (14, 28, 0.25, 10, 10, 0.22),
        5: (19, 38, 0.30, 15, 12, 0.22)
    }

    # Shadows for each elevation.
    # Each tuple is: (offset_y1, blur_radius1, color_alpha1, offset_y2, blur_radius2, color_alpha2)
    # The values are extracted from the css (box-shadow rule).
    def __init__(self, *args, **kwargs):
        super(ShadowBox, self).__init__(*args, **kwargs)
        self._orig_elev = 1

        self._update_shadow = Clock.create_trigger(self._create_shadow)

    def on_padding(self, inst, value):
        self.padding = 0
        self.ids.main.padding = value

    def on_spacing(self, inst, value):
        self.spacing = 0
        self.ids.main.spacing = value

    def add_widget(self, widget, index=0):
        if len(self.children) == 0:
            super().add_widget(widget, index=index)
        else:
            self.ids.main.add_widget(widget, index=index)

    def remove_widget(self, widget):
        self.ids.main.remove_widget(widget)

    def clear_widgets(self):
        self.ids.main.clear_widgets()

    def on_size(self, *args, **kwargs):
        self._update_shadow()

    def on_pos(self, *args, **kwargs):
        self._update_shadow()

    def on_elevation(self, *args, **kwargs):
        self._update_shadow()
    
    def on_radius(self, *args, **kwargs):
        self._update_shadow()
    

    def _create_shadow(self, *args):
        # print "update shadow"
        ow, oh = self.size[0], self.size[1]

        offset_x = 0

        # Shadow 1
        shadow_data = self._shadows[self.elevation]
        offset_y = shadow_data[0]
        radius = shadow_data[1]
        w, h = ow + radius * 6.0, oh + radius * 6.0
        t1 = self._create_boxshadow(ow, oh, radius, shadow_data[2])
        self.shadow_texture1 = t1
        self.shadow_size1 = w, h
        self.shadow_pos1 = [
            self.x - (w - ow) / 2. + offset_x,
            (self.y - (h - oh) / 2. - offset_y)
        ]

        # Shadow 2
        shadow_data = self._shadows[self.elevation]
        offset_y = shadow_data[3]
        radius = shadow_data[4]
        w, h = ow + radius * 6.0, oh + radius * 6.0
        t2 = self._create_boxshadow(ow, oh, radius, shadow_data[5])
        self.shadow_texture2 = t2
        self.shadow_size2 = w, h
        self.shadow_pos2 = [
            self.x - (w - ow) / 2. + offset_x, 
            self.y - (h - oh) / 3.8 - offset_y
        ]

    def _create_boxshadow(self, ow, oh, radius, alpha):
        # We need a bigger texture to correctly blur the edges
        w = ow + radius * 6.0
        h = oh + radius * 6.0
        w = int(w)
        h = int(h)
        texture = Texture.create(size=(w, h), colorfmt='rgba')
        im = Image.new('RGBA', (w, h), color=(1, 1, 1, 0))

        draw = ImageDraw.Draw(im)
        # the rectangle to be rendered needs to be centered on the texture
        x0, y0 = (w - ow) / 2., (h - oh) / 2.
        x1, y1 = x0 + ow - 1, y0 + oh - 1
        draw.rounded_rectangle((x0, y0, x1, y1), self.radius[0], fill=(20, 20, 20, int(90 * alpha)))
        # rgba(64, 67, 108, 0.1)
        im = im.filter(ImageFilter.GaussianBlur(radius * RAD_MULT))
        texture.blit_buffer(im.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        return texture

    # def on_touch_down(self, touch):
    #     if self.collide_point(touch.x, touch.y):
    #         self._orig_elev = self.elevation
    #         self.elevation = 5

    # def on_touch_up(self, touch):
    #     if self.collide_point(touch.x, touch.y):
    #         self.elevation = self._orig_elev