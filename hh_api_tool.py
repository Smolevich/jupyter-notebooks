import os
import json
import requests
import sys

def load_config():
    """Load configuration from config.json"""
    config_path = 'config.json'
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def get_api_headers():
    config = load_config()
    if not config:
        return None
    token = config.get('app_token')
    email = config.get('user_email', 'test@example.com')
    if not token:
        print("Error: app_token missing in config.json")
        return None
    return {
        'Authorization': f'Bearer {token}',
        'User-Agent': f'HH-User-Agent ({email})'
    }

def save_json(data, filename):
    """Save data to data/hh_api_data directory"""
    os.makedirs('data/hh_api_data', exist_ok=True)
    path = os.path.join('data/hh_api_data', filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Ответ сохранен в: {path}")

def get_vacancy_details(vacancy_id):
    headers = get_api_headers()
    if not headers: return
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=4, ensure_ascii=False))
            if input("\nСохранить ответ в файл? (y/n): ").lower() == 'y':
                save_json(data, f"vacancy_{vacancy_id}.json")
        else:
            print(f"Error: {response.status_code}\n{response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_employer_details(employer_id):
    headers = get_api_headers()
    if not headers: return
    url = f"https://api.hh.ru/employers/{employer_id}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=4, ensure_ascii=False))
            if input("\nСохранить ответ в файл? (y/n): ").lower() == 'y':
                save_json(data, f"employer_{employer_id}_details.json")
        else:
            print(f"Error: {response.status_code}\n{response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

def interactive_mode():
    actions = {
        '1': ("Введите ID вакансии: ", get_vacancy_details),
        '2': ("Введите ID работодателя: ", get_employer_details),
        '0': (None, lambda _: sys.exit(0))
    }

    print("\n--- HH API Search Tool ---")
    print("1. Детализация вакансии по ID")
    print("2. Детализация работодателя по ID")
    print("0. Выход")
    
    choice = input("\nВыберите режим: ").strip()
    
    if choice in actions:
        prompt, func = actions[choice]
        val = input(prompt).strip() if prompt else None
        func(val) if val or not prompt else None
    else:
        print("Некорректный выбор")

if __name__ == "__main__":
    if sys.stdin.isatty():
        interactive_mode()
    else:
        # Если запущен не в TTY (например, через pipe), выводим ошибку
        print("Ошибка: Скрипт предназначен для интерактивного использования в терминале.")
        sys.exit(1)
