# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 18:48:09 2025

@author: carlo
"""

"""
Created on Thu Mar 14 17:28:33 2024

@author: carlo
"""


import yfinance as yf
import pandas as pd

# Obtención de la acción
infal = yf.Ticker("0P0001MIBG.F")

# Obtener datos históricos de la acción
historical_data = infal.history(period="max")

# Eliminar la zona horaria del índice
historical_data.index = historical_data.index.tz_localize(None)

# Mostrar los primeros registros para ver cómo están organizados los datos
# print(historical_data.head())

# Preguntar cuándo compraste las acciones
compra_fecha = input("¿En qué fecha compraste el fondo Infal patrimonio? (Formato: YYYY-MM-DD): ")

# Asegurarse de que la fecha esté en formato correcto y sin zona horaria
compra_fecha = pd.to_datetime(compra_fecha).tz_localize(None)

# Si la fecha de compra no está en los datos, tomar la fecha más cercana disponible
if compra_fecha not in historical_data.index:
    # Obtener la fecha más cercana posterior (si no existe la fecha exacta)
    compra_fecha = historical_data.index[historical_data.index.searchsorted(compra_fecha, side='right')]

# Filtrar los datos desde la fecha de compra
historical_data['Date'] = historical_data.index
historical_data = historical_data[historical_data['Date'] >= compra_fecha]


# Calcular la rentabilidad desde la compra (diferencia entre el precio de cierre en la fecha de compra y el precio más reciente)
precio_compra = historical_data.iloc[0]['Close']
precio_ultimo = historical_data.iloc[-1]['Close']
fecha_ultimo = historical_data.index[-1].date()  # Fecha del último precio
rentabilidad = (precio_ultimo - precio_compra) / precio_compra * 100

# Calcular la volatilidad (desviación estándar de los precios de cierre)
volatilidad = historical_data['Close'].pct_change().std() * (252 ** 0.5)*100  # Anualizada

# Calcular la máxima caída (drawdown)
historical_data['Rolling_max'] = historical_data['Close'].cummax()
historical_data['Drawdown'] = historical_data['Close'] / historical_data['Rolling_max'] - 1
max_drawdown = historical_data['Drawdown'].min()

# Mostrar resultados
print(f"\nResultados desde la fecha de compra ({compra_fecha.date()}) :")
print(f"Precio de compra: {precio_compra:.2f}")
print(f"Fecha y precio más reciente: {fecha_ultimo} - {precio_ultimo:.2f}")
print(f"Rentabilidad: {rentabilidad:.2f}%")
print(f"Volatilidad anualizada: {volatilidad:.2f}%")
print(f"Máxima caída: {max_drawdown * 100:.2f}%")

