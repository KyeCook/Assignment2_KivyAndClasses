"""
Assignment 2
Kye Cook
started 04/05/2016

GitHub URL : https://github.com/KyeCook/Assignment2_KivyAndClasses

Program uses past assignment and converts into usable GUI using classes and kivy
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import StringProperty
from itemlist import ItemList
from Assign1 import update_csv

LIST_MODE = 0
HIRE_MODE = 1
RETURN_MODE = 2


class ItemsGUI(App):

    # This status text is a label that changes dynamically depending on item selected. Default value is within __init__
    status_text = StringProperty()

    def __init__(self, **kwargs):
        """
        Initializer for app class - allows for other classes to be imported and declared
        :param kwargs:
        :return:
        """
        super(ItemsGUI, self).__init__(**kwargs)
        self.items = ItemList()
        self.mode = LIST_MODE
        self.selected_items = []
        self.status_text = "Choose action from the left menu, then select items on the right"

    def build(self):
        """
        This actually builds and constructs the GUI
        :return: self.root
        """
        self.title = "Equipment Hire"
        self.root = Builder.load_file('GUI.kv')
        self.create_item_buttons()
        return self.root

    def create_item_buttons(self):
        """
        This class function dynamically builds and constructs the buttons dependant upon how many items are within the
        CSV file
        :return:
        """
        for item in self.items.items:
            temp_button = Button(text=item.name)
            temp_button.bind(on_release=self.press_entry)
            self.root.ids.itemsBox.add_widget(temp_button)
            # The below statement changes the buttons colour to red if the items availability is 'out'
            if item.in_or_out == "out":
                temp_button.background_color = (1.0, 0.0, 0.0, 1.0)

    def update_buttons(self):
        """
        This function runs upon the selection of a menu button to both reset the state of the buttons and also to update
        the colours depending upon changes made.
        :return:
        """
        for instance in self.root.ids.itemsBox.children:
            instance.state = 'normal'
            item_name = instance.text
            item = self.items.get_item(item_name)
            if item.in_or_out == "out":
                instance.background_color = (1.0, 0.0, 0.0, 1.0)
            else:
                instance.background_color = (1.0, 1.0, 1.0, 1.0)

    def press_entry(self, instance):
        """
        This class function changes the text notification within the bottom status label
        :param instance: --> instance is derived from the 'create_item_buttons' function
        :return:
        """
        item_name = instance.text

        item = self.items.get_item(item_name)
        if self.mode == LIST_MODE:
            self.status_text = "{} ({}) = ${:.2f} is {}".format(item.name, item.description, item.cost, item.in_or_out)

        elif self.mode == HIRE_MODE:
            self.hire_mode_functionality(item, instance)

        elif self.mode == RETURN_MODE:
            self.return_mode_functionality(item, instance)

    def hire_mode_functionality(self, item, instance):
        """
        Code within this function is segregated into separate function from where it is used to increase readability and
        actually performs the workings of HIRE_MODE
        :param item:
        :param instance:
        :return:
        """
        if item.in_or_out == "in":
                if item not in self.selected_items:
                    self.selected_items.append(item)
                    instance.state = "down"

                else:
                    self.selected_items.remove(item)
                    instance.state = "normal"

                names = []
                total_cost = 0

                for item in self.selected_items:
                    total_cost += item.cost
                    names.append(item.name)

                name_str = ",".join(names)
                if name_str == '':
                    self.status_text = "Hiring : Nothing"
                else:
                    self.status_text = "Hiring : {} for ${:.2f}".format(name_str, total_cost)

    def return_mode_functionality(self, item, instance):
        """
        Code within this function is segregated into separate function from where it is used to increase readability and
        actually performs the workings RETURN_MODE
        :param item:
        :param instance:
        :return:
        """
        if item.in_or_out == "out":
                if item not in self.selected_items:
                    self.selected_items.append(item)
                    instance.state = "down"

                else:
                    self.selected_items.remove(item)
                    instance.state = "normal"

                names = []
                for item in self.selected_items:
                    names.append(item.name)

                name_str = ",".join(names)
                if name_str == '':
                    self.status_text = "Returning : Nothing"
                else:
                    self.status_text = "Returning : {}".format(name_str)

    def handle_list_items(self):
        """
        This function occurs when the 'list items' button is selected and changes button states, status texts and sets
        the mode. The list constructed for the selected items is also reset.
        :return:
        """
        self.selected_items = []
        self.status_text = "Choose action from the left menu, then select items on the right"
        self.mode = LIST_MODE
        self.root.ids.list_items_btn.state = "down"
        self.root.ids.hire_items_btn.state = "normal"
        self.root.ids.return_items_btn.state = "normal"

        self.update_buttons()

    def handle_hire_item(self):
        """
        This function occurs when the 'hire items' button is selected and changes button states, status texts and sets
        the mode. The list constructed for the selected items is also reset.
        :return:
        """
        self.selected_items = []
        self.status_text = "Select available items to hire"
        self.mode = HIRE_MODE
        self.root.ids.list_items_btn.state = "normal"
        self.root.ids.hire_items_btn.state = "down"
        self.root.ids.return_items_btn.state = "normal"

        self.update_buttons()

    def handle_return_item(self):
        """
        This function occurs when the 'return items' button is selected and changes button states, status texts and sets
        the mode. The list constructed for the selected items is also reset.
        :return:
        """
        self.selected_items = []
        self.status_text = "Select available items to return"
        self.mode = RETURN_MODE
        self.root.ids.list_items_btn.state = "normal"
        self.root.ids.hire_items_btn.state = "normal"
        self.root.ids.return_items_btn.state = "down"

        self.update_buttons()

    def handle_confirm(self):
        """
        This function runs when the 'confirm' button is selected and changes items and button states according to
        current mode the user is in (HIRE_MODE or RETURN_MODE). The mode is then reset back to the default LIST_MODE
        :return:
        """
        self.root.ids.list_items_btn.state = "normal"
        self.root.ids.hire_items_btn.state = "normal"
        self.root.ids.return_items_btn.state = "normal"

        for item in self.selected_items:
            if self.mode == HIRE_MODE:
                item.in_or_out = "out"
            elif self.mode == RETURN_MODE:
                item.in_or_out = "in"
        self.mode = LIST_MODE

        self.update_buttons()

    def handle_add_item(self):
        """
        This opens the popup for add items
        :return:
        """
        self.root.ids.popup.open()

    def handle_save_item(self):
        """
        Function allows for added items to be appended to the already constructed items list.
        :return:
        """
        # Gets item information from kv file
        added_name = self.root.ids.added_name.text
        added_description = self.root.ids.added_description.text
        added_price = self.root.ids.added_price.text

        # Adds in error checking --> Try statement checks if numeric value is entered into item cost
        try:
            # Further error checking --> While checks values aren't NULL and that item cost > 0
            # N.B attempted to add price > $0 into own error checking loop but repeatedly crashed GUI so left as is
            while added_name != "" and added_description != "" and float(added_price) > 0:
                # Adds information found within kv file to function within itemlist
                self.items.add_item_from_values(added_name, added_description, added_price)
                temp_button = Button(text=added_name)
                temp_button.bind(on_release=self.press_entry)
                self.root.ids.itemsBox.add_widget(temp_button)
                # closes popup
                self.root.ids.popup.dismiss()
                self.clear_fields()

            # Updates the popups status text with error message, also changes colour to red to let show that it is error
            self.root.ids.popup_status_text.text = "ITEM INPUT CAN NOT BE NULL AND ITEM COST MUST BE > $0"
            self.root.ids.popup_status_text.color = (1.0, 0.0, 0.0, 1.0)

        except ValueError:
            self.root.ids.popup_status_text.text = "ITEM COST MUST BE NUMERIC"
            self.root.ids.popup_status_text.color = (1.0, 0.0, 0.0, 1.0)

    def clear_fields(self):
        """
        This clears inputted data from add group if cancel button is clicked.
        :return:
        """
        self.root.ids.added_name.text = ""
        self.root.ids.added_description.text = ""
        self.root.ids.added_price.text = ""

    def handle_cancel(self):
        """
        This handles the actions of the cancel button within the add group
        :return: none
        """
        # closes the popup window
        self.root.ids.popup.dismiss()
        self.clear_fields()

    def on_stop(self):
        """
        This function uses kivy method to activate upon closing of GUI. Actual function will return and export to csv
        :return:
        """
        items_to_save = self.items.get_items_for_saving()

        # calls previous assignments csv updating function
        update_csv(items_to_save)

ItemsGUI().run()
