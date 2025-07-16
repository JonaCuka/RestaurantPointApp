from data_provider import DataProvider

class LoginController:
    # Singleton pattern
    __login_controller = None 

    def __new__(cls):
        if cls.__login_controller is None:
            cls.__login_controller = super(LoginController, cls).__new__(cls) 
        return cls.__login_controller

    def __init__(self):
        if not hasattr(self, '__logged_in_user'):  # Fix typo (__login_in_user -> __logged_in_user)
            self.__logged_in_user = None

    @staticmethod
    def login_in_user(username, password):
        user_data_provider = DataProvider()
        user_list = user_data_provider.user_list
        for user in user_list:
            if user.username == username and user.password == password:
                instance = LoginController.get_instance()
                instance.__logged_in_user = user
                return True  # Indicate successful login
        return False  # Indicate login failure

    @staticmethod
    def get_instance():
        if LoginController.__login_controller is None:
            LoginController.__login_controller = LoginController()
        return LoginController.__login_controller

    @staticmethod
    def get_logged_in_user():
        return LoginController.get_instance().__logged_in_user  # Ensure returning the logged-in user

    @staticmethod
    def is_string_none_or_blank(value):
        return value in (None, "")
