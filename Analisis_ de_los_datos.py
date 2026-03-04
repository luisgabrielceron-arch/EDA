import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.float_format = '{:.2f}'.format

# 1. Cargar datos
df = pd.read_csv('cleaned_sampler.csv')
cols = ['Gender', 'Age', 'Travel method to school', 'Bag weight', 'Screen time after school', 'Climate change opinion']

# 3. GRÁFICOS VARIABLES CUALITATIVAS (Barras)
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.countplot(data=df, x='Gender', ax=axes[0], palette='Set2', order=df['Gender'].value_counts().index)
axes[0].set_title('Distribución por Género', fontsize=14)
axes[0].set_xlabel('Género')

sns.countplot(data=df, x='Travel method to school', ax=axes[1], palette='Set2', order=df['Travel method to school'].value_counts().index)
axes[1].set_title('Método de Transporte a la Escuela', fontsize=14)
axes[1].tick_params(axis='x', rotation=45)

sns.countplot(data=df, x='Climate change opinion', ax=axes[2], palette='Set2', order=df['Climate change opinion'].value_counts().index)
axes[2].set_title('Opinión sobre Cambio Climático', fontsize=14)
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# 4. GRÁFICOS VARIABLES CUANTITATIVAS (Histogramas y Boxplots)
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# Edad
sns.histplot(data=df, x='Age', discrete=True, ax=axes[0,0], color='skyblue')
axes[0,0].set_title('Distribución de Edad')
sns.boxplot(data=df, x='Age', ax=axes[1,0], color='skyblue')

# Peso Mochila
sns.histplot(data=df, x='Bag weight', kde=True, ax=axes[0,1], color='lightgreen')
axes[0,1].set_title('Distribución del Peso de Mochila (kg)')
sns.boxplot(data=df, x='Bag weight', ax=axes[1,1], color='lightgreen')

# Tiempo de pantalla
sns.histplot(data=df, x='Screen time after school', kde=True, ax=axes[0,2], color='salmon')
axes[0,2].set_title('Tiempo de Pantalla (Horas)')
sns.boxplot(data=df, x='Screen time after school', ax=axes[1,2], color='salmon')

plt.tight_layout()
plt.show()

# 5. IMPRIMIR ESTADÍSTICAS DESCRIPTIVAS NUMÉRICAS
print(df[['Age', 'Bag weight', 'Screen time after school']].describe())

#---------------------------------------ANALÍSIS BIVARIADO---------------------------------------

# Creamos el gráfico de caja
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df, 
    x='Travel method to school', 
    y='Bag weight', 
    palette='Set2'
)

