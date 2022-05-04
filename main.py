# Preprocesar el fichero de alojamientos para crear un data frame con las variables id, host_id, listing_url, room_type, neighbourhood_group_cleansed, price, cleaning_fee, accommodates, minimum_nights, minimum_cost, review_scores_rating, latitude, longitude, is_location_exact. Eliminar del data frame cualquier fila incompleta. Añadir al data frame nuevas variables con el coste mínimo por noche y por persona (que incluya los gastos de limpieza), y el número de servicios que ofrece el alojamiento.

# Creamos un DataFrame desde la url del fichero csv
alojamientos = pd.read_csv('madrid-airbnb-listings-small.csv', sep = '\t')
# Renombramos los nombres de las columnas que queremos
alojamientos.rename(columns = {'host_id': 'anfitrion', 'listing_url': 'url', 'room_type':'tipo_alojamiento', 'neighbourhood_group_cleansed':'distrito', 'price':'precio', 'cleaning_fee':'gastos_limpieza', 'accommodates':'plazas', 'minimum_nights':'noches_minimas', 'review_scores_rating':'puntuacion'}, inplace = True)
# Filtramos las columnas que quermos
alojamientos = alojamientos[['id', 'anfitrion', 'url', 'tipo_alojamiento', 'distrito', 'precio', 'gastos_limpieza', 'plazas', 'noches_minimas', 'puntuacion']]
# Eliminamos las filas con valores desconocidos
alojamientos = alojamientos.dropna()
# Eliminamos el carácter $ de las columnas del precio y gastos_limpieza y las convertimos a float
alojamientos['precio'] = alojamientos.precio.str.replace(',','').str[1:].astype('float')
alojamientos['gastos_limpieza'] = alojamientos.gastos_limpieza.str[1:].astype('float')
# Creamos una nueva columna con el precio por persona multiplicando el precio diario por el número mínimo de noches, sumando los gastos de limpieza y finalmente dividiendo por el número mínimo de noches y el número de plazas.
alojamientos['precio_persona'] = (alojamientos.precio * alojamientos.noches_minimas + alojamientos.gastos_limpieza) / (alojamientos.noches_minimas + alojamientos.plazas)
print(alojamientos)

# Ejercicio 7
# Crear una función que reciba una lista de distritos y devuelva una serie con los tipos de alojamiento en esos distritos y el porcentaje de alojamientos de ese tipo.
def tipos_alojamientos_distritos(alojamientos, distritos):
    '''
    Función que devuelve una serie con el porcentaje de tipos de alojamientos en una lista de distritos dada.

    Parámetros:
    - alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
    - distritos: Es una lista con los nombres de los distritos. 
    
    Devuelve: Una serie con el porcentaje de tipos de alojamientos en los distritos dados.
    '''
    return alojamientos[alojamientos.distrito.isin(distritos)].tipo_alojamiento.value_counts(normalize = True) * 100

# Ejemplo
print(tipos_alojamientos_distritos(alojamientos, ['Arganzuela', 'Centro']))

# Ejercicio 8
# Crear una función que reciba una lista de distritos y devuelva una serie con el número de alojamientos que cada anfitrión ofrece en esos distritos, ordenado de más a menos alojamientos.

def alojamientos_anfitriones_distritos(alojamientos, distritos):
    '''
    Función que devuelve una serie con el número de alojamientos de cada anfitrion en unos distritos dados, ordenada de mas a menos alojamientos.

    Parámetros:
    - alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
    - distritos: Es una lista con los nombres de los distritos. 
    
    Devuelve: Una serie con el número de alojamientos de cada anfitrion en los distritos dados, ordenada de mas a menos alojamientos.
    '''
    return alojamientos[alojamientos.distrito.isin(distritos)].anfitrion.value_counts().sort_values(ascending = False)

# Ejemplo
print(alojamientos_anfitriones_distritos(alojamientos, ['Centro']))
print(alojamientos_anfitriones_distritos(alojamientos, ['Villaverde']))

# Ejercicio 9
# Crear una función que reciba devuelva una serie con el número medio de alojamientos por anfitrión de cada distrito.

def media_alojamientos_distritos(alojamientos):
    '''
    Función que devuelve una serie con el número medio de alojamientos por anfitrión de cada distrito.

    Parámetros:
    - alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
    
    Devuelve: Una serie con el número medio de alojamientos por anfitrión de cada distrito.

    '''
    return alojamientos.groupby('distrito').anfitrion.value_counts().unstack(level = "distrito").mean()

