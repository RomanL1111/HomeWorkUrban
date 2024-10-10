import requests

response = requests.get('https://api.github.com')

if response.status_code == 200:
    print("Успешное подключение!")
    print("Ответ в формате JSON:", response.json())
else:
    print(f"Ошибка: {response.status_code}")






import pandas as pd

data = pd.read_csv('data.csv')

grouped_data = data.groupby('Category').sum()

filtered_data = data[data['Value'] > 10]

print(grouped_data)
print(filtered_data)






import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 35]

plt.plot(x, y, label="Линейный график")

plt.title("Пример графика")
plt.xlabel("Ось X")
plt.ylabel("Ось Y")


plt.legend()
plt.show()
