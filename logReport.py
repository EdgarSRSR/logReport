"""
Программа, которая Разбирает Параметры из командной строки, получает имя файла и создает отчет логов с информацией в формате json
"""

import argparse
import json
import datetime
from tabulate import tabulate

# Настройка парсер параметров командной строки
def parse_args():
    parser = argparse.ArgumentParser(prog = 'logReport', description ='Отчет лог файлов')
    parser.add_argument('--file', nargs = '+')
    parser.add_argument('--report')
    parser.add_argument('--date')
    return parser.parse_args()


# формирует отчет со списком эндпоинтов, количеством запросов по каждому эндпоинту и средним временем ответа
def process_logs(files, date_filter=None):
    logs = []
    url_info = []

    # извлекает логи из файла и сохраняет их в переменной logs
    for file_Log in files:
        with open(file_Log, 'r') as file:
            for element in file:
                try:
                    json_log = json.loads(element.strip())
                    logs.append(json_log)
                except json.JSONDecodeError as e:
                    print(f"Ошибка в файле")
    
    log_key = "url"
    # извлекает все значения URL-адресов
    url_values = [item[log_key] for item in logs if log_key in item]

    # получает все уникальные URL-адреса
    unique_urls = set(url_values)
    # вычисляет общее количество заголовков и среднее время отклика для каждого уникального URL-адреса
    for url in unique_urls:
        inner_list = []
        total = 0
        avg_response_time = 0
        if date_filter == None:
            for item in logs:
                if item[log_key]  == url:
                    total += 1
                    avg_response_time += float(item["response_time"])
        else:
            for item in logs:
                if item[log_key]  == url and datetime.datetime.strptime(item["@timestamp"][:item["@timestamp"].find('T')],'%Y-%m-%d').strftime('%Y-%d-%m') == date_filter :
                    total += 1
                    avg_response_time += float(item["response_time"])
        inner_list.append(url)
        inner_list.append(total)
        if total == 0:
            inner_list.append(0)
        else:
            inner_list.append(round(avg_response_time/total, 3))
        url_info.append(inner_list)
    
    return url_info

def main():
    args = parse_args()
    print(args.report)
    results = process_logs(args.file, args.date)
    # выводит результаты в виде таблицы
    print(tabulate(results, headers = ["handler","total", "avg_response_time"], tablefmt="outline"))

if __name__ == '__main__':
    main()





