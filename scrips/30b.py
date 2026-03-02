import os
import pandas as pd

def filter_year11_13_30b():
    # Carpeta donde está este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta al archivo raw (subir un nivel y luego a data/raw)
    raw_path = os.path.normpath(os.path.join(script_dir, "..", "data", "raw", "sampler.csv"))
    
    # Ruta de salida (subir un nivel y luego a data/processed)
    output_dir = os.path.normpath(os.path.join(script_dir, "..", "data", "processed"))
    output_path = os.path.join(output_dir, "year11_13_responses_30b.csv")
    
    # Crear carpeta de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Leer CSV
    try:
        df = pd.read_csv(raw_path)
    except FileNotFoundError:
        print(f"Archivo no encontrado en: {raw_path}")
        print("Verifica que el archivo exista en esa ruta.")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    print(f"Total de filas en raw: {len(df)}")
    
    # Verificar que la columna 'Year numeric' existe
    if 'Year numeric' not in df.columns:
        print("La columna 'Year numeric' no existe. Columnas disponibles:")
        print(df.columns.tolist()[:10])  # muestra las primeras 10
        return
    
    # Convertir a numérico y filtrar años 11-13
    df['Year numeric'] = pd.to_numeric(df['Year numeric'], errors='coerce')
    mask_year = df['Year numeric'].isin([11, 12, 13])
    df_year = df[mask_year].copy()
    print(f"Estudiantes en años 11-13: {len(df_year)}")
    
    # Identificar columnas de la pregunta 30b
    cols_30b = [col for col in df.columns if col.startswith("How wrong (caregivers/parents) -")]
    print(f"Columnas de pregunta 30b encontradas: {len(cols_30b)}")
    
    if len(cols_30b) == 0:
        print("No se encontraron columnas con ese prefijo. Lista de columnas disponibles:")
        # Mostrar columnas que podrían ser las de interés
        possible = [col for col in df.columns if "caregivers" in col or "parents" in col]
        print(possible[:10])
        return
    
    # Filtrar quienes respondieron al menos una (no nulo)
    mask_response = df_year[cols_30b].notna().any(axis=1)
    df_responses = df_year[mask_response].copy()
    
    print(f"Estudiantes que respondieron al menos una pregunta 30b: {len(df_responses)}")
    
    # Guardar
    df_responses.to_csv(output_path, index=False)
    print(f"Archivo guardado en: {output_path}")
    
    # Opcional: guardar los que no respondieron
    df_no_response = df_year[~mask_response].copy()
    if len(df_no_response) > 0:
        no_resp_path = os.path.join(output_dir, "year11_13_no_responses_30b.csv")
        df_no_response.to_csv(no_resp_path, index=False)
        print(f"Archivo de no respondedores guardado en: {no_resp_path}")
    
    print("\nResumen:")
    print(f"Total años 11-13: {len(df_year)}")
    print(f"Respondieron: {len(df_responses)} ({len(df_responses)/len(df_year)*100:.1f}%)")
    print(f"No respondieron: {len(df_no_response)}")

if __name__ == "__main__":
    filter_year11_13_30b()