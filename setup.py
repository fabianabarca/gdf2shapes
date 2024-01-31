from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Convert a LineString geometry to a GTFS shapes.txt format."
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()


setup(
    name="geo2shapes",
    packages=find_packages(include=["geo2shapes"]),
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Fabián Abarca and José Andrés Rodríguez",
    license="MIT",
    install_requires=[
        "pandas",
        "geopandas",
        "shapely",
        "osmnx",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
    ],
)
