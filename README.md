# Convertidor de `shapes` para GTFS

Esta es una herramienta para crear y validar un archivo `shapes.txt` de [GTFS](https://gtfs.org/) a partir de otros formatos de datos geoespaciales, utilizado en conjunto con el editor GTFS. El archivo `shapes.txt` contiene secuencias de puntos geoespaciales que describen una trayectoria de un viaje para una ruta de transporte público.

La herramienta utiliza [GeoPandas](https://geopandas.org/en/stable/) como base para el manejo de datos geoespaciales y [OSMnx](https://osmnx.readthedocs.io/en/stable/) para la validación de redes viales con mapas de OpenStreetMap.

A pesar de tener la intención de ser lo suficientemente general, el paquete está pensado para ser utilizado con el editor GTFS desarrollado para Costa Rica, por lo que no todos los supuestos aplican para cualquier _feed_ GTFS.

## Especificación de `shapes`

Este paquete utiliza la especificación del archivo `shapes.txt` de [GTFS Schedule 2.0](https://gtfs.org/schedule/reference/#shapestxt), que tiene los siguientes campos:

- `shape_id`: identificación de la trayectoria
- `shape_pt_lat`: latitud WGS84 en grados decimales
- `shape_pt_lon`: longitud WGS84 en grados decimales
- `shape_pt_sequence`: secuencia en que los puntos se conectan para formar la trayectoria
- `shape_dist_traveled`: distancia recorrida a lo largo de la trayectoria desde el primer punto hasta el punto actual

> Llave primaria compuesta (identificador único de cada registro): (`shape_id`, `shape_pt_sequence`)

## Validación de las trayectorias

La validación fundamental es que cada trayectoria sea un subconjunto de una red vial, es decir, que la trayectoria "pase por carretera" y que cumpla con, por ejemplo, el sentido de la vía y cualquier otro requisito de circulación.

Una validación opcional _a posterior_ es la cercanía de la trayectoria con las paradas que sigue una ruta (asumiendo que todos los viajes de una ruta siguen la misma secuencia de paradas, según una premisa del editor que no es obligatoria en GTFS). Esta validación, si se implementa, debería hacerse junto con otra tabla auxiliar llamada `route_stops`. Aunque esta validación es necesaria, quizá no corresponda a este paquete (discusión abierta).

## Posible secuencia de tareas y funciones

1. Recopilar datos como GeoDataFrame de GeoPandas.
2. Calcular distancias a través de la trayectoria hasta llegar a cada punto, para llenar la columna `shape_dist_traveled`.
3. Encontrar un _bounding box_ de la trayectoria (un rectángulo mínimo, u otra geometría mejor acotada, que contiene toda la trayectoria) para descargar los datos del mapa y validar que la trayectoria es parte de la red vial.
4. Exportar como tabla validada `shapes` de GTFS y posiblemente guardar en base de datos.

Según sea el paradigma de programación, es posible hacer funciones como:

```python
# Read shape from file or database and create GeoDataFrame
shape = X.get_shape(shape.geojson)

# Update GeoDataFrame with calculated column shape_dist_traveled
shape = X.distance_traveled(shape)

# Validate shape with given criteria (returns boolean)
X.validate_map(shape)

# Export as CSV-like table
X.export_shapes(shape)
```

donde `X` es el paquete creado. Posiblemente sea necesario hacer _bulk processing_ de trayectorias y no una por una como en el ejemplo anterior.

## Interacción con bases de datos

Como parte del proyecto de editor de GTFS, este paquete debe leer datos almacenados en bases de datos geoespaciales (en este caso, PostGIS en PostgreSQL con Django). Sin embargo, puede o no ser tarea de este paquete hacer la lectura y escritura de datos. Posiblemente, para mantenerlo generalizable, no lo haría.
