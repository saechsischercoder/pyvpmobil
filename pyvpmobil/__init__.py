"""
School Timetable API Client

A Python client for accessing school timetables from stundenplan24.de
"""

import requests
from xmltodict import parse
from base64 import b64encode
from datetime import datetime
from typing import List, Dict, Optional, Any


# Custom Exceptions
class VPMobilError(Exception):
    """Base exception for VPMobil related errors"""
    pass


class InvalidClassName(VPMobilError):
    """Raised when an invalid class name is provided"""
    pass


class AuthenticationError(VPMobilError):
    """Raised when authentication fails"""
    pass


class DataNotFoundError(VPMobilError):
    """Raised when requested data is not found"""
    pass


class SchoolTimetable:
    """
    Main class for accessing school timetable data from stundenplan24.de
    
    Attributes:
        json_data: Parsed JSON data from the XML response
        off_days: List of free days/holidays
        extra_info: Additional information from the timetable
    """
    
    def __init__(self, date: datetime, school_code: int, username: str, password: str):
        """
        Initialize the SchoolTimetable client
        
        Args:
            date: The date for which to fetch the timetable
            school_code: Unique school identifier
            username: Authentication username
            password: Authentication password
            
        Raises:
            AuthenticationError: If credentials are invalid
            DataNotFoundError: If timetable data is not available
            VPMobilError: For other API-related errors
        """
        self._validate_inputs(date, school_code, username, password)
        
        self.date = date
        self.school_code = school_code
        self._auth_header = self._create_auth_header(username, password)
        
        # Fetch and parse data
        self._fetch_data()
        self._parse_data()
    
    def _validate_inputs(self, date: datetime, school_code: int, username: str, password: str) -> None:
        """Validate input parameters"""
        if not isinstance(date, datetime):
            raise ValueError("Date must be a datetime object")
        if not isinstance(school_code, int) or school_code <= 0:
            raise ValueError("School code must be a positive integer")
        if not username or not password:
            raise ValueError("Username and password cannot be empty")
    
    def _create_auth_header(self, username: str, password: str) -> str:
        """Create Basic Authentication header"""
        credentials = f"{username}:{password}"
        encoded_credentials = b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    def _fetch_data(self) -> None:
        """Fetch XML data from the API"""
        url = f"https://www.stundenplan24.de/{self.school_code}/mobil/mobdaten/PlanKl{self.date.strftime('%Y%m%d')}.xml"
        
        try:
            response = requests.get(
                url, 
                headers={"Authorization": self._auth_header},
                timeout=10
            )
            response.raise_for_status()
            self.xml_data = response.text
            
        except requests.exceptions.RequestException as e:
            raise VPMobilError(f"Failed to fetch data: {str(e)}")
        
        # Check for common error responses
        if "Seite nicht gefunden" in self.xml_data:
            raise DataNotFoundError(
                "Timetable data not found. This could be due to: "
                "invalid credentials, no school on the given date, "
                "or timetable not yet available for the requested date."
            )
    
    def _parse_data(self) -> None:
        """Parse XML data and extract relevant information"""
        try:
            parsed_data = parse(self.xml_data)
            self.json_data = parsed_data["VpMobil"]
        except Exception as e:
            raise VPMobilError(f"Failed to parse XML data: {str(e)}")
        
        # Parse free days
        self.off_days = self._parse_off_days()
        
        # Parse extra information
        self.extra_info = self._parse_extra_info()
    
    def _parse_off_days(self) -> List[datetime]:
        """Parse and return list of free days"""
        try:
            free_days_data = self.json_data.get("FreieTage", {}).get("ft", [])
            if isinstance(free_days_data, str):
                free_days_data = [free_days_data]
            
            return [
                datetime.strptime(date, "%y%m%d") 
                for date in free_days_data
            ]
        except (KeyError, ValueError):
            return []
    
    def _parse_extra_info(self) -> Optional[str]:
        """Parse and return extra information"""
        try:
            zi_zeile = self.json_data["ZusatzInfo"]["ZiZeile"]
            if isinstance(zi_zeile, list):
                return "\n".join(zi_zeile)
            return zi_zeile
        except KeyError:
            return None
    
    def get_class_timetable(self, class_name: str) -> 'ClassTimetable':
        """
        Get timetable for a specific class
        
        Args:
            class_name: Name of the class
            
        Returns:
            ClassTimetable object
            
        Raises:
            InvalidClassName: If the class name doesn't exist
        """
        return ClassTimetable(class_name, self.json_data)
    
    def get_available_classes(self) -> List[str]:
        """Get list of all available class names"""
        try:
            classes = self.json_data.get("Klassen", {}).get("Kl", [])
            return [school_class["Kurz"] for school_class in classes]
        except (KeyError, TypeError):
            return []


class ClassTimetable:
    """
    Represents a timetable for a specific class
    
    Attributes:
        class_name: Name of the class
        timetable: List of lessons with details
    """
    
    def __init__(self, class_name: str, json_data: Dict[str, Any]):
        """
        Initialize ClassTimetable
        
        Args:
            class_name: Name of the class
            json_data: Parsed JSON data from SchoolTimetable
            
        Raises:
            InvalidClassName: If the class name doesn't exist
        """
        self.class_name = class_name.lower()
        self._find_class_data(json_data)
        self._parse_timetable()
    
    def _find_class_data(self, json_data: Dict[str, Any]) -> None:
        """Find and store class data"""
        try:
            classes = json_data["Klassen"]["Kl"]
            for school_class in classes:
                if school_class["Kurz"].lower() == self.class_name:
                    self._class_json = school_class
                    return
            
            raise InvalidClassName(f"Class '{self.class_name}' does not exist")
            
        except KeyError:
            raise VPMobilError("Invalid data structure: missing class information")
    
    def _parse_timetable(self) -> None:
        """Parse timetable data into a structured format"""
        try:
            lessons = self._class_json["Pl"]["Std"]
            if not isinstance(lessons, list):
                lessons = [lessons]
            
            self.timetable = []
            for lesson in lessons:
                self.timetable.append({
                    "period": lesson.get("St", ""),
                    "start_time": lesson.get("Beginn", ""),
                    "end_time": lesson.get("Ende", ""),
                    "subject": lesson.get("Fa", ""),
                    "teacher": lesson.get("Le", ""),
                    "classroom": lesson.get("Ra", ""),
                    "info": lesson.get("If", "")
                })
                
        except (KeyError, TypeError) as e:
            raise VPMobilError(f"Failed to parse timetable: {str(e)}")
    
    def get_lessons_by_period(self, period: str) -> List[Dict[str, str]]:
        """Get all lessons for a specific period"""
        return [lesson for lesson in self.timetable if lesson["period"] == period]
    
    def get_lessons_by_subject(self, subject: str) -> List[Dict[str, str]]:
        """Get all lessons for a specific subject"""
        return [lesson for lesson in self.timetable if subject.lower() in lesson["subject"].lower()]
