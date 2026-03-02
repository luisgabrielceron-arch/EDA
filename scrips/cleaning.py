import os
import pandas as pd
import numpy as np

def clean_sampler_data(input_path, output_path):
    """
    Limpia el archivo sampler.csv basado en el cuestionario Census_Blank.pdf.
    """
    print("Cargando datos...")
    df = pd.read_csv(input_path)
    original_shape = df.shape
    print(f"Dimensiones originales: {original_shape}")

    # --- 1. Manejo de valores nulos y reemplazos ---
    # Reemplazar "n/a" literal por NaN
    df = df.replace("n/a", np.nan)
    # También reemplazar cadenas vacías por NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)

    # --- 2. Columnas numéricas (convertir a float/int) ---
    # Edad
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    # Altura, longitud pie, circunferencias, etc.
    numeric_cols = ['Height', 'Right foot length', 'Wrist circumference', 
                    'Left thumb circumference', 'Travel time to school', 
                    'Bag weight', 'Fruit/vegetables in lunch', 'Memory time',
                    'Reaction time', 'Time standing on left leg', 
                    'Scheduled activities in last week', 'Screen time after school',
                    'Bed time', 'Wake time', 'Time you get home from school',
                    'Time you ate dinner'] + [col for col in df.columns if col.startswith('How true')]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Las columnas de tiempo (Bed time, etc.) podrían convertirse a datetime, pero por ahora las dejamos como string
    # Nota: algunas tienen valores como "23:30:00", otras vacías. Se mantienen como string.

    # --- 3. Columnas categóricas con opciones conocidas ---
    # Género
    gender_map = {'male': 'M', 'female': 'F'}
    df['Gender'] = df['Gender'].map(gender_map).fillna(df['Gender'])  # conserva otros si los hay

    # País de nacimiento - podría estandarizar mayúsculas, pero hay muchos únicos; lo dejamos.
    # Etnias: convierto 'yes'/'no' a 1/0
    ethnic_cols = ['New Zealand European', 'Maori', 'Samoan', 'Cook Islands Maori',
                   'Tongan', 'Niuean', 'Chinese', 'Indian']
    for col in ethnic_cols:
        if col in df.columns:
            df[col] = df[col].map({'yes': 1, 'no': 0}).fillna(0).astype(int)

    # Color de ojos - estandarizar a minúsculas
    df['Eye Colour'] = df['Eye Colour'].str.lower()

    # Handedness
    handed_map = {'right- handed': 'right', 'left- handed': 'left', 'ambidextrous': 'ambi'}
    df['Handedness'] = df['Handedness'].str.lower().map(handed_map).fillna(df['Handedness'])

    # Método de viaje
    df['Travel method to school'] = df['Travel method to school'].str.lower()

    # Litter in lunch: 'yes'/'no'/'nolunch'
    df['Litter in lunch'] = df['Litter in lunch'].str.lower()

    # Tecnología (columnas de 23): convierto 'yes' a 1, pero algunas son 'no' o vacío. 
    tech_cols = ['Own cell phone', 'Facebook account', 'Instagram account', 
                 'Snapchat account', 'Reddit account', 'YouTube channel', 
                 'Technology - None of these']
    for col in tech_cols:
        if col in df.columns:
            df[col] = df[col].map({'yes': 1, 'no': 0}).fillna(0).astype(int)

    # Frecuencias (siempre, a menudo, etc.) - se pueden mapear a números ordinales si se desea
    freq_map = {'always': 4, 'often': 3, 'sometimes': 2, 'rarely': 1, 'never': 0}
    freq_cols = ['Check messages as soon as you wake up', 'Respond to messages immediately',
                 'Take phone to school', 'Lose focus as school due to phone']
    for col in freq_cols:
        if col in df.columns:
            df[col] = df[col].str.lower().map(freq_map).fillna(df[col])

    # Sentimientos sin teléfono (múltiples opciones) - son binarias (1 si marcó)
    feeling_cols = ['Feeling without phone - Angry', 'Feeling without phone - Anxious',
                    'Feeling without phone - Frustrated', 'Feeling without phone - Happy',
                    'Feeling without phone - Lonely', 'Feeling without phone - Relieved',
                    'Feeling without phone - Sad', 'Feeling without phone - Neutral']
    for col in feeling_cols:
        if col in df.columns:
            df[col] = df[col].map({'yes': 1, 'no': 0}).fillna(0).astype(int)

    # Opinión sobre tiempo de pantalla
    screen_opinion_map = {'toomuch': 'too much', 'aboutright': 'about right', 'toolittle': 'too little'}
    for col in ['Screen time opinion - On your phone', 'Screen time opinion - On social media',
                'Screen time opinion - Playing video games']:
        if col in df.columns:
            df[col] = df[col].str.lower().map(screen_opinion_map).fillna(df[col])

    # Opinión cambio climático
    climate_map = {
        'urgent': 'urgent',
        'future': 'future',
        'notaproblem': 'not a problem',
        'dontknow': "don't know"
    }
    df['Climate change opinion'] = df['Climate change opinion'].str.lower().map(climate_map).fillna(df['Climate change opinion'])

    # --- 4. Validación de rangos razonables (eliminar filas con outliers extremos) ---
    initial_rows = len(df)
    # Edad: entre 4 y 20 años (rango escolar típico)
    df = df[(df['Age'] >= 4) & (df['Age'] <= 20) | df['Age'].isna()]
    # Altura: entre 80 y 220 cm (niños pequeños a adolescentes altos)
    if 'Height' in df.columns:
        df = df[(df['Height'] >= 80) & (df['Height'] <= 220) | df['Height'].isna()]
    # Peso de mochila: entre 0 y 30 kg (razonable)
    if 'Bag weight' in df.columns:
        df = df[(df['Bag weight'] >= 0) & (df['Bag weight'] <= 30) | df['Bag weight'].isna()]
    # Tiempo de viaje: entre 0 y 240 minutos
    if 'Travel time to school' in df.columns:
        df = df[(df['Travel time to school'] >= 0) & (df['Travel time to school'] <= 240) | df['Travel time to school'].isna()]
    
    rows_after_range = len(df)
    print(f"Filas eliminadas por rangos inválidos: {initial_rows - rows_after_range}")

    # --- 5. Guardar resultado ---
    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Datos limpios guardados en: {output_path}")
    print(f"Dimensiones finales: {df.shape}")
    print("\nResumen de valores nulos por columna (primeras 10):")
    print(df.isnull().sum().sort_values(ascending=False).head(10))

if __name__ == "__main__":
    input_file = os.path.join("..", "data", "raw", "sampler.csv")
    output_file = os.path.join("..", "data", "processed", "cleaned_sampler.csv")
    clean_sampler_data(input_file, output_file)