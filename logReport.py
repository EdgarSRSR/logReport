# program en cli que lee archivos de los y crea un resumen de cada endpoint y el tiempo promedio de uso, fecha(opcional)
# el camino al archivo y el nombre del reporte se escriben como parametros
# ejemplo de inicializacion del programa: python main.py --file file.log --report average
# los archivos vienen en formato JSON
# reporte debe se imprime en el cli como tabla
# bibliotecas sugeridas: argparse, tabulate
# argparser - para trabajar con la cli
# tabulate ayuda a organizar la informacion en tablas en el cli
# requieren testing: pytest-cov


# ya esta el MVP, pasos a sequir
# añadir git y subir a github
# testear
# subir a github

import argparse
import json
import datetime
from tabulate import tabulate

# Setup parser for command line parameters
parser = argparse.ArgumentParser(prog = 'logReport', description ='Отчет лог файлов')
parser.add_argument('--file', nargs = '+')
parser.add_argument('--report')
parser.add_argument('--date')
args = parser.parse_args()
print(args.file, args.report, args.date)

# All logs from the files are saved in logs
logs = []
url_info = []

# Extract the logs from the file and save them in logs variable
for file_Log in args.file:
    with open(file_Log, 'r') as file:
        total_lines = 0
        for element in file:
            try:
                json_log = json.loads(element.strip())
                logs.append(json_log)
                total_lines += 1 
            except json.JSONDecodeError as e:
                print(f"Ошибка в файле")

log_key = "url"
# Extract all url values
url_values = [item[log_key] for item in logs if log_key in item]

# Get all unique urls
unique_urls = set(url_values)

# check the date format
#test_date = datetime.datetime.strptime(logs[0]["@timestamp"][:logs[0]["@timestamp"].find('T')],'%Y-%m-%d').strftime('%Y-%d-%m')
#print(test_date)
#if None  == args.date:
#    print("test_date and args.date are equal .")
#else:
#    print("test_date and args.date are not equal (case-insensitive).")


# calculate total and average time response for each unique url
for url in unique_urls:
    inner_list = []
    total = 0
    avg_response_time = 0
    if args.date == None:
        #print("no date")
        for item in logs:
            if item[log_key]  == url:
                total += 1
                avg_response_time += float(item["response_time"])
    else:
        #print("date given")
        for item in logs:
            if item[log_key]  == url and datetime.datetime.strptime(item["@timestamp"][:item["@timestamp"].find('T')],'%Y-%m-%d').strftime('%Y-%d-%m') == args.date :
                total += 1
                avg_response_time += float(item["response_time"])
    inner_list.append(url)
    inner_list.append(total)
    if total == 0:
        inner_list.append(0)
    else:
        inner_list.append(round(avg_response_time/total, 3))
    url_info.append(inner_list)

# print the results into a table
print(tabulate(url_info, headers = ["handler","total", "avg_response_time"], tablefmt="outline"))






