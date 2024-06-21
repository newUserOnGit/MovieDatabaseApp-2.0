from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from Entity.NetworkService import UNOGSRequestProtocol
from Entity.DatabaseHelper import DatabaseHelper


class CustomScrollView(ScrollView):
	scroll_y_pos = NumericProperty(1.0)

	def __init__(self, **kwargs):
		super(CustomScrollView, self).__init__(**kwargs)
		self.bind(scroll_y=self.on_scroll_y)

	def on_scroll_y(self, instance, value):
		self.scroll_y_pos = value


class DataTable(GridLayout):
	def __init__(self, data, **kwargs):
		super(DataTable, self).__init__(**kwargs)
		self.cols = 1
		self.spacing = 10  # Расстояние между записями
		self.size_hint_y = None  # Разрешаем изменение высоты
		self.bind(minimum_height=self.setter('height'))

		for item in data:
			item_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=300)
			self.add_widget(item_layout)

			title = Label(text=item[1] if item[1] is not None else '', halign='center', font_size='20sp',
			              size_hint=(None, None), size=(300, 50))
			item_layout.add_widget(title)

			image_url = item[2] if item[2] is not None else ''
			image = AsyncImage(source=image_url, size_hint=(None, None), size=(300, 200), pos_hint={'center_x': 0.5})
			item_layout.add_widget(image)

			description = Label(text=item[3] if item[3] is not None else '', halign='center', font_size='15sp',
			                    size_hint=(None, None), size=(300, 50))
			item_layout.add_widget(description)


class MainApp(App):
	def build(self):
		unogs_protocol = UNOGSRequestProtocol()
		data = unogs_protocol.get_data()
		conn, cursor = DatabaseHelper.connect_to_database()
		DatabaseHelper.write_to_database(data, conn, cursor)
		cursor.execute("SELECT kinopoiskId, nameRu, posterUrl, description FROM movies")
		data_from_db = cursor.fetchall()
		data_table = DataTable(data=data_from_db)

		scroll_view = CustomScrollView()
		scroll_view.add_widget(data_table)
		scroll_view.scroll_y = 1.0  # Перемещаем скролл вниз

		return scroll_view


if __name__ == '__main__':
	MainApp().run()