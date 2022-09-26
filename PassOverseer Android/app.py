import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import random

kivy.require('1.9.0')


class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

    def give_pw(self):
        self.pw.text = str(random.randint(0, 100))


class PassOverseer(App):
    def build(self):
        return MyRoot()


passoverseer = PassOverseer()
passoverseer.run()