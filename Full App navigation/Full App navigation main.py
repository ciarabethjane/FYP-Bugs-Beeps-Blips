import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from plyer import notification
from plyer.utils import platform


class SettingsScreen(Screen):
    earliest_var = ObjectProperty(None)
    latest_var = ObjectProperty(None)

    def submitButton(self):
        print(self.earliest_var.text, self.latest_var.text)

    


class MainMenuScreen(Screen):
    def toSurvey(self):
        import webbrowser
        webbrowser.open('https://forms.gle/e4di6afpdqwKr2df9')

    def notify(self, title, message):
        title = title
        message = message
        kwargs = {'title': title, 'message': message}

        notification.notify(**kwargs)

class SurveyScreen(Screen):
    def toSurvey(self):
        import webbrowser
        webbrowser.open('https://forms.gle/e4di6afpdqwKr2df9')


class FeedbackScreen(Screen):
    pass

class InformationScreen(Screen):
    pass

class OnboardSurveyScreen(Screen):
    def toSurvey(self):
        import webbrowser
        webbrowser.open('https://forms.gle/e4di6afpdqwKr2df9')
    

class DisplayScreenManager(ScreenManager):
    pass

sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='mainMenuScreen'))
sm.add_widget(SettingsScreen(name='settingsScreen'))
sm.add_widget(SurveyScreen(name='surveyScreen'))
sm.add_widget(FeedbackScreen(name='feedbackScreen'))
sm.add_widget(InformationScreen(name='informationScreen'))
sm.add_widget(OnboardSurveyScreen(name= 'onboardSurveyScreen'))


class Menu(App):
    def __build__(self):
        return sm


if __name__ == "__main__":
    Menu().run()
