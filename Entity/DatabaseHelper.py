import json
import sqlite3
import os
from Entity.NetworkService import UNOGSRequestProtocol


class DatabaseHelper:
	@staticmethod
	def open_json_file():
		request_network_service = UNOGSRequestProtocol()
		data = request_network_service.get_data()
		return data

	@staticmethod
	def connect_to_database():
		base_dir = os.path.dirname(os.path.abspath(__file__))
		db_path = os.path.join(base_dir, 'MovieDatabaseApp-2.0.db')
		conn = sqlite3.connect(db_path)
		cursor = conn.cursor()
		cursor.execute(
			'''CREATE TABLE IF NOT EXISTS movies ( 
			kinopoiskId TEXT,
			imdbId TEXT,
			nameRu TEXT,
			nameEn TEXT,
			nameOriginal TEXT,
			countries TEXT,
			genres TEXT,
			ratingKinopoisk TEXT,
			ratingImdb TEXT,
			year INTEGER,
			type TEXT,
			posterUrl TEXT,
			posterUrlPreview TEXT,
			coverUrl TEXT,
			logoUrl TEXT,
			description TEXT,
			ratingAgeLimits TEXT )''')

		return conn, cursor

	def write_to_database(data, conn, cursor):
		def create_unique_index(cursor):
			cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_kinopoisk_id ON movies (kinopoiskId)')

		# Подключаемся к базе данных SQLite
		conn, cursor = DatabaseHelper.connect_to_database()

		# Создаем уникальный индекс для столбца kinopoiskId
		create_unique_index(cursor)

		# Получаем список kinopoiskId всех фильмов из базы данных
		cursor.execute("SELECT kinopoiskId FROM movies")

		for item in data['items']:
			kinopoiskId = item.get('kinopoiskId')
			imdbId = item.get('imdbId')
			nameRu = item.get('nameRu')
			nameEn = item.get('nameEn')
			nameOriginal = item.get('nameOriginal')
			countries = ', '.join([country['country'] for country in item.get('countries', [])])
			genres = ', '.join([genre['genre'] for genre in item.get('genres', [])])
			ratingKinopoisk = item.get('ratingKinopoisk')
			ratingImdb = item.get('ratingImdb')
			year = item.get('year')
			type = item.get('type')
			posterUrl = item.get('posterUrl')
			posterUrlPreview = item.get('posterUrlPreview')
			coverUrl = item.get('coverUrl')
			logoUrl = item.get('logoUrl')
			description = item.get('description')
			ratingAgeLimits = item.get('ratingAgeLimits')

			cursor.execute('''INSERT OR IGNORE INTO movies (
						kinopoiskId, imdbId, nameRu, nameEn, nameOriginal, countries, genres, 
	                    ratingKinopoisk, ratingImdb, year, type, posterUrl, posterUrlPreview, 
	                    coverUrl, logoUrl, description, ratingAgeLimits) 
	                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
			(kinopoiskId, imdbId, nameRu, nameEn, nameOriginal, countries, genres,
				        ratingKinopoisk, ratingImdb, year, type, posterUrl, posterUrlPreview,
				        coverUrl, logoUrl, description, ratingAgeLimits
			            ))

		conn.commit()
		conn.close()
