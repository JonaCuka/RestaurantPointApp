from data_provider import DataProvider, Restaurant, Menu
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.widget import Widget
import uuid
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
import logging
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

from model import Table

logging.basicConfig(level=logging.DEBUG)

BUTTON_COLOR = (0.2, 0.4, 0.6, 1)

class RestaurantManagerContentPanel(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_provider = DataProvider()
        self.restaurant_list = self.data_provider.restaurant_list
        self.selected_row_index = None  # Track the selected row index
        self.add_widget(self.create_content_panel())

    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2, spacing=20, size_hint=(1, 1))   
        split_layout_panel.add_widget(self._create_restaurant_input_data_panel())
        split_layout_panel.add_widget(self._create_restaurant_datatable_panel())
        return split_layout_panel

    def _create_restaurant_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20, size_hint=(0.3, 1))

        self.name_input = MDTextField(font_size="18sp", hint_text="Name")
        input_data_component_panel.add_widget(self.name_input)

        self.address_input = MDTextField(font_size="18sp", hint_text="Address")
        input_data_component_panel.add_widget(self.address_input)
        
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel
    
    def _create_buttons_component_panel(self):
        buttons_component_panel = GridLayout(cols=3, padding=0, spacing=20, size_hint=(1, None))

        add_restaurant_button = Button(text="Add", size_hint=(None, None), size=(100, 40), background_color=BUTTON_COLOR)
        add_restaurant_button.bind(on_release=self.add_restaurant)
        update_restaurant_button = Button(text="Update", size_hint=(None, None), size=(100, 40), background_color=BUTTON_COLOR)
        update_restaurant_button.bind(on_release=self.update_restaurant)
        delete_restaurant_button = Button(text="Delete", size_hint=(None, None), size=(100, 40), background_color=BUTTON_COLOR)
        delete_restaurant_button.bind(on_release=self.delete_restaurant)

        buttons_component_panel.add_widget(add_restaurant_button)
        buttons_component_panel.add_widget(update_restaurant_button)
        buttons_component_panel.add_widget(delete_restaurant_button)
        
        return buttons_component_panel
    
    def _create_restaurant_datatable_panel(self):
        restaurant_datatable_panel = GridLayout(cols=1, padding=30, spacing=20, size_hint=(0.7, 1))
        restaurant_datatable_panel.add_widget(self._create_restaurant_dropdown())
        restaurant_datatable_panel.add_widget(self._create_restaurant_datatable())
        return restaurant_datatable_panel

    def _create_restaurant_dropdown(self):
        restaurant_dropdown_button = Button(text="Select a Restaurant", size_hint=(1, None), height=dp(40))
        restaurant_dropdown_button.bind(on_release=self._open_restaurant_selection_dropdown)
        return restaurant_dropdown_button
    
    def _open_restaurant_selection_dropdown(self, button):
        restaurant_menu_items = []
        for restaurant in self.restaurant_list:
            restaurant_menu_items.append(
                {
                    "viewclass" : "OneLineListItem",
                    "text" : restaurant.name,
                }
            )
        restaurant_dropdown = MDDropdownMenu(
            caller=button,
            items=restaurant_menu_items,
            width_mult=4,  # Calculate the width manually if needed
            max_height=dp(150)
        )
        restaurant_dropdown.open()

    def _create_restaurant_datatable(self):
        restaurant_datatable_row_data = []

        for restaurant in self.restaurant_list:
            restaurant_datatable_row_data.append(
                (restaurant.name, restaurant.address)
            )
        self.restaurant_datatable = MDDataTable(
            size_hint=(1, 0.85),
            background_color_header="a733095",
            background_color_cell="aFFFFFF",
            background_color_selected_cell="a733095",
            use_pagination=True,
            rows_num=10,  # Correct property name
            column_data=[
                ("Name", dp(50)),
                ("Address", dp(50)),
            ],
            row_data=restaurant_datatable_row_data
        )

        self.restaurant_datatable.bind(on_row_press=self.on_row_press)

        return self.restaurant_datatable

    def on_row_press(self, instance_table, instance_row):
        try:
            # Get the selected row index
            row_index = instance_row.index // len(instance_table.column_data)
            # Access the selected row data
            selected_row = instance_table.row_data[row_index]
            self.name_input.text = selected_row[0]
            self.address_input.text = selected_row[1]
            self.selected_row_index = row_index  # Update the selected row index
            logging.debug(f"Row {row_index} selected: {selected_row}")
        except Exception as e:
            logging.error(f"Error selecting row: {e}")

    def add_restaurant(self, instance):
        name = self.name_input.text
        address = self.address_input.text
        if name and address:
            new_restaurant = Restaurant(
                id=str(uuid.uuid4()),
                name=name,
                address=address
            )
            self.restaurant_list.append(new_restaurant)
            self.refresh_datatable()
            self.clear_inputs()
        else:
            self.show_popup("Please provide both name and address.")    

    def update_restaurant(self, instance):
        name = self.name_input.text
        address = self.address_input.text
        if self.selected_row_index is not None and name and address:
            restaurant = self.restaurant_list[self.selected_row_index]
            restaurant.name = name
            restaurant.address = address
            self.refresh_datatable()
            self.clear_inputs()
        else:
            self.show_popup("Please provide both name and address.")    

    def delete_restaurant(self, instance):
        if self.selected_row_index is not None:
            del self.restaurant_list[self.selected_row_index]
            self.refresh_datatable()
            self.clear_inputs()
        else:
            self.show_popup("Please select a restaurant to delete.")    

    def refresh_datatable(self):
        self.restaurant_datatable.row_data = [
            (restaurant.name, restaurant.address) for restaurant in self.restaurant_list
        ]
        self.selected_row_index = None  # Reset the selected row index

    def clear_inputs(self):
        self.name_input.text = ""
        self.address_input.text = ""
        self.selected_row_index = None

    def show_popup(self, message):
        popup = Popup(title="Input Error",
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open() 


class MenuManagerContentPanel(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_provider = DataProvider()
        self.restaurant_list = self.data_provider.restaurant_list
        self.selected_restaurant = None
        self.selected_row_index = None
        self.add_widget(self.create_content_panel())

    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2, spacing=20, size_hint=(1, 1))   
        split_layout_panel.add_widget(self._create_menu_input_data_panel())
        split_layout_panel.add_widget(self._create_menu_datatable_panel())
        return split_layout_panel

    def _create_menu_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20, size_hint=(0.3, 1))

        self.menu_name_input = MDTextField(font_size="18sp", hint_text="Menu name")
        input_data_component_panel.add_widget(self.menu_name_input)
        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel
    
    def _create_buttons_component_panel(self):
        buttons_component_panel = GridLayout(cols=3, padding=0, spacing=20, size_hint=(1, None))

        add_menu_button = Button(text="Add", size_hint=(None, None), size=(100, 40), background_color=BUTTON_COLOR
)
        add_menu_button.bind(on_release=self.add_menu)
        update_menu_button = Button(text="Update", size_hint=(None, None), size=(100, 40), background_color=BUTTON_COLOR
)
        update_menu_button.bind(on_release=self.update_menu)
        delete_menu_button = Button(text="Delete", size_hint=(None, None), size=(100, 40), background_color=BUTTON_COLOR
)
        delete_menu_button.bind(on_release=self.delete_menu)

        buttons_component_panel.add_widget(add_menu_button)
        buttons_component_panel.add_widget(update_menu_button)
        buttons_component_panel.add_widget(delete_menu_button)
        
        return buttons_component_panel
    
    def _create_menu_datatable_panel(self):
        menu_datatable_panel = GridLayout(cols=1, padding=30, spacing=20, size_hint=(0.7, 1))
        menu_datatable_panel.add_widget(self._create_restaurant_spinner())
        menu_datatable_panel.add_widget(self._create_menu_datatable())
        return menu_datatable_panel

    def _create_restaurant_spinner(self):
        restaurant_spinner_layout = GridLayout(cols=1, padding=30, spacing=20, size_hint=(1, None))

        restaurant_selection_label = Label(text="Restaurant Selection", bold=True, font_size="16sp")
        restaurant_spinner_layout.add_widget(restaurant_selection_label)

        self.restaurant_spinner = Spinner(
            text='Select a Restaurant',
            values=[restaurant.name for restaurant in self.restaurant_list],
            size_hint=(None, None),
            size=(200, 44)
        )
        self.restaurant_spinner.bind(text=self.on_restaurant_select)
        restaurant_spinner_layout.add_widget(self.restaurant_spinner)
        return restaurant_spinner_layout

    def on_restaurant_select(self, spinner, text):
        for restaurant in self.restaurant_list:
            if restaurant.name == text:
                self.selected_restaurant = restaurant
                self.refresh_menu_datatable()
                break

    def _create_menu_datatable(self):
        self.menu_datatable_row_data = []

        self.menu_datatable = MDDataTable(
            size_hint=(1, 0.6),
            background_color_header="a733095",
            background_color_cell="aFFFFFF",
            background_color_selected_cell="a733095",
            use_pagination=True,
            rows_num=5,
            column_data=[
                ("Menu Name", dp(100)),
            ],
            row_data=self.menu_datatable_row_data
        )

        self.menu_datatable.bind(on_row_press=self.on_menu_row_press)

        return self.menu_datatable

    def on_menu_row_press(self, instance_table, instance_row):
        try:
            # Get the selected row index
            row_index = instance_row.index // len(instance_table.column_data)
            # Access the selected row data
            selected_row = instance_table.row_data[row_index]
            self.menu_name_input.text = selected_row[0]
            self.selected_row_index = row_index  # Update the selected row index
        except Exception as e:
            self.show_popup(f"Error selecting row: {e}")

    def add_menu(self, instance):
        if self.selected_restaurant:
            menu_name = self.menu_name_input.text
            if menu_name:
                new_menu = Menu(
                    id=str(uuid.uuid4()),
                    menu_name=menu_name
                )
                self.selected_restaurant.add_menu(new_menu)
                self.refresh_menu_datatable()
                self.clear_inputs()
            else:
                self.show_popup("Please provide a menu name.")    

    def update_menu(self, instance):
        if self.selected_restaurant and self.selected_row_index is not None:
            menu_name = self.menu_name_input.text
            if menu_name:
                menu_id = self.selected_restaurant.menu_list[self.selected_row_index].id
                self.selected_restaurant.update_menu(menu_id, menu_name)
                self.refresh_menu_datatable()
                self.clear_inputs()
            else:
                self.show_popup("Please provide a menu name.")    

    def delete_menu(self, instance):
        try:
            if self.selected_restaurant and self.selected_row_index is not None:
                menu_id = self.selected_restaurant.menu_list[self.selected_row_index].id
                self.selected_restaurant.delete_menu(menu_id)
                self.refresh_menu_datatable()
                self.clear_inputs()
                self.selected_row_index = None  # Reset the selected row index after deletion
            else:
                self.show_popup("Please select a menu to delete.")
        except Exception as e:
            self.show_popup(f"Error deleting menu: {e}")

    def refresh_menu_datatable(self):
        if self.selected_restaurant:
            self.menu_datatable_row_data = [
                (menu.menu_name,) for menu in self.selected_restaurant.menu_list
            ]
            self.menu_datatable.row_data = self.menu_datatable_row_data
            self.selected_row_index = None  # Reset the selected row index

    def clear_inputs(self):
        self.menu_name_input.text = ""
        self.selected_row_index = None

    def show_popup(self, message):
        popup = Popup(title="Input Error",
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()



class MenuItemManagerContentPanel(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_provider = DataProvider()
        self.restaurant_list = self.data_provider.restaurant_list
        self.selected_restaurant = None
        self.selected_menu = None
        self.selected_row_index = None
        self.add_widget(self.create_content_panel())

    def create_content_panel(self):
        layout = GridLayout(cols=2, spacing=20)
        layout.add_widget(self._create_menu_item_input_data_panel())
        layout.add_widget(self._create_menu_item_datatable_panel())
        return layout

    def _create_menu_item_input_data_panel(self):
        panel = GridLayout(cols=1, padding=30, spacing=20, size_hint=(0.3, 1))

        self.menu_id_input = TextInput(hint_text="Item ID", font_size="14sp", size_hint_y=None, height=35)
        self.menu_name_input = TextInput(hint_text="Item Name", font_size="14sp", size_hint_y=None, height=35)
        self.menu_price_input = TextInput(hint_text="Item Price", font_size="14sp", size_hint_y=None, height=35)

        panel.add_widget(self.menu_id_input)
        panel.add_widget(self.menu_name_input)
        panel.add_widget(self.menu_price_input)
        panel.add_widget(self._create_type_layout())
        panel.add_widget(self._create_buttons_component_panel())

        return panel

    def _create_type_layout(self):
        layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=40)

        self.meal_checkbox = CheckBox(group='type')
        self.drink_checkbox = CheckBox(group='type')

        meal_label = Label(text='Meal', color=(0, 0, 0, 1), font_size='14sp')
        drink_label = Label(text='Drink', color=(0, 0, 0, 1), font_size='14sp')

        layout.add_widget(self.meal_checkbox)
        layout.add_widget(meal_label)
        layout.add_widget(self.drink_checkbox)
        layout.add_widget(drink_label)

        return layout
    def _create_buttons_component_panel(self):
        layout = GridLayout(cols=3, spacing=10, size_hint=(1, None), height=50)

        add_btn = Button(text="Add", on_release=self.add_menu, background_color= BUTTON_COLOR)
        update_btn = Button(text="Update", on_release=self.update_menu, background_color= BUTTON_COLOR)
        delete_btn = Button(text="Delete", on_release=self.delete_menu, background_color= BUTTON_COLOR)

        layout.add_widget(add_btn)
        layout.add_widget(update_btn)
        layout.add_widget(delete_btn)

        return layout

    def _create_menu_item_datatable_panel(self):
        panel = GridLayout(cols=1, spacing=20, padding=30, size_hint=(0.7, 1))
        panel.add_widget(self._create_restaurant_spinner())
        panel.add_widget(self._create_menu_spinner())
        panel.add_widget(self._create_menu_item_datatable())
        return panel

    def _create_restaurant_spinner(self):
        layout = GridLayout(cols=1, spacing=10, size_hint=(1, None), height=100)
        layout.add_widget(Label(text="Restaurant Selection", color=(0, 0, 0, 1),font_size="16sp"))

        self.restaurant_spinner = Spinner(
            text='Select a Restaurant',
            values=[r.name for r in self.restaurant_list],
            size_hint=(1, None),
            height=44
        )
        self.restaurant_spinner.bind(text=self.on_restaurant_select)
        layout.add_widget(self.restaurant_spinner)
        return layout

    def _create_menu_spinner(self):
        layout = GridLayout(cols=1, spacing=10, size_hint=(1, None), height=100)
        layout.add_widget(Label(text="Menu Selection", color=(0, 0, 0, 1), font_size="16sp"))

        self.menu_spinner = Spinner(
            text='Select a Menu',
            size_hint=(1, None),
            height=44
        )
        self.menu_spinner.bind(text=self.on_menu_select)
        layout.add_widget(self.menu_spinner)
        return layout

    def _create_menu_item_datatable(self):
        self.menu_item_datatable = MDDataTable(
            size_hint=(1, 0.8),
            use_pagination=True,
            rows_num=5,
            column_data=[
                ("ID", dp(30)),
                ("Name", dp(40)),
                ("Price", dp(30)),
                ("Type", dp(30)),
            ],
            row_data=[]
        )
        self.menu_item_datatable.bind(on_row_press=self.on_menu_item_row_press)
        return self.menu_item_datatable

    def on_restaurant_select(self, spinner, text):
        self.selected_restaurant = next((r for r in self.restaurant_list if r.name == text), None)
        if self.selected_restaurant:
            self.menu_spinner.values = [m.menu_name for m in self.selected_restaurant.menu_list]

    def on_menu_select(self, spinner, text):
        self.selected_menu = next((m for m in self.selected_restaurant.menu_list if m.menu_name == text), None)
        self.refresh_menu_item_datatable()

    def on_menu_item_row_press(self, table, row):
        row_index = row.index // len(table.column_data)
        selected = table.row_data[row_index]
        self.menu_id_input.text = selected[0]
        self.menu_name_input.text = selected[1]
        self.menu_price_input.text = selected[2]
        self.meal_checkbox.active = selected[3] == 'Meal'
        self.drink_checkbox.active = selected[3] == 'Drink'
        self.selected_row_index = row_index

    def add_menu(self, instance):
        if not self.selected_menu:
            self.show_popup("Please select a menu first.")
            return

        id_ = self.menu_id_input.text.strip()
        name = self.menu_name_input.text.strip()
        price = self.menu_price_input.text.strip()
        type_ = 'Meal' if self.meal_checkbox.active else 'Drink' if self.drink_checkbox.active else None

        if id_ and name and price and type_:
            item = {"id": id_, "name": name, "price": price, "type": type_}
            self.selected_menu.add_menu_item(item)  # ✅ Now passes a single argument
            self.refresh_menu_item_datatable()
            self.clear_inputs()
        else:
            self.show_popup("Please fill in all fields.")


    def update_menu(self, instance):
        if not self.selected_menu or self.selected_row_index is None:
            self.show_popup("Please select a menu item to update.")
            return

        id_ = self.menu_id_input.text.strip()
        name = self.menu_name_input.text.strip()
        price = self.menu_price_input.text.strip()
        type_ = 'Meal' if self.meal_checkbox.active else 'Drink' if self.drink_checkbox.active else None

        if id_ and name and price and type_:
            current_item = self.selected_menu.menu_item_list[self.selected_row_index]
            self.selected_menu.update_menu_item(current_item["id"], id_, name, price, type_)
            self.refresh_menu_item_datatable()
            self.clear_inputs()
        else:
            self.show_popup("Please fill in all fields.")

    def delete_menu(self, instance):
        if not self.selected_menu or self.selected_row_index is None:
            self.show_popup("Please select a menu item to delete.")
            return

        item_id = self.selected_menu.menu_item_list[self.selected_row_index]["id"]
        self.selected_menu.delete_menu_item(item_id)
        self.refresh_menu_item_datatable()
        self.clear_inputs()

    def refresh_menu_item_datatable(self):
        if self.selected_menu:
            new_data = [(i["id"], i["name"], i["price"], i["type"]) for i in self.selected_menu.menu_item_list]
            self.menu_item_datatable.update_row_data(self.menu_item_datatable, new_data)
            self.selected_row_index = None

    def clear_inputs(self):
        self.menu_id_input.text = ""
        self.menu_name_input.text = ""
        self.menu_price_input.text = ""
        self.meal_checkbox.active = False
        self.drink_checkbox.active = False
        self.selected_row_index = None

    def show_popup(self, message):
        Popup(title="Error", content=Label(text=message), size_hint=(None, None), size=(400, 200)).open()


class TableManagerContentPanel(Widget):
    def __init__(self, restaurant=None, **kwargs):
        super().__init__(**kwargs)
        self.data_provider = DataProvider()

        # Default to first restaurant if none is passed
        if restaurant is None:
            if not self.data_provider.restaurant_list:
                raise ValueError("No restaurants found in data provider.")
            restaurant = self.data_provider.restaurant_list[0]

        self.restaurant = restaurant
        self.table_list = self.restaurant.table_list
        self.selected_row_index = None
        self.add_widget(self.create_content_panel())

    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2, spacing=20, size_hint=(1, 1))   
        split_layout_panel.add_widget(self._create_table_input_data_panel())
        split_layout_panel.add_widget(self._create_table_datatable_panel())
        return split_layout_panel

    def _create_table_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20, size_hint=(0.3, 1))

        self.seats_input = MDTextField(font_size="18sp", hint_text="Seats")
        input_data_component_panel.add_widget(self.seats_input)

        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel

    def _create_buttons_component_panel(self):
        buttons_component_panel = GridLayout(cols=3, padding=0, spacing=20, size_hint=(1, None))

        add_button = Button(text="Add", size_hint=(None, None), size=(100, 40), background_color=BUTTON_COLOR
)
        add_button.bind(on_release=self.add_table)

        update_button = Button(text="Update", size_hint=(None, None), size=(100, 40), background_color=BUTTON_COLOR
)
        update_button.bind(on_release=self.update_table)

        delete_button = Button(text="Delete", size_hint=(None, None), size=(100, 40), background_color=BUTTON_COLOR
)
        delete_button.bind(on_release=self.delete_table)

        buttons_component_panel.add_widget(add_button)
        buttons_component_panel.add_widget(update_button)
        buttons_component_panel.add_widget(delete_button)

        return buttons_component_panel

    def _create_table_datatable_panel(self):
        datatable_panel = GridLayout(cols=1, padding=30, spacing=20, size_hint=(0.7, 1))
        datatable_panel.add_widget(self._create_table_datatable())
        return datatable_panel

    def _create_table_datatable(self):
        table_datatable_row_data = [
            (str(i + 1), str(table.seats)) for i, table in enumerate(self.table_list)
        ]

        self.table_datatable = MDDataTable(
            size_hint=(1, 0.85),
            background_color_header="a733095",
            background_color_cell="aFFFFFF",
            background_color_selected_cell="a733095",
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Table #", dp(30)),  # New label
                ("Seats", dp(50)),
            ],
            row_data=table_datatable_row_data
        )

        self.table_datatable.bind(on_row_press=self.on_row_press)
        return self.table_datatable


    def on_row_press(self, instance_table, instance_row):
        try:
            selected_row_data = instance_row.text  # Text of the first cell in the row (Table #)
            table_number = int(selected_row_data) - 1  # Table # starts from 1, list index starts from 0

            if 0 <= table_number < len(self.table_list):
                selected_table = self.table_list[table_number]
                self.seats_input.text = str(selected_table.seats)
                self.selected_row_index = table_number
            else:
                self.show_popup("Selected row is out of bounds.")
        except Exception as e:
            logging.error(f"Error selecting row: {e}")
            self.show_popup("Failed to select table.")


    def add_table(self, instance):
        seats = self.seats_input.text
        if seats:
            try:
                seats = int(seats)
                new_table = Table(
                    table_id=str(uuid.uuid4()),
                    seats=seats
                )
                self.table_list.append(new_table)
                self.refresh_datatable()
                self.clear_inputs()
            except ValueError:
                self.show_popup("Seats must be a number.")
        else:
            self.show_popup("Please provide the number of seats.")

    def update_table(self, instance):
        seats = self.seats_input.text
        if self.selected_row_index is not None and seats:
            try:
                seats = int(seats)
                table = self.table_list[self.selected_row_index]
                table.seats = seats
                self.refresh_datatable()
                self.clear_inputs()
            except ValueError:
                self.show_popup("Seats must be a number.")
        else:
            self.show_popup("Please select a table and provide the number of seats.")

    def delete_table(self, instance):
        if self.selected_row_index is not None:
            del self.table_list[self.selected_row_index]
            self.refresh_datatable()
            self.clear_inputs()
        else:
            self.show_popup("Please select a table to delete.")

    def refresh_datatable(self):
        self.table_datatable.row_data = [
            (str(i + 1), str(table.seats)) for i, table in enumerate(self.table_list)
        ]
        self.selected_row_index = None

    def clear_inputs(self):
        self.seats_input.text = ""
        self.selected_row_index = None

    def show_popup(self, message):
        popup = Popup(title="Input Error",
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()
