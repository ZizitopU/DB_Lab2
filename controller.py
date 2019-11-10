import utils as utils


class Controller(object):

    # Very strange and not typical code
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start(self):
        self.view.print_hello_message()
        self.show_main_menu()

    # Main menu handler
    def show_main_menu(self):
        self.view.print_start_menu()

        input_v = self.view.request_input("Enter number (from 1 to 4)",
                                          valid_cases=['1', '2', '3', '4'])

        if input_v == "1":
            self.print_tables()
            self.show_main_menu()

        if input_v == "2":
            sql_query = self.view.request_input("Enter query:")
            print(self.model.query(sql_query))
            self.show_main_menu()
        #
        # if input == "3":
        #     string = self.view.request_input("String to find: ")
        #     self.model.find_no_string_in_all_tables(string)

        if input_v == "4":
            utils.do_nothing()

        if input_v == "back":
            utils.do_nothing()
            self.show_main_menu()

    # handler меню таблиць
    def print_tables(self):
        tables = self.model.list_tables()
        self.view.print_tables(tables)
        input_v = self.view.request_input("Enter number (from 1 to " + str(len(tables)) + "):",
                                          validator=lambda x: x.isdigit() and 0 < int(x) <= len(tables))
        if input_v == "back":
            return None
        self.table_menu(tables[int(input_v)-1])

    def select_obj_menu(self):
        column = self.view.request_input("\tEnter field to check:")
        if column != "back" and column != "":
            expected_value = self.view.request_input("\tEnter expected value on this field:")
            if expected_value != "back":
                return column, expected_value
        return None, None

    def table_menu(self, table_name):
        self.view.print_table_menu(table_name)
        input_v = self.view.request_input("Enter number (from 1 to 7):",
                                          valid_cases=["1", "2", "3", "4", "5", "6"])

        if input_v != "back":
            # SELECT ALL
            if input_v == "1":
                data = self.model.get_full_table(table_name)
                self.view.print_table(data)
                self.view.after_action_message(data)
                self.table_menu(table_name)

            # DELETE
            if input_v == "2":
                column, value = self.select_obj_menu()
                if column and value:
                    self.view.after_action_message(self.model.delete_data(table_name, column, value))
                self.table_menu(table_name)

            # INSERT
            if input_v == "3":
                def insert():
                    data_list = []
                    print("You can enter nothing for random value.")
                    for column_data in self.model.get_table_columns_data(table_name):
                        data = self.view.request_input("\tField '" + column_data[0] + "'(" + column_data[1] + "):")
                        if data == 'back':
                            return
                        elif data == '':
                            data_list.append(utils.gen_random(column_data[1]))
                        else:
                            data_list.append(data)

                    self.view.after_action_message(self.model.insert_data(table_name, tuple(data_list)))
                insert()
                self.table_menu(table_name)

            # # UPDATE
            # if input_v == "4":
            #     self.update_menu(table_name)
            #     self.view.print_divider(2)
            #     self.table_controller(table_name)
            #
            # SELECT
            if input_v == "5":
                column, value = self.select_obj_menu()
                if column and value:
                    data = self.model.select_some(table_name, column, value)
                    self.view.print_table(data, on_none_message="NOTHING FOUND")
                    self.view.after_action_message(data)
                self.table_menu(table_name)

            # INSERT RANDOM
            if input_v == "6":
                self.view.after_action_message(self.model.insert_random(table_name))
                self.table_menu(table_name)

    # update handler для таблиці
    def update_menu(self, table_name):
        def_obj = self.model.get_object(table_name)
        self.view.print_message("Object to update:")
        obj = self.view.request_input_object(def_obj, True)
        object_to_find = get_formatted_object(obj)
        print("#Need to update: " + str(object_to_find))
        print("Def obj: " + str(def_obj))
        new_object = self.view.request_input_object(def_obj)
        print(new_object)
        new_object = get_formatted_object(new_object)
        print(str(new_object))
        self.model.update_item(table_name, object_to_find, new_object)