# Títulos y etiquetas claras
plt.title('Comparación del Peso de la Mochila según el Método de Transporte', fontsize=14)
plt.xlabel('Método de Transporte', fontsize=12)
plt.ylabel('Peso de la Mochila (kg)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.show()

# Relación entre Tiempo de pantalla tras el colegio y la Edad

# Gráfico de dispersión con una línea de tendencia
plt.figure(figsize=(9, 6))

# Creamos el gráfico de dispersión con línea de tendencia Y JITTER
sns.regplot(data=df, 
            x='Age', 
            y='Screen time after school', 
            x_jitter=0.3,  # <--- ESTA ES LA MAGIA: Separa los puntos horizontalmente
            y_jitter=0.1,  # <--- Separa un poquito los puntos verticalmente
            scatter_kws={'alpha': 0.4, 'color': 'steelblue'}, # Puntos más transparentes y azules
            line_kws={'color': 'red', 'linewidth': 2})  # Línea de tendencia en rojo

# Personalizamos los textos
plt.title('Relación entre Edad y Tiempo de Pantalla después de la escuela', fontsize=14)
plt.xlabel('Edad (Años)', fontsize=12)
plt.ylabel('Tiempo de pantalla (Horas)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5) # Una cuadrícula de fondo ayuda a leer mejor

# Mostramos el gráfico
plt.show()

# Calculo del numero exacto de esta correlacion 

# Calculamos la correlación específica
correlacion_edad_pantalla = df['Age'].corr(df['Screen time after school'])

# Imprimimos el resultado redondeado a 2 decimales
print(f"La correlación entre Edad y Tiempo de pantalla es: {correlacion_edad_pantalla:.2f}")


#-----------------CALCULO ENCUESTA ESTUDIANTES 11 12 13 SOBRE DROGAS------------------

# Cargar los datos (asegúrate de que los archivos estén en la misma carpeta que tu código)
df_respuestas = pd.read_csv('year11_13_responses_30b.csv')
df_no_respuestas = pd.read_csv('year11_13_no_responses_30b.csv')

# Filtrar para asegurar que solo trabajamos con Years 11, 12 y 13
anios_deseados = ['Year 11', 'Year 12', 'Year 13']
df_respuestas = df_respuestas[df_respuestas['Year categorical'].isin(anios_deseados)]
df_no_respuestas = df_no_respuestas[df_no_respuestas['Year categorical'].isin(anios_deseados)]

# Nombres exactos de las columnas de la encuesta (según tu dataset)
col_30a = 'How true: I get carried away by my feelings'
col_30b = 'How true: I say the first thing that comes into my mind without thinking enough about it'

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar el archivo de los que SÍ respondieron
df = pd.read_csv('year11_13_responses_30b.csv')

# Filtrar solo Years 11, 12 y 13
anios = ['Year 11', 'Year 12', 'Year 13']
df = df[df['Year categorical'].isin(anios)]

# Columnas exactas de la pregunta 30A (Estudiantes)
cols_30a = [
    'How wrong - Drink alcohol',
    'How wrong - Smoke tobacco cigarettes',
    'How wrong - Smoke e-cigarettes',
    'How wrong - Smoke marijuana'
]

# Transformar los datos para graficarlos fácil
df_30a = df[['Year categorical'] + cols_30a].melt(
    id_vars='Year categorical', 
    var_name='Sustancia', 
    value_name='Nivel de Desaprobación'
)

# Limpiar los nombres de las columnas para que el gráfico quede más bonito
df_30a['Sustancia'] = df_30a['Sustancia'].str.replace('How wrong - ', '')

# 2. Crear el Gráfico
plt.figure(figsize=(10, 6))
sns.barplot(data=df_30a, x='Sustancia', y='Nivel de Desaprobación', hue='Year categorical', order=['Drink alcohol', 'Smoke tobacco cigarettes', 'Smoke e-cigarettes', 'Smoke marijuana'], hue_order=anios, palette='mako')

plt.title('Pregunta 30A: ¿Qué tan incorrecto ves que alguien de tu edad consuma...? (Puntaje Promedio)', fontsize=14)
plt.xlabel('Tipo de Sustancia', fontsize=12)
plt.ylabel('Nivel de Desaprobación\n(-100 = Nada, 100 = Muy incorrecto)', fontsize=12)
plt.legend(title='Año Escolar')
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.show()


# Columnas exactas de la pregunta 30B (Padres)
cols_30b = [
    'How wrong (caregivers/parents) - Drink alcohol',
    'How wrong (caregivers/parents) - Smoke tobacco cigarettes',
    'How wrong (caregivers/parents) - Smoke e-cigarettes',
    'How wrong (caregivers/parents) - Smoke marijuana'
]

# Transformar los datos
df_30b = df[['Year categorical'] + cols_30b].melt(
    id_vars='Year categorical', 
    var_name='Sustancia', 
    value_name='Nivel de Desaprobación'
)

# Limpiar los nombres
df_30b['Sustancia'] = df_30b['Sustancia'].str.replace('How wrong (caregivers/parents) - ', '', regex=False)

# Crear el Gráfico
plt.figure(figsize=(10, 6))
sns.barplot(data=df_30b, x='Sustancia', y='Nivel de Desaprobación', hue='Year categorical', order=['Drink alcohol', 'Smoke tobacco cigarettes', 'Smoke e-cigarettes', 'Smoke marijuana'], hue_order=anios, palette='rocket')

plt.title('Pregunta 30B: ¿Qué tan incorrecto creen tus padres que sería si tú consumieras...? (Puntaje Promedio)', fontsize=14)
plt.xlabel('Tipo de Sustancia', fontsize=12)
plt.ylabel('Nivel de Desaprobación\n(-100 = Nada, 100 = Muy incorrecto)', fontsize=12)
plt.legend(title='Año Escolar', loc='lower right')
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.show()