from model import Restaurant, Table, Menu, User
import uuid
from enums import UserRole

class DataProvider:
    def __init__(self):
        # Create user list
        self.__user_list = []
        self._create_users()
        self.__restaurant_list = []
        self._create_restaurant_list()

    # Create method for user list
    def _create_users(self):
        user1 = User("1", "1", UserRole.MANAGER)
        user2 = User("2", "2", UserRole.WAITER)
        user3 = User("3", "3", UserRole.COOKER)
        self.__user_list.append(user1)
        self.__user_list.append(user2)
        self.__user_list.append(user3)

    @property
    def user_list(self):
        return self.__user_list

    def _create_restaurant_list(self):
        restaurant_names = ["Restaurant1", "Restaurant2", "Restaurant3", "Restaurant4"]
        for name in restaurant_names:
            restaurant = Restaurant(uuid.uuid4(), name, "Some Address")
            self.__restaurant_list.append(restaurant)
            self._create_menu_list_for_restaurant(restaurant)
            self._create_table_list_for_restaurant(restaurant)

    def _create_menu_list_for_restaurant(self, restaurant):
        item_id_counter = 1  # Start item IDs from 1
        for menu_index in range(1, 4):  # 3 menus
            menu = Menu(id=str(menu_index), menu_name=f"{restaurant.name} Menu_Name_{menu_index}")

            # Add some menu items to the menu
            for item_index in range(2):  # 2 items per menu
                menu_item = {
                    "id": str(item_id_counter),  # Now it's "1", "2", "3", etc.
                    "name": f"Item_{item_index + 1}",
                    "price": f"{5 * (item_index + 1)}",  # Example: 5, 10
                    "type": "Meal" if item_index % 2 == 0 else "Drink"
                }
                menu.add_menu_item(menu_item)
                item_id_counter += 1  # Increment ID for next item

            restaurant.add_menu(menu)



    def _create_table_list_for_restaurant(self, restaurant):
        for id in range(1, 4):
            table = Table(table_id=str(uuid.uuid4()), seats=4)  # Assuming 4 seats per table
            restaurant.table_list.append(table)

    def _print_data(self):
        for restaurant in self.restaurant_list:
            print("--------------------------------------------")
            print("Menu List in the " + restaurant.name + " Restaurant")
            print("--------------------------------------------")
            for menu in restaurant.menu_list:
                print("\t" + menu.menu_name)
                print("-----------------------------------------------")
            print("\t" + "Table List in " + restaurant.name + " Restaurant")
            print("\t" + "----------------------------------------------------")
            for table in restaurant.table_list:
                print(f"\t\tTable ID: {table.table_id}, Seats: {table.seats}")
            print("------------------------------------------------")

    @property
    def restaurant_list(self):
        return self.__restaurant_list