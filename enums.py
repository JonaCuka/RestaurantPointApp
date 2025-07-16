from enum import Enum

class ItemType(Enum):
    MEAL = "Meal"
    DRINK = "Drink"

class UserRole(Enum):
    MANAGER = 1
    WAITER = 2
    COOKER = 3
    

class UserFeauters(Enum):
    RESTAURANT_MANAGER = "Restaurant Manager"
    MENU_MANAGER = "Menu Manager"
    MENU_ITEM_MANAGER = "Menu Item Manager"
    TABLE_MANAGER = "Table Manager"
    TABLE_ORDERS = "Table Orders"
    ORDER_STATUS = "Order Status"
    SIGN_OUT = "Sign Out"

