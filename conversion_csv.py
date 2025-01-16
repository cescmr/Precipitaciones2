import os
import pandas as pd
import matplotlib.pyplot as plt

def inspect_files(directory):
    """
    Inspecciona los archivos en el directorio, verificando formato y columnas.
    """
    file_summaries = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    header = f.readline().strip()
                    columns = header.split(',')
                    num_columns = len(columns)
                    file_summaries.append((file, num_columns, columns))
            except Exception as e:
                print(f"Error leyendo el archivo {file}: {e}")
    return file_summaries

def validate_files(directory, expected_columns):
    """
    Valida que todos los archivos tengan el mismo formato.
    """
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            try:
                df = pd.read_csv(file_path)
                if list(df.columns) != expected_columns:
                    print(f"Formato incorrecto en {file}")
            except Exception as e:
                print(f"Error procesando el archivo {file}: {e}")

def clean_data(df):
    """
    Limpia y procesa el DataFrame.
    """
    df.replace(-999, pd.NA, inplace=True)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    for col in df.select_dtypes(include=['object']).columns:
        if col != 'fecha':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def analyze_data(df):
    """
    Calcula estadísticas de las precipitaciones.
    """
    missing_percentage = (df.isna().sum() / len(df)) * 100

    df['año'] = df['fecha'].dt.year
    annual_stats = df.groupby('año')['precipitacion'].agg(['sum', 'mean']).rename(columns={'sum': 'total_anual', 'mean': 'media_anual'})
    annual_stats['tasa_variacion'] = annual_stats['total_anual'].pct_change() * 100

    most_rainy_year = annual_stats['total_anual'].idxmax()
    least_rainy_year = annual_stats['total_anual'].idxmin()

    print("Porcentaje de datos faltantes:")
    print(missing_percentage)
    print("\nEstadísticas anuales:")
    print(annual_stats)
    print(f"Año más lluvioso: {most_rainy_year}")
    print(f"Año más seco: {least_rainy_year}")

    annual_stats['total_anual'].plot(kind='bar', title='Precipitación Total Anual', xlabel='Año', ylabel='Total Precipitación (mm)')
    plt.show()

    annual_stats['media_anual'].plot(kind='line', title='Media Anual de Precipitación', xlabel='Año', ylabel='Media Precipitación (mm)')
    plt.show()

def main():
    directory = "./datos_aemet"

    file_summaries = inspect_files(directory)
    print("Resumen de archivos:")
    for summary in file_summaries:
        print(summary)

    if file_summaries:
        _, _, expected_columns = file_summaries[0]
        validate_files(directory, expected_columns)

    all_data = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            df = pd.read_csv(file_path)
            df = clean_data(df)
            all_data.append(df)

    combined_data = pd.concat(all_data, ignore_index=True)
    analyze_data(combined_data)

if __name__ == "__main__":
    main()
