# pyVPMobil
pyVPMobil is an unoffical python package to interact with the API of the german timetable service VpMobil/Stundenplan24.

## Installation
To install pyVPMobil run:
```bash
pip install git+https://github.com/BlueSchnabeltier/pyvpmobil-x.git
```

## Usage
Here is an example script, where all functions are demonstrated:
```python
# Import necessary modules 
from pyVPMobil import School
from datetime import datetime, timedelta

# Create a datetime object
tomorrow = datetime.today() + timedelta(days=1)

# Initialize a school client
school = School(date=tomorrow, school_code=12345678, username="user", password="password")

# Print out the off days that VpMobil is aware of
print(school.off_days)

# Print out all the VpMobil data from your school in the json format
print(school.json_data)

# Print out the little extra text that is displayed below some school days in VpMobil
print(school.extra_info)

# Initialize a class
Class = school.Class(class_name="1a")

# Print the timetable of the class
print(Class.timetable)
```
