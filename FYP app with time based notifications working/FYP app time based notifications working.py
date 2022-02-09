from dis import show_code
from errno import EALREADY
from turtle import color, settiltangle, update
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
   
    
    def submitButton(self):
        
        self.earliest_time = str(self.earliest_var.text)
        self.latest_time = str(self.latest_var.text)
        print("Now: ",self.earliest_time,self.latest_time)
        return self.earliest_time, self.latest_time
     

class MainMenuScreen(Screen):
    pass
        
class SurveyScreen(Screen):
  pass

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
    time_list =[]
    #surevy_taken = False
    survey_number = 0
    times_generated = True
    day_number = 0

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
        #print("Survey Number on start: ",self.survey_number)
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
            
            time_var = datetime.now().strftime("%H:%M:%S")
            return time_var
            

    def updateTime(self, tick):
        Clock.schedule_interval(self.showTime,1)

        
    def notify(self, title, message):
        title = title
        message = message
        kwargs = {'title': title, 'message': message}

        notification.notify(**kwargs)
    
    def setTargetTime(self,update_list):
        
        for i in range(6):
            hour = random.randint(10,20) # random hour value between 10 am and 8 pm, hardcoded for now
            minute = random.randint(0,59) # random minute value  between 0 and 59
            
            if len(str(minute)) ==2: 
                time_value = str(hour)+":"+str(minute)+":00"
            else: 
                time_value = str(hour)+":0"+str(minute)+":00" # this makes sure that the time is written to the list correctly as "10:01" and not "10:1"
            update_list.append(time_value) # creates list of the values that have been created
            update_list.sort() # sorts the list to make sure that they are sorted by time value --> to trigger notifications porperly
        
        print(update_list)
        return update_list


    def surveyTaken(self):
        # this si triggered when the Survey button is clicked
        # what it does:
        # - updates survey number vairable which is used to determine which time to use to trigger the next survey
        # - when all 6 surveys of the day are completed, in increases the day variable
        # - taht tracks which day it is
        # is it's the weekend (day 5 and 6) then no survey is triggered and at midnight, the day variable is increased

        
        if self.day_number== 5: # Day: saturday, no surveys should be triggered
            self.survey_number = 0 # reset survey number variable
            self.time_list = []
            self.time_list.append("23:59:59") # when this time comes, the check update function will update the day variable instead of triggering a survey, see line 185
            print(self.time_list)
            
        elif self.day_number == 6:# Day: SUnday, no survey triggered
            self.survey_number = 0
            self.time_list = []
            self.time_list.append("23:59:59")
            print(self.time_list)

        else: # any day that is not a weekend, as in every day where we send out survey
            # this checks which survey has been taken and increases the survey number variable which

            if self.survey_number < 5: # update survey number until all 6 are complete
                self.survey_number += 1
                print("Survey Number: ", self.survey_number) # for testing
            else: 
                self.survey_number = 0 # reset survey number for next day (survey number used to access correct time value)
                self.day_number += 1 # increase day by 1 to keep track of which day of study we're on
                print("Day: ", self.day_number)
                self.time_list = [] # reset time list
                self.setTargetTime(self.time_list) # creating new time list for the next da
          


    def checkNotification(self,tick):
        #!TODO the app notification probelm could be solved with toast notifications 
        
        time = self.showTime(1) # access current time value in hour:minute:second format
        if self.day_number == 5: # is Saturday: skips to next day without survey being taken
            if time == self.time_list[0]:
                self.day_number += 1 
                print("updated Day: ", self.day_number)
                self.surveyTaken()
        elif self.day_number == 6: # if Sunday: skips to next day without survey being taken and reconfiguring a new time list
            if time == self.time_list[0]:
                self.day_number += 1
                print("updated Day: ", self.day_number)
                self.setTargetTime(self.time_list) # triggers setting time list for Monday
                

        else: 
            if time == self.time_list[self.survey_number]: # any other day where surveys are triggeres normally
                self.notify("Hello World!","It's Survey Time")  # triggers notification
            

    def conituousylyCheck(self,tick): # calls previous function once per second --> checks for match between current time and value in time list
        Clock.schedule_interval(self.checkNotification,1)

    def snooze(self):
        #print("Survey number: ",self.survey_number)
        #time_value = self.time_list[self.survey_number]
        #time_value_list = time_value.split(":")
        #print (time_value_list)
        # this way it takes the time value from the list
        # the way below adds 5 minutes to current time (because user won't always snooze exactly when notification is given)
        time = self.showTime(1)
        time_values = time.split(":")
        
        hour_value = int(time_values[0])
        minute_value = int(time_values[1])
        if minute_value >= 55 and minute_value <= 59 :
            new_minute_value = minute_value - 55
            new_hour_value = hour_value +1
            new_time_value = str(new_hour_value)+":0"+str(new_minute_value)+":00"

        else: 
            new_minute_value = minute_value + 5
            new_time_value = str(hour_value)+":"+str(new_minute_value)+":00"
        print(self.time_list)
        self.time_list[self.survey_number] = new_time_value
        print(self.time_list) # updates time list with new value when the next notification will be sent
        
        

    # ------------------------ Surveys -----------------------------------

    def toSurvey(self, survey_link, end_of_day_survey):
        # !TODO need to add end of day Survey

        import webbrowser
        if self.survey_number != 6:
            webbrowser.open(survey_link)
        else: 
            webbrowser.open(end_of_day_survey)
        


if __name__ == "__main__":
    Menu().run()
