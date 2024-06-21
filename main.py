from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from Entity.NetworkService import UNOGSRequestProtocol
from Entity.DatabaseHelper import DatabaseHelper


class DataTable(GridLayout):
    def __init__(self, data, **kwargs):
        super(DataTable, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(MDLabel(text='Kinopoisk ID'))
        self.add_widget(MDLabel(text='Title'))
        for item in data:
            self.add_widget(MDLabel(text=str(item[0]))) # Извлекаем данные из кортежа по индексу
            self.add_widget(MDLabel(text=item[1]))  # Извлекаем данные из кортежа по индексу


class MainApp(MDApp):
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Orange"

		# Получаем данные с помощью UNOGSRequestProtocol
		unogs_protocol = UNOGSRequestProtocol()
		data = unogs_protocol.get_data()

		# Подключаемся к базе данных SQLite
		conn, cursor = DatabaseHelper.connect_to_database()

		# Записываем данные в базу данных
		DatabaseHelper.write_to_database(data, conn, cursor)

		# Читаем данные из базы данных
		cursor.execute("SELECT kinopoiskId, nameRu FROM movies")
		data_from_db = cursor.fetchall()
		data_table = DataTable(data=data_from_db)

		scroll_view = ScrollView()
		scroll_view.add_widget(data_table)
		
		return scroll_view


MainApp().run()