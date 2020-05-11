import requests
import datetime
import time
from dicttoxml import dicttoxml
import jwt

values = {
    'gps_login'        : 'toottk',
    'gps_password'     : 'DGvvAZ5zL',
    'gps_url'          : 'https://online.omnicomm.ru',
    'gps_jwt'          : '',
    'gps_refresh_key'  : '',
    'sleep_time'       : 15,
    'last_refresh_time': 0,
    'session_time'     : 500,
    'vehicle_xml_hat'  : "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><tns:vehicle xmlns:tns=\"http://schemes.omnicomm.ru/vehicle\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
    }
headers = {
    'accept'      : 'application/json',
    'Content-Type': 'application/json'
    }


def RequestWithRetry(req):
    if not values['gps_jwt']:
        print('Im in no gps_JWT')
        status = 0
        while status != 200:
            response = login_gps_system()
            status = response.status_code
            if status != 200:
                time.sleep(values['sleep_time'])
        values['last_refresh_time'] = time.localtime()
    elif values['gps_refresh_key'] or (time.localtime() - values['last_refresh_time']) < values['session_time']:
        print('Im in with GPS_refresh_key')
        status = 0
        while status != 200:
            response = refresh_gps_system()
            status = response.status_code
            if status != 200:
                time.sleep(values['sleep_time'])
        values['last_refresh_time'] = time.localtime()
    return req()


def login_gps_system():
    response = requests.post(url=f"{values['gps_url']}/auth/login?jwt=1", headers=headers,
                             data="{\"login\":\"%s\",\"password\":\"%s\"}" % (
                                 values['gps_login'], values['gps_password']))
    values['gps_jwt'] = response.json()['jwt']
    values['gps_refresh_key'] = response.json()['refresh']
    return response


def refresh_gps_system():
    h = headers.copy()
    h['Authorization'] = values['gps_refresh_key']
    response = requests.post(url=f"{values['gps_url']}/auth/login?jwt=1", headers=h)
    print(response.json())
    values['gps_jwt'] = response.json()['jwt']
    values['gps_refresh_key'] = response.json()['refresh']
    return response


def get_vehicle_statistic_on_period(vehicle_id, time_start=datetime.datetime.now(), time_end=datetime.datetime.now()):
    h = headers.copy()
    h['Authorization'] = "JWT " + values['gps_jwt']
    params = {
        'timeBegin' : time_start.timestamp(),
        'timeEnd'   : time_end.timestamp(),
        'vehicles'  : f'[{vehicle_id}]',
        'dataGroups': "[mw,fuel,mnt]"
        }
    response = requests.get(url=f"{values['gps_url']}/ls/api/v1/reports/statistics", headers=h,
                            params=params)
    return response


def get_vehicle_state(vehicle):
    h = headers.copy()
    h['Authorization'] = "JWT " + values['gps_jwt']
    h.pop('Content-Type')
    response = requests.get(url="%s/ls/api/v1/vehicles/%d/state" % (values['gps_url'], vehicle), headers=h)
    return response


def format_string(xmlbuf):
    xmlbody = ""
    for x in str(xmlbuf):
        if x == '\"':
            xmlbody += '\\\\\\' + x
        elif x == '/':
            xmlbody += "\\\\" + x
        else:
            xmlbody += x
    return xmlbody


def add_new_vehicle(dictionary):
    h = headers.copy()
    h['Authorization'] = "JWT " + values['gps_jwt']
    wanted_keys = ['id']
    new_dict = {key: value for key, value in dictionary.items() if key in wanted_keys}
    for x in wanted_keys:
        dictionary.pop(x)
    xmlbuf1 = dicttoxml(new_dict, root=False, attr_type=False)
    xmlbuf2 = dicttoxml(dictionary, root=False, attr_type=False)
    xmlbody1 = format_string(xmlbuf1)
    xmlbody2 = format_string(xmlbuf2)
    payload = "{\"xmlProfile\":" + f"\"{format_string(values['vehicle_xml_hat'])}{xmlbody1[2:-1]}\\r\\n{xmlbody2[2:-1]}" + "<\\/tns:vehicle>\"}"
    response = requests.post(url='%s/ls/api/v1/vehicles?login=%s' % (values['gps_url'], values['gps_login']), headers=h,
                             data=payload)
    return response


def get_jwt_exp():
    encoded = values['gps_jwt']
    decoded = jwt.decode(encoded, 'secret', algorithms='HS256')
    return decoded
