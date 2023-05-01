from setuptools import setup

setup(name="pyVPMobil",
    version="1.0",
    description="An unoffical python package to interact with the API of the german timetable service VpMobil/Stundenplan24",
    author="BlueSchnabeltier",
    author_email="finn.ueschner@icloud.com",
    url="https://github.com/BlueSchnabeltier/pyVPMobil",
    packages=["pyVPMobil"],
    install_requires=["datetime", "requests", "xmltodict"],
)
