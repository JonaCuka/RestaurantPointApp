from kivymd.app import MDApp  
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from view import LoginScreen


class App(MDApp):  
    def build(self):
       
        Window.size = (600,600)
        Window.top = 30
        Window.left = 20
        
        self.screen_manager = ScreenManager()
        self.login_screen = LoginScreen(name = 'login_screen')
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.bind(current = self.on_screen_change)
        return self.screen_manager
    
    def on_screen_change(self, screen_manager, current_screen_name ):
        if current_screen_name == 'login_screen':
            Window.size = (400,600)
        elif current_screen_name == 'two_panel_layout_screen':
            Window.size = (1400,800) 
App().run()




