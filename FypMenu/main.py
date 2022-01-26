import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

class CanvasWidget(Widget):
    pass

class MainMenu(GridLayout):
    def toSurvey(self):
        import webbrowser
        webbrowser.open('https://forms.gle/e4di6afpdqwKr2df9')

class Menu(App):
    def __build__(self):
        return CanvasWidget()


if __name__ == "__main__":
    Menu().run()