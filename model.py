from enums import UserRole, ItemType

class User:

    def __init__(self, username: str, password: str, user_role: UserRole):
        self.__username = username
        self.__password = password
        self.__user_role = user_role
    
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, username):  
        self.__username = username
    
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        self.__password = password
    
    @property
    def user_role(self):
        return self.__user_role
    
    @user_role.setter
    def user_role(self, user_role):  
        self.__user_role = user_role


        
class Restaurant:
    def __init__(self, id, name, address, menu_list=None, table_list=None):
        self.__id = id
        self.__name = name
        self.__address = address
        self.__menu_list = menu_list if menu_list is not None else []
        self.__table_list = table_list if table_list is not None else []

    @property
    def id(self):
       return self.__id

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, address):
        self.__address = address

    @property
    def menu_list(self):
        return self.__menu_list
    
    @menu_list.setter
    def menu_list(self, menu_list):
        self.__menu_list = menu_list

    @property
    def table_list(self):
        return self.__table_list
    
    @table_list.setter
    def table_list(self, table_list):
        self.__table_list = table_list

    def add_menu(self, menu):
        self.__menu_list.append(menu)

    def update_menu(self, menu_id, menu_name):
        for menu in self.__menu_list:
            if menu.id == menu_id:
                menu.menu_name = menu_name
                break

    def delete_menu(self, menu_id):
        self.__menu_list = [menu for menu in self.__menu_list if menu.id != menu_id]


class Menu:
    def __init__(self, id, menu_name):
        self.__id = id
        self.__menu_name = menu_name
        self.menu_item_list = []

    def add_menu_item(self, item):
        self.menu_item_list.append(item)

    def update_menu_item(self, item_id, new_id, new_name, new_price, new_type):
        for item in self.menu_item_list:
            if item["id"] == item_id:
                item.update({"id": new_id, "name": new_name, "price": new_price, "type": new_type})

    def delete_menu_item(self, item_id):
        self.menu_item_list = [item for item in self.menu_item_list if item["id"] != item_id]    

    @property
    def id(self):
        return self.__id
    
    @property
    def menu_name(self):
        return self.__menu_name
    
    @menu_name.setter
    def menu_name(self, menu_name):
        self.__menu_name = menu_name


class Table:
    def __init__(self, table_id, seats, status='Available'):
        self.__table_id = table_id
        self.__seats = seats
        self.__status = status

    @property
    def table_id(self):
        return self.__table_id

    @property
    def seats(self):
        return self.__seats

    @seats.setter
    def seats(self, seats):
        self.__seats = seats

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status
    

    def add_table(self, table):
        self.__table_list.append(table)

    def update_table_status(self, table_id, new_status):
        for table in self.__table_list:
            if table.table_id == table_id:
                table.status = new_status
                break

    def delete_table(self, table_id):
        self.__table_list = [table for table in self.__table_list if table.table_id != table_id]
