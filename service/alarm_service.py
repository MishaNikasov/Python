import requests

from manager import date_manager
from model.AlarmModel import AlarmModel

URL = "https://vadimklimenko.com/map/alarms.json?v="


def get_alarm():
    json = __get_alarm_response()
    vin_state = json['cities']['3159']
    update_date = json["updated_at"]
    alarm_model = AlarmModel(vin_state, update_date)
    return alarm_model


def __get_alarm_response():
    url = URL + str(date_manager.get_current_time_in_millis())
    alarm_request = requests.get(url)
    alarm_json_response = alarm_request.json()
    return alarm_json_response
