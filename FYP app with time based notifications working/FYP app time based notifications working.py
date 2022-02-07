from dis import show_code
from errno import EALREADY
from turtle import settiltangle, update
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
from kivy.clock import Clock
from datetime import datetime
from time import strftime, time
import random


#--------------------------------   Global Variables-----------------------------------------------------------------------------



class SettingsScreen(Screen):
    #earliest_var = ObjectProperty(None)
    #latest_var = ObjectProperty(None)
    
    def submitButton(self):
        
        self.earliest_time = str(self.earliest_var.text)
        self.latest_time = str(self.latest_var.text)
        print("Now: ",self.earliest_time,self.latest_time)
        return self.earliest_time, self.latest_time
     

class MainMenuScreen(Screen):
    pass
        
class SurveyScreen(Screen):
    def toSurvey(self):
        import webbrowser
        webbrowser.open('https://forms.gle/e4di6afpdqwKr2df9')

class AltSurveyScreen(Screen):
    pass
    
class FeedbackScreen(Screen):
    pass

class InformationScreen(Screen):
    pass

class OnboardSurveyScreen(Screen):
    pass 
    
class DisplayScreenManager(ScreenManager):
    pass

sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='mainMenuScreen'))
sm.add_widget(SettingsScreen(name='settingsScreen'))
sm.add_widget(SurveyScreen(name='surveyScreen'))
sm.add_widget(FeedbackScreen(name='feedbackScreen'))
sm.add_widget(InformationScreen(name='informationScreen'))
sm.add_widget(OnboardSurveyScreen(name= 'onboardSurveyScreen'))
sm.add_widget(AltSurveyScreen(name='altSurveyScreen'))


class Menu(App):

    # global variables
    time_list =[]
    #surevy_taken = False
    survey_number = 0 # number of survey for the day, 6 surveys in total with indeces 0 - 5

    def __build__(self):

        return sm
       # return SettingsScreen

    def on_start(self):
        print("Survey Number on start: ",self.survey_number)
        self.showTime(1)
        self.updateTime(1)
        self.setTargetTime(self.time_list)
        self.checkNotification(1)
        self.conituousylyCheck(1)
        print("Survey Number on start: ",self.survey_number)
        return super().on_start()

    def processVariables (self):
        text = self.root.ids.Earliest.text
        print(text)
        return text

# --------------- Settings screen functions -------------------------------#

    def submitButton(self):
        self.earliest_value = self.processVariables()
        print(self.earliest_value)


# ------------- Main Menu Screen Functions ------------------------

    clock_var = ObjectProperty(None)
    
    def showTime(self,tick):
            # returns current time in hour:minute:second format as a string
            time_var = datetime.now().strftime("%H:%M:%S")
            #print(time_var)
            return time_var
            

    def updateTime(self, tick):
        # continuously calls showTime function to update the time variable
        Clock.schedule_interval(self.showTime,1)

        
    def notify(self, title, message):
        # notification
        title = title
        message = message
        kwargs = {'title': title, 'message': message}

        notification.notify(**kwargs)

    
    def setTargetTime(self,update_list):
        # returns list of times to be used in triggering notification. hour and minute values are randomly generated and the sorted list is returned
        # takes parameter of the list, so when calling need to pass in list from the global variable list
        for i in range(6):
            hour = random.randint(10,20)
            minute = random.randint(0,59)
            
            if len(str(minute)) ==2: 
                time_value = str(hour)+":"+str(minute)+":00"
            else: 
                time_value = str(hour)+":0"+str(minute)+":00"
            update_list.append(time_value)
            update_list.sort()
            
        print(update_list)
        return update_list






    def surveyTaken(self):
        #  !TODO needs to be reset every day --> no need, create list of lists, 1 list for each day, move on to next list on next day
        # triggered when "Survey" button is pressed. Keeps track of how many surveys are completed
        # also used when triggering notifications. That#s how the sytem knows to move on to the next time value in the time list
        if self.survey_number < 5:
            self.survey_number += 1
        else: 
            self.survey_number = 5
            print("Error: List index out of range") # way of catching errors and making sure the index doesn#t go out of bounds

        
        
        

    def checkNotification(self,tick):
        # checks current time and when time matched the value in the timelist, a notification is triggered
        time = self.showTime(1)
        #while self.survey_number < len(self.time_list):
        if time == self.time_list[self.survey_number]:
            self.notify("Hello World!","It's Survey Time")
            
            



    def conituousylyCheck(self,tick):
        # continuously calls previous function to make sure it#s checked every second
        # !TODO ask Laura about changing time interval, as it is it checks every second, could break it
        Clock.schedule_interval(self.checkNotification,1)

    def snooze(self):
        # snooze button
        # updates time value in the list by adding 5 minutes
        # !TODO need to change to add 5 minutes to current time value, not list time value
        # !TODO need to make sure that after 3 snoozes, system moves on to next value in time list (meaning survey is not taken)

        #print("Survey number: ",self.survey_number)
        time_value = self.time_list[self.survey_number] # gets value for current survey from time list
        time_value_list = time_value.split(":") # splits that value into list with 3 values: [hour, minute, second])
        
        hour_value = int(time_value_list[0]) # assigns values from list to variables for updating
        minute_value = int(time_value_list[1])
        if minute_value >= 55 and minute_value <= 59 : # this is used to make sure the minute value doesn'z go over 60 and that in that case the hour value is also updated
            new_minute_value = minute_value - 55
            new_hour_value = hour_value +1
            new_time_value = str(new_hour_value)+":0"+str(new_minute_value)+":00"

        else: # this is the normal case, just adds 5 minutes to the minute value
            new_minute_value = minute_value + 5
            new_time_value = str(hour_value)+":"+str(new_minute_value)+":00"
        print(self.time_list)
        self.time_list[self.survey_number] = new_time_value # updates time value in global time list
        print(self.time_list)
        
        

    # ------------------------ Surveys -----------------------------------

    def toSurvey(self):
        import webbrowser
        webbrowser.open('https://forms.gle/e4di6afpdqwKr2df9')
        


if __name__ == "__main__":
    Menu().run()