from data_provider import DataProvider

class App():

    def build(self):
        data_provider = DataProvider()
        data_provider._print_data()

App().build() 