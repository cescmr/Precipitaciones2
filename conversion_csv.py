import os
import pandas as pd
import matplotlib.pyplot as plt

# PAS1: Leer y revisar los archivos
def inspect_files(directory):
    """Inspecciona los archivos en el directorio, verificando formato y columnas."""
    file_summaries = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Leer las primeras líneas para inspección
                    header = f.readline().strip()
                    columns = header.split(',')  # Suponiendo separación por comas
                    num_columns = len(columns)
                    file_summaries.append((file, num_columns, columns))
            except Exception as e:
                print(f"Error leyendo el archivo {file}: {e}")
    return file_summaries

# PAS2: Validación de formatos
def validate_files(directory, expected_columns):
    """Valida que todos los archivos tengan el mismo formato."""
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            try:
                df = pd.read_csv(file_path)
                if list(df.columns) != expected_columns:
                    print(f"Formato incorrecto en {file}")
            except Exception as e:
                print(f"Error procesando el archivo {file}: {e}")

# PAS3: Limpieza de datos
def clean_data(df):
    """Limpia y procesa el DataFrame."""
    # Reemplazar valores faltantes (-999) por NaN
    df.replace(-999, pd.NA, inplace=True)
    # Asegurar tipos de datos correctos
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    for col in df.select_dtypes(include=['object']).columns:
        if col != 'fecha':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# PAS4: Calcular estadísticas y analizar datos
def analyze_data(df):
    """Calcula estadísticas de las precipitaciones."""
    # Calcular porcentaje de datos faltantes
    missing_percentage = df.isna().mean() * 100

    # Estadísticas anuales
    df['año'] = df['fecha'].dt.year
    annual_stats = df.groupby('año')['precipitacion'].agg(['sum', 'mean']).rename(columns={'sum': 'total_anual', 'mean': 'media_anual'})

    # Tendencia anual (tasa de variación)
    annual_stats['tasa_variacion'] = annual_stats['total_anual'].pct_change() * 100

    # Años más húmedos y más secos
    most_rainy_year = annual_stats['total_anual'].idxmax()
    least_rainy_year = annual_stats['total_anual'].idxmin()

    print("Porcentaje de datos faltantes:")
    print(missing_percentage)
    print("\nEstadísticas anuales:")
    print(annual_stats)
    print(f"Año más lluvioso: {most_rainy_year}")
    print(f"Año más seco: {least_rainy_year}")

    # Gráficos
    annual_stats['total_anual'].plot(kind='bar', title='Precipitación Total Anual')
    plt.show()
    annual_stats['media_anual'].plot(kind='line', title='Media Anual de Precipitación')
    plt.show()

# Proceso completo
def main():
    directory = "./datos_aemet"  # Ruta al directorio con los archivos

    # Inspeccionar archivos
    file_summaries = inspect_files(directory)
    print("Resumen de archivos:")
    for summary in file_summaries:
        print(summary)

    # Validar archivos (usar columnas del primer archivo como referencia)
    if file_summaries:
        _, _, expected_columns = file_summaries[0]
        validate_files(directory, expected_columns)

    # Leer y procesar datos
    all_data = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path)
            df = clean_data(df)
            all_data.append(df)

    # Combinar todos los datos
    combined_data = pd.concat(all_data, ignore_index=True)

    # Analizar datos
    analyze_data(combined_data)

if __name__ == "__main__":
    main()
