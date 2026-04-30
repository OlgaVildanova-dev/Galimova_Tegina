import unittest
import json
import os
from unittest.mock import patch, MagicMock
import main  # Предполагается, что основной код приложения находится в main.py

# Путь к файлу избранных пользователей
FAVORITES_FILE = 'favorites.json'

class TestGitHubUserFinder(unittest.TestCase):

    def setUp(self):
        """Подготовка перед каждым тестом: удаление файла избранных, если он есть."""
        if os.path.exists(FAVORITES_FILE):
            os.remove(FAVORITES_FILE)

    def tearDown(self):
        """Очистка после теста."""
        self.setUp() # Повторная очистка на случай, если setUp не сработал

    # --- Тесты валидации ввода ---
    def test_empty_search_input(self):
        """Тест: поиск с пустым полем ввода должен вернуть ошибку."""
        result = main.search_user("")
        self.assertEqual(result, "Ошибка: Поле не должно быть пустым!")

    # --- Тесты работы с API (с использованием mock) ---
    @patch('main.requests.get')
    def test_search_existing_user(self, mock_get):
        """Тест: успешный поиск существующего пользователя."""
        # Настраиваем мок-ответ от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'login': 'torvalds',
            'name': 'Linus Torvalds',
            'avatar_url': 'https://avatars.githubusercontent.com/u/1024025'
        }
        mock_get.return_value = mock_response

        result = main.search_user("torvalds")
        self.assertIn("Linus Torvalds", result)
        self.assertIn("torvalds", result)

    @patch('main.requests.get')
    def test_search_non_existing_user(self, mock_get):
        """Тест: поиск несуществующего пользователя должен вернуть ошибку."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = main.search_user("thisuserdoesnotexist12345")
        self.assertEqual(result, "Ошибка: Пользователь не найден!")

    # --- Тесты работы с избранным ---
    def test_add_to_favorites_and_save(self):
        """Тест: добавление пользователя в избранное и сохранение в JSON."""
        user_data = "Linus Torvalds (@torvalds)"
        
        # Добавляем в избранное
        main.add_to_favorites(user_data)
        
        # Проверяем, что файл создался
        self.assertTrue(os.path.exists(FAVORITES_FILE))
        
        # Проверяем содержимое файла
        with open(FAVORITES_FILE, 'r') as f:
            favorites = json.load(f)
            self.assertIn(user_data, favorites)

    def test_load_favorites(self):
        """Тест: загрузка избранных пользователей из JSON."""
        # Сначала создаем файл с данными
        test_data = ["User A (@a)", "User B (@b)"]
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(test_data, f)
        
        # Загружаем данные через функцию приложения
        loaded_data = main.load_favorites()
        
        self.assertEqual(loaded_data, test_data)

if __name__ == '__main__':
    unittest.main()
