import pandas as pd
import geopandas as gpd
import osmnx as ox
from shapely.geometry import LineString, Point


def convert(gdf):
    """Converts a GeoJSON file containing LineString features to a CSV with shape information.

    Parameters
    ----------
    gdf : GeoDataFrame
        Contains the LineString features to be converted.

    Returns
    -------
    df : DataFrame
        Contains the shape information in a format suitable for GTFS.

    Example
    -------
    >>> import geopandas as gpd
    >>> import geo2shapes
    >>> gdf = gpd.read_file("my_file.geojson")
    >>> df = geo2shapes.convert(gdf)   
    """

    # Filter for features of type LineString
    gdf = gdf[gdf["geometry"].type == "LineString"]

    # Initialize lists to store data
    names = []
    latitudes = []
    longitudes = []
    sequence = []
    distance = []

    # Iterate through features (LineStrings)
    for idx, row in gdf.iterrows():
        name = row["name"]
        coordinates = row["geometry"].coords
        point0 = Point(coordinates[0])
        total_distance = 0
        counter = 0

        # Calculate the traveled distance during the trajectory
        for coord in coordinates:
            names.append(name)
            longitude, latitude = coord
            latitudes.append(latitude)
            longitudes.append(longitude)
            sequence.append(counter)
            point = Point(coord)
            geoseries = gpd.GeoSeries([point0, point], crs="EPSG:4326")
            # Convert the coordenates to Costa Rica system EPSG:5367 (meters)
            geoseries = geoseries.to_crs("EPSG:5367")
            # Calculate distance between both points
            points_distance = geoseries[0].distance(geoseries[1])
            total_distance += points_distance
            # Convert distance from meters to kilometers
            distance.append(round((total_distance / 1000), 3))
            point0 = point
            counter += 1

    # Create a DataFrame from the lists
    df = pd.DataFrame(
        {
            "shape_id": names,
            "shape_pt_lat": latitudes,
            "shape_pt_lon": longitudes,
            "shape_pt_sequence": sequence,
            "shape_dist_traveled": distance,
        }
    )

    return df


def validate(imput_file):
    """Validates a GeoJSON file containing LineString features.

    Parameters
    ----------
    imput_file : str
        (¿Qué entra aquí: WKT, archivo, .geojson?)

    Returns
    -------
    output_file : str
        Path to the output CSV file.

    """
    # Load Shape file
    gdf = gpd.read_file(imput_file)

    # Specify the Bounding box
    bounding_box = (
        9.947588,
        9.933921,
        -84.040216,
        -84.053926,
    )  # Bounding box of UCR, Costa Rica.

    # Obtain the road network graph within the bounding box
    G = ox.graph_from_bbox(
        bounding_box[0],
        bounding_box[1],
        bounding_box[2],
        bounding_box[3],
        network_type="all",
    )

    # Initialize the results dictionary
    results = {}

    # Iterate over each LineString in the GeoDataFrame
    for idx, row in gdf.iterrows():
        linestring = row["geometry"]

        # Convert the LineString to a GeoSeries of points
        points = linestring.representative_point()

        # Validate each segment of the LineString
        for i in range(len(points) - 1):
            # Get the current segment
            segment = LineString([points[i], points[i + 1]])

            # Validate if the segment intersects any road in the graph
            for edge in ox.graph_to_gdfs(G, nodes=False, edges=True).geometry:
                if segment.intersects(edge):
                    break
            else:
                # No intersection with any road was found
                results[idx] = False
                break
        else:
            # All segments are valid
            results[idx] = True

    # Print results
    def show_results(results):
        for idx, valid in results.items():
            print(f"LineString {idx} es válido: {valid}")

    return show_results
