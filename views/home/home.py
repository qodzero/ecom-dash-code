from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict
from kivy.clock import Clock

import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib as mpl
import matplotlib.pyplot as plt

from widgets.kivyplt import MatplotFigure

Builder.load_file('views/home/home.kv')
class Home(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        x = np.array([x for x in range(7)])
        xlabels = ['', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', "Thur", 'Fri']
        y = np.array([0, 8, 16, 14, 12, 9, 18])

        xy_spline = make_interp_spline(x,y)
        x1 = np.linspace(x.min(), x.max(), 500)
        y1 = xy_spline(x1)

        chart = mpl.figure.Figure(figsize=(2,2))
        chart.gca().spines['top'].set_visible(False)
        chart.gca().spines['right'].set_visible(False)
        chart.gca().spines['left'].set_visible(False)
        chart.gca().set_xticklabels(xlabels)
        chart.gca().plot(x1,y1)

        plot = MatplotFigure(chart)
        plot.pos = [-2, 0]
        self.ids.graph.clear_widgets()
        self.ids.graph.add_widget(plot)
