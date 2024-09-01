import requests
import json

def test_search_request():
    url = "http://localhost:8080/search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer JH45ksGfwMZ78swf32fdsbawer35wsxd9SFB32sdQWsdn23SdwsfwsdF32f"  # Добавляем API ключ
    }

    # Текст для поиска
    search_query = "Какие самые приоритетные направления роста в Searadar?"

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

if __name__ == "__main__":
    test_search_request()