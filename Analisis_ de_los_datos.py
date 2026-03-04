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

# Esto cruzará Edad, Peso de mochila y Tiempo de pantalla entre sí
sns.pairplot(df[['Age', 'Bag weight', 'Screen time after school']])
plt.show()

# Calculamos la correlación y la redondeamos a 2 decimales
correlacion = df[['Age', 'Bag weight', 'Screen time after school']].corr().round(2)
print(correlacion)

#Mapa de calor 
plt.figure(figsize=(8, 6))
sns.heatmap(correlacion, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Mapa de Correlación')
plt.show()

# Relación entre Tiempo de pantalla tras el colegio y la Edad

# Gráfico de dispersión con una línea de tendencia
plt.figure(figsize=(9, 6))

# Creamos el gráfico de dispersión con línea de tendencia
sns.regplot(data=df, 
            x='Age', 
            y='Screen time after school', 
            scatter_kws={'alpha':0.5}, # Puntos un poco transparentes
            line_kws={'color':'red'})  # Línea de tendencia en rojo para que resalte

# Personalizamos los textos
plt.title('Relación entre Edad y Tiempo de Pantalla después de la escuela', fontsize=14)
plt.xlabel('Edad (Años)', fontsize=12)
plt.ylabel('Tiempo de pantalla (Horas)', fontsize=12)

# Mostramos el gráfico
plt.show()

# Calculo del numero exacto de esta correlacion 

# Calculamos la correlación específica
correlacion_edad_pantalla = df['Age'].corr(df['Screen time after school'])

# Imprimimos el resultado redondeado a 2 decimales
print(f"La correlación entre Edad y Tiempo de pantalla es: {correlacion_edad_pantalla:.2f}")

