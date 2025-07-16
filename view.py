from kivy.uix.screenmanager import Screen
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from controller import LoginController
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from enums import UserRole
from data_provider import DataProvider, Restaurant
from utils import AuthorizationServices, UserFeaturesContentPanelResolver
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from admin_view import RestaurantManagerContentPanel

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username_input = None
        self.password_input = None
        self.add_widget(self._create_login_components())

    def _create_login_components(self):
        layout = BoxLayout(orientation='vertical')
        
        with layout.canvas.before:
            Color(1, 1, 1, 1)  # Background color white
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)


        form_layout = GridLayout(cols=1, padding=[0, 0, 0, 1], spacing=20, size_hint=(None, None), size=("400dp", "400dp"))
        form_layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}  # Adjusted position hint

        self._create_username_component()
        form_layout.add_widget(self.username_input)

        self._create_password_component()
        form_layout.add_widget(self.password_input)

        login_button = self._create_button_component()
        form_layout.add_widget(login_button)

        layout.add_widget(form_layout)
        return layout

    def _create_username_component(self):
        self.username_input = MDTextField(hint_text="Username", size_hint=(1, None), height="50dp")

    def _create_password_component(self):
        self.password_input = MDTextField(password=True, hint_text="Password", size_hint=(1, None), height="50dp")

    def _create_button_component(self):
        login_button = Button(
            text="Login",
            size_hint=(1, None),
            height="50dp",
            background_color=(0, 0.5, 1, 1),
            color=(1, 1, 1, 1)
        ) 
        login_button.bind(on_press=self.login_with_provided_credentials)
        return login_button

    def login_with_provided_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if self._are_credentials_provided(username, password):
            LoginController.login_in_user(username, password)
            user = LoginController.get_logged_in_user()
            if user is None:
                popup = Popup(title="Login failed", content=Label(text="Invalid username or password"),
                            size_hint=(None, None), size=(400, 200))
                popup.open()
            else:
                screen_name = 'two_panel_layout_screen'
                if self.manager.has_screen(screen_name):
                    screen_to_remove = self.manager.get_screen(screen_name)
                    self.manager.remove_widget(screen_to_remove)

                self.two_panel_layout_screen = TwoPanelLayoutScreen(name= screen_name)
                self.manager.add_widget(self.two_panel_layout_screen)
                self.manager.current = screen_name
                self._reset_fields()  

    def _are_credentials_provided(self, username, password):
        if LoginController.is_string_none_or_blank(username):
            popup = Popup(title="Credentials missing", content=Label(text="Please provide your username"),
                           size_hint=(None, None), size=(400, 200))
            popup.open()
            return False
        elif LoginController.is_string_none_or_blank(password):
            popup = Popup(title="Credentials missing", content=Label(text="Please provide your password"),
                           size_hint=(None, None), size=(400, 200))
            popup.open()
            return False
        return True
    
    def _reset_fields(self):
        self.username_input.text = ""
        self.password_input.text = ""

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class TwoPanelLayoutScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = LoginController.get_logged_in_user()
        self.add_widget(self._create_split_layout_panel())

    def _create_split_layout_panel(self):
        self.split_layout_panel = GridLayout(cols=2)
        self.split_layout_panel.add_widget(self._create_navigation_bar_panel())
        self.split_layout_panel.add_widget(self._create_content_panel())
        return self.split_layout_panel   

    def _create_navigation_bar_panel(self):
        navigation_bar_panel = GridLayout(cols=1, spacing=20)
        navigation_bar_panel.size_hint_x = 0.3
    
        self.navigation_bar_buttons = self._create_navigation_bar_panel_component()
        for button in self.navigation_bar_buttons:
            if button.text != "Sign Out":
                button.bind(on_press=self._change_content_panel_label)
            else:
                button.bind(on_press=self._sign_out)
            navigation_bar_panel.add_widget(button)
        return navigation_bar_panel
    
    def _create_navigation_bar_panel_component(self):
        navigation_bar_buttons = []
        authorization_service = AuthorizationServices()
        user_role = self.user.user_role
        user_features = authorization_service.get_user_feature_by_user_role(user_role)
        
        for feature in user_features:
            button = Button(text=feature.value, background_color=(0, 1, 1, 1),
                            color=(0, 1, 1, 1),
                            font_size="18sp",
                            size_hint=(1, None))
            button.user_feature = feature
            button.size = (300, 60)
            navigation_bar_buttons.append(button)
        return navigation_bar_buttons

    def _create_content_panel(self):
        self.content_panel = GridLayout(cols=1, spacing=20)
        self.content_panel.size_hint_x = 0.8
        
        self.content_panel_content = Label(text="Content Space", size_hint=(1, 0.9), color=(0, 0, 0, 1))
        
        self.content_panel.add_widget(self.content_panel_content)
        return self.content_panel   
    
    def _change_content_panel_label(self, instance):
        self.split_layout_panel.clear_widgets()
        self.split_layout_panel.add_widget(self._create_navigation_bar_panel())
        user_feature = instance.user_feature
        user_feature_panel = UserFeaturesContentPanelResolver.get_user_feature_panel(user_feature)
        self.split_layout_panel.add_widget(user_feature_panel)
        for button in self.navigation_bar_buttons:
            if button.text == instance.text:
                button.background_color = (0, 0, 0, 1)
                self.content_panel_content.color = (0, 0, 0)
            else:
                button.background_color = (0, 1, 1, 1)    

    def _sign_out(self, instance):
        self.manager.current = 'login_screen'


class LoginScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.username_input = None
        self.password_input = None
        self.add_widget(self._create_login_components())

    def _create_login_components(self):
        layout = GridLayout(cols=1, padding=150, spacing=30)
        self._create_username_component()
        layout.add_widget(self.username_input)

        self._create_password_component()
        layout.add_widget(self.password_input)

        login_button = self._create_button_component()
        layout.add_widget(login_button)
        return layout

    def _create_username_component(self):
        self.username_input = MDTextField(hint_text="Enter Username", size_hint=(None, None), size=("300dp", "50dp"))

    def _create_password_component(self):
        self.password_input = MDTextField(password=True, hint_text="Enter Password", size_hint=(None, None), size=("300dp", "50dp"))

    def _create_button_component(self):
        login_button = Button(
            text="Login",
            size_hint=(None, None),
            size=(100, 50),
            background_color=(1, 1, 1, 1)  
        ) 
        return login_button