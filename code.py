import os
import pandas as pd
import random
import seaborn as sb
import matplotlib.pyplot as plt

directory = "/content/"  

class DataArchive:
    def __init__(self, directory: str):
        self.files = {}
        self.load_files(directory)

    def load_files(self, directory: str):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                varname = f"file_{filename.replace('.', '_')}"
                self.files[varname] = pd.read_csv(filepath)


archive = DataArchive(directory)

plt.figure(figsize=(12, 6))
for attr_name, df in archive.files.items():
    df['Date'] = pd.to_datetime(df['Date'])  
    df = df.sort_values(by="Date")
    df.set_index("Date", inplace=True)

    plt.plot(df.index, df['Close'], label=f"{attr_name} Closing Price", 
             color=(random.random(), random.random(), random.random()))

print(df["Close"].describe())
print("Медиана:", df["Close"].median())  
print("Стандартное отклонение:", df["Close"].std())  

plt.xlabel("Дата")
plt.ylabel("Стоимость (USD)")
plt.title("Стоимость акций игроков фондового рынка")
plt.legend()
plt.grid()
plt.show()

df_prices = pd.DataFrame()
for attr_name, df in archive.files.items():
    df_prices[attr_name.split("_")[1] + " Close"] = df['Close']

plt.figure(figsize=(10, 6))
sb.heatmap(df_prices.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Корреляционная матрица Netflix Stock Data")
plt.show()

window_size = 50 

if 'NFLX Close' in df_prices.columns and 'PARA Close' in df_prices.columns:
    rolling_corr = df_prices['NFLX Close'].rolling(window=window_size).corr(df_prices['PARA Close'])

    plt.figure(figsize=(12, 6))
    plt.plot(rolling_corr, label="Rolling Correlation (NFLX vs PARA)", color="purple")
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xlabel("Дата")
    plt.ylabel("Корреляция")
    plt.title("Скользящая корреляция Netflix vs Paramount")
    plt.legend()
    plt.show()
else:
    print("NFLX или PARA данные отсутствуют в загруженных файлах.")
