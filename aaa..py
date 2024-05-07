import pandas as pd

# Step 1: Read the CSV file
df = pd.read_csv('Dados.csv')

# Step 2: Explore the DataFrame
# Print the first few rows of the DataFrame
#print(df.head())

# Get summary statistics of numerical columns
#print(df.describe())

# Get information about the DataFrame
#print(df.info())

# Access specific columns
#print(df['Carga'])

# Access specific rows
print(df["Carga"].iloc[56])  # Access the first row
print(df['Carga'][56])

# Filter rows based on conditions
#filtered_df = df[df['Carga'] > 10]

# Iterate over rows
#for index, row in df.iterrows():
 #   print(row['Carga'])

# Group data
#grouped_data = df.groupby('Carga').mean()
import csv
import numpy as np

# Define the data
Horas = [i for i in np.linspace(0, 23.75, 96)]
Carga = [0, 0, 0, 0, 0, 0, 10, 100, 500, 100, 10, 1000, 2000, 1000, 100, 10, 10, 10, 100, 500, 1000, 2000, 500, 10]
GerSolar = [0, 0, 0, 0, 0, 0, 5, 10, 100, 1000, 2000, 3000, 5000, 4000, 3000, 2000, 1000, 1000, 100, 5, 0, 0, 0, 0]
CargaVE =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5000, 0, 0, 0, 0, 0, 0, 5000, 0, 0, 0, 0]
previsao = [0, 0, 0, 0, 0, 0, 0, -90, -400, 900, 1990, 0, 0, 3000, -100, 990, 990, -1010, 0, -495, -1000, -2000, -500, -10]

# Interpolation
Horas_interp = np.linspace(0, 23.75, 96)
Carga_interp = np.interp(Horas_interp, range(len(Carga)), Carga)
GerSolar_interp = np.interp(Horas_interp, range(len(GerSolar)), GerSolar)
CargaVE_interp = np.interp(Horas_interp, range(len(CargaVE)), CargaVE)
previsao_interp = np.interp(Horas_interp, range(len(previsao)), previsao)

# Combine data into a list of lists
data = zip(Horas_interp, Carga_interp, GerSolar_interp, CargaVE_interp, previsao_interp)

# Specify the file path
file_path = 'Dados.csv'

# Write data to CSV file
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Hora', 'Carga', 'GerSolar', 'CargaVE', 'Previsao'])  # Write header
    for row in data:
        writer.writerow(row)

print("Data has been written to", file_path)
