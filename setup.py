from setuptools import setup

setup(name="pyvpmobil",
    description="Python API client for German school timetable services VpMobil/Stundenplan24 with comprehensive data access",
    author="BlueSchnabeltier",
    url="https://github.com/saechsischercoder/pyvpmobil",
    packages=["pyvpmobil"],
    install_requires=["datetime", "requests", "xmltodict"],
)
