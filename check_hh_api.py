import requests
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'token.json')

def check_hh_api():
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Ошибка при загрузке {CONFIG_PATH}: {e}")
        return

    token = config.get('app_token')
    email = config.get('user_email', 'test@example.com')
    
    if not token:
        print("❌ 'app_token' отсутствует в config.json")
        return

    print(f"--- Проверка HH API ({datetime.now().strftime('%H:%M:%S')}) ---")
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': f'HH-User-Agent ({email})'
    }

    try:
        resp = requests.get('https://api.hh.ru/me', headers=headers)
        if resp.status_code == 200:
            user = resp.json()
            auth_type = user.get('auth_type', 'unknown')
            is_app = user.get('is_application', False)
            print(f"✅ Авторизация ОК! Тип: {auth_type} (Приложение: {is_app})")
            
            print("\n--- Проверка прав доступа (Scopes) ---")
            
            tests = [
                ("Поиск вакансий", "https://api.hh.ru/vacancies?text=Python&per_page=1"),
                ("Поиск резюме", "https://api.hh.ru/resumes?text=Python&per_page=1"),
                ("Доступ к справочникам", "https://api.hh.ru/dictionaries"),
                ("Доступ к откликам", "https://api.hh.ru/negotiations"),
                ("Поиск работодателей", "https://api.hh.ru/employers?text=Yandex&per_page=1")
            ]
            
            for name, url in tests:
                t_resp = requests.get(url, headers=headers)
                status = "✅ ДОСТУПНО" if t_resp.status_code == 200 else f"❌ НЕТ ДОСТУПА ({t_resp.status_code})"
                print(f"- {name:25}: {status}")

            print("\n💡 Примечание: client_credentials (токен приложения) обычно дает доступ только к публичным данным (вакансии, справочники).")
        else:
            print(f"❌ Ошибка авторизации ({resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

if __name__ == "__main__":
    check_hh_api()
