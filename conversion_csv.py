import os
import pandas as pd
import matplotlib.pyplot as plt

def load_and_clean_data(directory):
    """Carga y limpia los datos de todos los archivos CSV en el directorio."""
    all_data = []

    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path)
            df.replace(-999, pd.NA, inplace=True)  # Reemplazar valores -999 con NaN
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  # Convertir la columna de fecha
            all_data.append(df)

    return pd.concat(all_data, ignore_index=True)

def analyze_data(df):
    """Analiza los datos y muestra estadísticas y gráficos."""
    # Calcular porcentaje de datos faltantes
    missing_percentage = (df.isna().sum() / len(df)) * 100
    print("Porcentaje de datos faltantes:")
    print(missing_percentage)

    # Agregar columna de año
    df['año'] = df['fecha'].dt.year

    # Calcular estadísticas anuales
    annual_stats = df.groupby('año')['precipitacion'].agg(['sum', 'mean']).rename(columns={'sum': 'total_anual', 'mean': 'media_anual'})
    annual_stats['tasa_variacion'] = annual_stats['total_anual'].pct_change() * 100

    print("\nEstadísticas anuales:")
    print(annual_stats)

    # Identificar años extremos
    most_rainy_year = annual_stats['total_anual'].idxmax()
    least_rainy_year = annual_stats['total_anual'].idxmin()
    print(f"Año más lluvioso: {most_rainy_year}")
    print(f"Año más seco: {least_rainy_year}")

    # Graficar estadísticas
    annual_stats['total_anual'].plot(kind='bar', title='Precipitación Total Anual', xlabel='Año', ylabel='Total Precipitación (mm)')
    plt.show()

    annual_stats['media_anual'].plot(kind='line', title='Media Anual de Precipitación', xlabel='Año', ylabel='Media Precipitación (mm)')
    plt.show()

def main():
    directory = "./datos_aemet"  # Cambia esta ruta si tus archivos están en otro lugar

    # Cargar y limpiar datos
    combined_data = load_and_clean_data(directory)

    # Analizar datos
    analyze_data(combined_data)

if __name__ == "__main__":
    main()
