from requests import get
from .exceptions import *
from xmltodict import parse
from base64 import b64encode
from datetime import datetime

class School:
    def __init__(self, date: datetime, school_code: int, username: str, password: str):
        auth = b64encode(f"{username}:{password}".encode()).decode()
        self.xml_data = get(f"https://www.stundenplan24.de/{school_code}/mobil/mobdaten/PlanKl{date.strftime('%Y%m%d')}.xml", headers={"Authorization": f"Basic {auth}"}).text

        if "Seite nicht gefunden" in self.xml_data:
            raise VPMobilError("Either school isn't in on the given date, the timetable isn't there yet for the reqeusted date or the credentials provided are invalid")

        global json_data
        json_data = parse(self.xml_data)["VpMobil"]
        self.json_data = json_data
        self.off_days = [datetime.strptime(date, "%y%m%d") for date in self.json_data["FreieTage"]["ft"]]

        try:
            self.extra_info = "\n".join(line for line in self.json_data["ZusatzInfo"]["ZiZeile"])

        except KeyError:
            self.extra_info = None

    class Class:
        def __init__(self, class_name):
            class_json = None

            for Class in json_data["Klassen"]["Kl"]:
                if Class["Kurz"] == class_name.lower():
                    class_json = Class

                    break

            if class_json == None:
                raise InvalidClassName("The class you input does not exist.")

            self.timetable = [{"count": lesson["St"], "begin": lesson["Beginn"], "end": lesson["Ende"], "subject": lesson["Fa"], "teacher": lesson["Le"], "classroom": lesson["Ra"], "info": lesson["If"]} for lesson in class_json["Pl"]["Std"]]
