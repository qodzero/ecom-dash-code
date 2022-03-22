
from kivy.app import App

from .view import MainWindow

class MainApp(App):
    def build(self):
        return MainWindow()
