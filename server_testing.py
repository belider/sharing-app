import requests
import json

def test_search_request():
    # url = "http://localhost:8080/search"
    url = "https://sharing-app-production.up.railway.app/search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer JH45ksGfwMZ78swf32fdsbawer35wsxd9SFB32sdQWsdn23SdwsfwsdF32f"  # Добавляем API ключ
    }

    # Текст для поиска
    search_query = "Какие у меня сейчас челленджы на работе?"

    # Тело запроса
    data = {
        "search_query": search_query
    }

    try:
        # Отправляем POST-запрос
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Проверяем статус-код ответа
        if response.status_code == 200:
            print("Результаты поиска:")
            print(response.json())
        elif response.status_code == 404:
            print("Результаты не найдены или произошла ошибка.")
        else:
            print(f"Произошла ошибка: {response.status_code}")
            print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

def test_accept_shared_folder():
    url = "http://localhost:8080/accept_shared_folder"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer JH45ksGfwMZ78swf32fdsbawer35wsxd9SFB32sdQWsdn23SdwsfwsdF32f"  # Добавляем API ключ
    }

    # Тестовая ссылка на shared папку
    # test_url = "https://www.icloud.com/notes/0abDz6qO8xq1frYxdIlW5uUaA"
    test_url = "https://www.icloud.com/notes/0bfB8DeYxtn1mOo0pJ8NDjNtQ"

    # Тело запроса
    data = {
        "url": test_url
    }

    try:
        # Отправляем POST-запрос
        response = requests.post(url, headers=headers, json=data)

        # Проверяем статус-код ответа
        if response.status_code == 200:
            print("Успешно принято приглашение в shared папку:")
            print(response.json())
        else:
            print(f"Произошла ошибка: {response.status_code}")
            print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")

# if __name__ == "__main__":
#     test_search_request()

if __name__ == "__main__":
    # print("\n--- Тестирование принятия приглашения в shared папку ---")
    # test_accept_shared_folder()
    
    print("\n--- Тестирование поиска с Bearer авторизацией ---")
    test_search_request()