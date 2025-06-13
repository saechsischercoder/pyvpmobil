# School Timetable API Client

**Professional Python client for stundenplan24.de mobile API - streamlined school schedule access with comprehensive data parsing**

Access German school timetables programmatically with this robust API client. Built for developers who need reliable integration with stundenplan24.de's mobile platform, featuring type-safe operations and intelligent error handling.

## ✨ Key Features

### **📅 Comprehensive Schedule Access**
- **Date-specific timetables** - fetch schedules for any date
- **Class-based filtering** - get timetables for specific classes
- **Multi-class support** - access all available classes in your school

### **🏫 Extended School Information**
- **Holiday tracking** - automatic free day and holiday detection
- **School announcements** - access additional institutional information
- **Real-time updates** - always current with the latest schedule changes

### **🛡️ Professional-Grade Reliability**
- **Type-safe operations** - comprehensive type hints and validation
- **Robust error handling** - specific exceptions for different failure scenarios
- **Authentication management** - secure credential handling

## 🚀 Quick Installation

### **Direct Installation (Recommended)**
```bash
pip install git+https://github.com/BlueSchnabeltier/pyvpmobil.git
```

## 📖 Usage Examples

### **Basic Timetable Access**
```python
from datetime import datetime
from school_timetable import SchoolTimetable

# Initialize client
school = SchoolTimetable(
    date=datetime(2025, 6, 13),
    school_code=12345,
    username="your_username",
    password="your_password"
)

# Get available classes
classes = school.get_available_classes()
print("Available classes:", classes)

# Fetch specific class timetable
timetable = school.get_class_timetable("10a")
print("Today's schedule:", timetable.timetable)
```

### **Advanced Schedule Analysis**
```python
from school_timetable import SchoolTimetable, InvalidClassName

try:
    school = SchoolTimetable(
        date=datetime(2025, 6, 13),
        school_code=12345,
        username="student123",
        password="secure_password"
    )
    
    # Get class schedule
    class_schedule = school.get_class_timetable("10a")
    
    # Display formatted schedule
    for lesson in class_schedule.timetable:
        print(f"🕐 Period {lesson['period']}: {lesson['subject']}")
        print(f"   📍 {lesson['classroom']} | 👨‍🏫 {lesson['teacher']}")
        print(f"   ⏰ {lesson['start_time']} - {lesson['end_time']}")
        print()
    
    # Check for holidays
    if school.off_days:
        print("🎉 Upcoming free days:", school.off_days)
    
    # School announcements
    if school.extra_info:
        print("📢 School info:", school.extra_info)
        
except InvalidClassName as e:
    print(f"❌ Class not found: {e}")
except Exception as e:
    print(f"🚨 Error: {e}")
```

## 🔧 API Reference

### **SchoolTimetable Class**

Main interface for school data access.

#### **Constructor**
```python
SchoolTimetable(date: datetime, school_code: int, username: str, password: str)
```

**Parameters:**
- `date` - Target date for timetable retrieval
- `school_code` - Your school's unique identifier
- `username` - Authentication username
- `password` - Authentication password

#### **Methods**
- `get_class_timetable(class_name: str) -> ClassTimetable` - Retrieve specific class schedule
- `get_available_classes() -> List[str]` - List all accessible classes

#### **Properties**
- `off_days` - Holiday and free day information
- `extra_info` - Additional school announcements
- `json_data` - Raw API response data

### **ClassTimetable Class**

Represents individual class schedules with filtering capabilities.

#### **Methods**
- `get_lessons_by_period(period: str) -> List[Dict]` - Filter by time period
- `get_lessons_by_subject(subject: str) -> List[Dict]` - Filter by subject

#### **Properties**
- `timetable` - Complete lesson list with details
- `class_name` - Associated class identifier

## ⚠️ Error Handling

### **Custom Exceptions**
- `VPMobilError` - Base exception for all API-related errors
- `InvalidClassName` - Specified class doesn't exist
- `AuthenticationError` - Credential validation failed
- `DataNotFoundError` - Requested information unavailable

### **Best Practices**
```python
from school_timetable import (
    SchoolTimetable, 
    InvalidClassName, 
    AuthenticationError,
    DataNotFoundError
)

try:
    # Your API calls here
    pass
except AuthenticationError:
    print("Check your credentials")
except InvalidClassName:
    print("Verify class name spelling")
except DataNotFoundError:
    print("No data for selected date")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 📋 Requirements

- **Python 3.7+** - Modern Python version required
- **requests** - HTTP client library
- **xmltodict** - XML parsing utilities

## 🔒 Security Notes

- Store credentials securely (environment variables recommended)
- Validate school codes before API calls
