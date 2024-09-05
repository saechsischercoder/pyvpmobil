from setuptools import setup

setup(name="pyvpmobil",
    version="1.1",
    description="An unoffical python package to interact with the API of the german timetable service VpMobil/Stundenplan24",
    author="BlueSchnabeltier",
    author_email="finn.ueschner@icloud.com",
    url="https://github.com/BlueSchnabeltier/pyvpmobil",
    packages=["pyvpmobil"],
    install_requires=["datetime", "requests", "xmltodict"],
)