# Ejemplo
print('Número medio de alojamientos por anfitrión en cada distrito')
print(media_alojamientos_distritos(alojamientos))

# Ejercicio 10
# Crear una función que reciba una lista de distritos y dibuje un diagrama de sectores con los porcentajes de tipos de alojamientos en esos distritos.

def sectores_tipos_alojamientos(alojamientos, distritos):
    '''
    Función que dibuja un diagrama de sectores con los porcentajes de tipos de alojamientos en unos distritos dados.

    Parámetros:
    - alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
    - distritos: Es una lista con los nombres de los distritos. 
    '''
    # Definimos la figura y los ejes del gráfico
    fig, ax = plt.subplots()
    # Filtramos los distritos de la lista de distritos dada, después contamos la frecuencias de los tipos de alojamientos y dibujamos el diagrama de sectores
    alojamientos[alojamientos.distrito.isin(distritos)].tipo_alojamiento.value_counts(normalize = True).plot(kind = 'pie',  autopct='%1.0f%%', ax = ax)
    # Ponermos el título
    ax.set_title('Distribución del porcentaje de tipos de alojamientos\n Distritos de ' + ', '.join(distritos), loc = "center", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    # Eliminamos la etiqueta del eje y
    ax.set_ylabel('')
    # Guardamos el gráfico.
    plt.savefig('img/sectores-tipos-alojamientos-' + '-'.join(distritos) + '.png', bbox_inches='tight')
    return

#Ejemplo
sectores_tipos_alojamientos(alojamientos, ['Arganzuela', 'Centro'], )

# Ejercicio 11
# Crear una función que dibuje un diagrama de barras con el número de alojamientos por distritos.

def barras_alojamientos_distritos(alojamientos):
    '''
    Función que dibuja un diagrama de barras con el número de alojamientos por distritos.

    Parámetros:
    - alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
    '''
    # Definimos la figura y los ejes del gráfico
    fig, ax = plt.subplots()
    # Contamos la frecuencias de alojamientos por distritos y dibujamos las barras.
    alojamientos.distrito.value_counts().plot(kind = 'bar')
    # Ponemos el título
    ax.set_title('Número de alojamientos por distrito', loc = "center", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    # Ponemos una rejilla
    ax.grid(axis = 'y', color = 'lightgray', linestyle = 'dashed')
    # Guardamos el gráfico.
    plt.savefig('img/barras-alojamientos-distritos.png', bbox_inches='tight')
    return

# Ejemplo
barras_alojamientos_distritos(alojamientos)

# Ejercicio 12
# Crear una función que dibuje un diagrama de barras con los porcentajes acumulados de tipos de alojamientos por distritos.

def barras_tipos_alojamientos_distritos(alojamientos):
    '''
    Función que dibuja un diagrama de barras con los porcentajes acumulados de tipos de alojamientos por distritos.

    Parámetros:
    - alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
    '''
    # Definimos la figura y los ejes del gráfico
    fig, ax = plt.subplots()
    # Agrupamos el DataFrame por distritos y contamos las frecuencias de los tipos de alojamiento. Después pivotamos el índice de los tipos de alojamientos para pasarlos a columnas y dibujamos las barras acumuladas.
    (alojamientos.groupby('distrito').tipo_alojamiento.value_counts(normalize = True)*100).unstack().plot(kind = 'bar', stacked = True, ax = ax)
    # Ponemos el título
    ax.set_title('Tipos de alojamiento por distrito (%)', loc = "center", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    # Eliminamos la etiqueta del eje x
    ax.set_xlabel('')
    # Ponemos una rejilla
    ax.grid(axis = 'y', color = 'lightgray', linestyle = 'dashed')
    # Reducimos el eje x un 30% para que quepa la leyenda
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    # Dibujar la leyenda fuera del área del gráfico
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    # Guardamos el gráfico.
    plt.savefig('img/barras-tipos-alojamientos-distritos.png', bbox_inches='tight')
    return

# Ejemplo
barras_tipos_alojamientos_distritos(alojamientos)

# Ejercicio 13
# Crear una función reciba una lista de distritos y una lista de tipos de alojamientos, y dibuje un diagrama de sectores con la distribución del número de alojamientos de ese tipo por anfitrión en esos distritos.

def sectores_tipos_alojamientos_anfitrion(alojamientos, distritos, tipos):
    '''
    Función que dibuja un diagrama de sectores con la distribución del número de alojamientos por anfitrión de unos tipos y en unos distritos dados.

    Parámetros:
    - alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
    - distritos: Es una lista con los nombres de los distritos. 
    - tipos: Es una lista con los nombres de los tipos de alojamientos.
    '''
    # Definimos la figura y los ejes del gráfico
    fig, ax = plt.subplots()
    # Filtramos los distritos y los tipos de alojamientos 
    alojamientos_filtrados = alojamientos[alojamientos.distrito.isin(distritos) & alojamientos.tipo_alojamiento.isin(tipos)]
    # Contamos la frecuencia de alojamientos por anfitrión y dibujamos el diagrama de sectores
    alojamientos_filtrados.anfitrion.value_counts(normalize = True).plot(kind = 'pie', labels = None, ax = ax)
    # Ponermos el título
    ax.set_title('Distribución del número de alojamientos por anfitrión\nDistritos de ' + ', '.join(distritos) + '\nTipos de alojamiento' + ','.join(tipos), loc = "center", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    # Eliminamos la etiqueta del eje y
    ax.set_ylabel('')
    # Guardamos el gráfico.
    plt.savefig('img/sectores-tipos-alojamientos-anfitrion-' + '-'.join(distritos) + '.png', bbox_inches='tight')
    return

# Ejemplo
sectores_tipos_alojamientos_anfitrion(alojamientos, ['Arganzuela', 'Centro'], ['Entire home/apt', 'Hotel room'])

# Ejercicio 14
# Crear una función que dibuje un diagrama de barras con los precios medios por persona y día de cada distrito.

def barras_precios_medios_persona(alojamientos):
    '''
    Función que dibuja un diagrama de barras con los precios medios por persona y día de cada distrito.

    Parámetros:
    - alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
    '''
    # Definimos la figura y los ejes del gráfico
    fig, ax = plt.subplots()
    # Agrupamos por distrito, calculamos la media de precio por persona y dibujamos las barras.
    alojamientos.groupby('distrito').precio_persona.mean().plot(kind = 'bar', ax = ax)
    # Ponemos el título
    ax.set_title('Precio medio por persona y noche', loc = "center", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    # Eliminamos la etiqueta del eje x
    ax.set_xlabel('')
    # Ponemos una rejilla
    ax.grid(axis = 'y', color = 'lightgray', linestyle = 'dashed')
    # Guardamos el gráfico.
    plt.savefig('img/precios-medios-distritos.png', bbox_inches='tight')
    return

# Ejemplo
barras_precios_medios_persona(alojamientos)

# Ejercicio 15
# Crear una función que reciba una lista de distritos y dibuje un gráfico de dispersión con el precio por noche y persona y la puntuación en esos distritos.

def precios_puntuacion_distritos(alojamientos, distritos):
    '''
    Función que dibuja un diagrama de dispersión con el precio por noche y persona y la puntuación en unos distritos dados.

    Parámetros:
    - alojamientos: Es una lista de diccionarios, donde cada diccionario contiene los datos de un alojamiento.
    - distritos: Es una lista con los nombres de los distritos. 
    '''
    # Definimos la figura y los ejes del gráfico
    fig, ax = plt.subplots()
    # Filtramos los distritos
    alojamientos_filtrados = alojamientos[alojamientos.distrito.isin(distritos)]
    # Creamos una nueva columna con el precio por persona multiplicando el precio diario por el número mínimo de noches, sumando los gastos de limpieza y finalmente dividiendo por el número mínimo de noches y el número de plazas.
    alojamientos['precio_persona'] = (alojamientos.precio * alojamientos.noches_minimas + alojamientos.gastos_limpieza) / (alojamientos.noches_minimas + alojamientos.plazas)
    # Dibujamos el diagrama de sipersión
    ax.scatter(alojamientos['precio_persona'], alojamientos['puntuacion'])
    # Ponemos el título
    ax.set_title('Precios vs Puntuación\nDistritos de ' + ', '.join(distritos), loc = "center", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    # Ponemos las etiquetas de los ejes
    ax.set_xlabel('Precio en €')
    ax.set_ylabel('Puntuación')
    # Guardamos el gráfico.
    plt.savefig('img/precios-puntuacion-distritos.png', bbox_inches='tight')
    return

# Ejemplo
precios_puntuacion_distritos(alojamientos, ['Arganzuela', 'Centro'])