import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clean_price(price):
    # Удаляем "руб." и преобразуем в число
    return int(price.replace('руб.', '').replace(' ', ''))


# Параметры нормального распределения
mean = 0  # Среднее значение
std_dev = 1  # Стандартное отклонение
num_samples = 1000  # Количество образцов

# Генерация случайных чисел, распределенных по нормальному распределению
data = np.random.normal(mean, std_dev, num_samples)

# Построение гистограммы
plt.figure(figsize=(10, 5))
plt.hist(data, bins=30, color='blue', edgecolor='black', alpha=0.7)
plt.title('Гистограмма для нормального распределения')
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.grid(True)
plt.show()

# Генерация двух наборов случайных данных для диаграммы рассеяния
x_data = np.random.rand(100)  # Набор X
y_data = np.random.rand(100)  # Набор Y

# Построение диаграммы рассеяния
plt.figure(figsize=(10, 5))
plt.scatter(x_data, y_data, color='green', alpha=0.5, edgecolor='black')
plt.title('Диаграмма рассеяния')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()

# Настройка WebDriver
driver = webdriver.Chrome()
for i in range(42):
    url = "https://www.divan.ru/petrozavodsk/category/divany-i-kresla/page-"+str(i+1)
    driver.get(url)

    time.sleep(3)

    # Сбор данных
    parsed_data = []

    goods = driver.find_elements(By.CSS_SELECTOR, 'div.WdR1o')
    for good in goods:
        try:
            # Извлечение цены
            price_element = good.find_element(By.CSS_SELECTOR, 'span.KIkOH')
            price = price_element.text.strip() if price_element.text else ""

            # Добавление в список
            parsed_data.append([price])

        except:
            continue

# Завершение работы WebDriver
driver.quit()

# Сохранение данных в CSV
with open("divan.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['Price'])
    writer.writerows(parsed_data)

# Чтение данных из исходного CSV файла и их обработка
input_file = 'divan.csv'
output_file = 'cleaned_divan.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='',
                                                                  encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Читаем заголовок и записываем его в новый файл
    header = next(reader)
    writer.writerow(header)

    # Обрабатываем и записываем данные строк
    for row in reader:
        clean_row = [clean_price(row[0])]
        writer.writerow(clean_row)

print(f"Обработанные данные сохранены в файл {output_file}")

# Загрузка данных из CSV-файла
file_path = 'cleaned_divan.csv'
data = pd.read_csv(file_path)

# Предположим, что столбец с ценами называется 'price'
prices = data['Price']

average_price = int(prices.mean())

# Построение гистограммы
plt.hist(prices, bins=10, edgecolor='black')

# Добавление заголовка и меток осей
plt.title('Гистограмма цен на диваны. Средняя цена: '+str(average_price)+' руб.')
plt.xlabel('Цена')
plt.ylabel('Частота')

# Показать гистограмму
plt.show()