import datetime
import string
import os
import time
import NetworkManager
import dbus
import requests , json
from pyric import pyw
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core import n_m, info_wlan
from model_location import Location, Base
from core.loger import Loger

BASE = os.path.dirname(__file__)

texto = string.Template("""
     Wifi State          
--------------------------------------------------------------                
Wifi Interface : $wifi
Card Estate    : ${card} 
Card Mac       : ${mac} 
Driver         : $driver
Chipset        : $chip
Manufacturer   : ${man}
-----------------------------
Avaliable Conex: ${con}
---------------------------------------------------------------------------------               
               """)


LOGPATH = '/var/log/journal/vplocation/'
DATABASE_PATH = BASE + "/location_vp.db"

log = Loger(os.path.join(BASE, 'log_vozplus.log'), __name__)         # log class

   ###### DB  SQlite
engine = create_engine('sqlite:////' + DATABASE_PATH)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

TOKEN = None
API_KEY = 'AIzaSyDGpqb7tcxGRzNorjOPQFRZfbKH8PxrtUg'



wifi_nearby = []
list_info = list()


def main():
  try:
      print("path_db", DATABASE_PATH)

      execute()
      while True:
          time.sleep(1800)
          execute()
  except KeyboardInterrupt:
      print('FINISH')


def execute():
   try:
       log.console_info('Executed() method running  : ' + __name__)
       info_wlan.active_con()
       if get_mac_from_this_equip() != None:

           log.console_info('Retrieving Mac Adrees From Wifi Card  : ' + __name__)
           wifi_scan()
       print(is_internet_there())
       if is_internet_there() == True:
             get_all_records()
       maximun_records()
   except dbus.exceptions.DBusException as error:

       log.console_info('There is not Wifi Card  : {}'.format(error) + __name__)
   except requests.exceptions.ConnectionError as error:
       log.console_info('There is not Internet connection  : {}'.format(error) + __name__)


def get_all_info():

    log.console_info('Retrieving All Info from Wifi Nearby : ' + __name__)
    for dev in NetworkManager.NetworkManager.GetDevices():
        if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:

            continue
        for ap in dev.GetAllAccessPoints():
            info = dict()
            info['macAddress'] = str(ap.HwAddress)
            info['signalStrength'] = '-' + str(ap.Strength)
            info['signalToNoiseRatio'] = '0'
            list_info.append(info)
    data_to_send = {'usermac': get_mac_from_this_equip(), 'created':created_at(), 'wifiAccessPoints': list_info}
    log.console_success('Success All Info from Wifi Nearby : ' + __name__)

    return data_to_send



def  to_json(result):

    data = None
    try:
       data = json.dumps(result)

       log.console_info('Parsing All Info from Wifi Nearby  to Json: ' + __name__)

    except TypeError as e:
        log.console_info('Except Riased, Parsing All Info from Wifi Nearby  to Json: ' + __name__)
    else:
        log.console_success('Succes Parsing All Info from Wifi Nearby  to Json: ' + __name__)

    return data


def get_mac_from_this_equip():

    try:

       log.console_info('Retrieving Mac Adrees From Wifi Card ( Inside Method )  : ' + __name__)
       wlan = (pyw.winterfaces())[0]
       card = pyw.getcard(wlan)
       mac =  pyw.ifinfo(card)
       m = None
       m = mac['hwaddr']
       log.console_success('Success Retrieving Mac Adrees From Wifi Card ( {} )  : ' .format(error)+ __name__)
       return m

    except UnboundLocalError as error:
        log.log_warning('Except raised, Retrieving Mac Adrees From Wifi Card ( {} )  : '.format(error) + __name__)
        return False
    except IndexError as error:
        log.log_warning('Except raised, Retrieving Mac Adrees From Wifi Card ( {} )  : '.format(error) + __name__)
        return False
    except dbus.exceptions.DBusException as error:
        log.log_warning('Except raised, Retrieving Mac Adrees From Wifi Card ({})  : '.format(error) + __name__)
        return False

def created_at():

    dt = datetime.datetime.now()
    hora = "{}-{}-{}  {}:{}:{}".format(dt.day, dt.month, dt.year, dt.hour, dt.minute , dt.second)
    return hora


def wifi_scan():

    if NetworkManager.NetworkManager.WirelessEnabled != True and NetworkManager.NetworkManager.WirelessHardwareEnabled != True:
        iswifihere = ((n_m.list_())[0])[1]
        n_m.activate(iswifihere)

        print("%-30s %s" % ("Wireless enabled:", NetworkManager.NetworkManager.WirelessEnabled))
        print("%-30s %s" % ("Wireless hw enabled:", NetworkManager.NetworkManager.WirelessHardwareEnabled))

    elif get_mac_from_this_equip() != False:
        is_wifi_present()
        location = Location(ssid=str(get_mac_from_this_equip()), data=str(to_json(get_all_info())))
        add_to_db(location)

    elif info_wlan.available_con() != True:
         log.console_warning("Turn On wifi pls")


def delete_records(ssid):

    session.query(Location.ssid == ssid).delete()
    session.commit()


def add_to_db(location):

    session.add(location)
    session.commit()


def get_all_records():

    i = 0

    records = session.query(Location).yield_per(1)
    for r in records:
        location = json.loads(r.data)
        #location = {'considerIp': 'true', 'wifiAccessPoints': location['wifiAccessPoints']}
        #location = json.dumps(location)
        print("google json : ", location)
        i += 1
        if i > 5:
           sendto_api(r.ssid, r.created, r.data)
        if i > 150:
            delete_records(get_mac_from_this_equip())
        print("({})".format(i), r.data, end='\n')


def maximun_records():

    records = session.query(Location).yield_per(1)
    i = 0
    for  r in records:
       i += 1

    if i > 300:
        delete_records(get_mac_from_this_equip())


def is_wifi_present():
    wlan = pyw.winterfaces()

    if len(wlan) >= 1:
        interface = wlan[0]
        if pyw.isinterface(interface):
            card = pyw.getcard(interface)
            info = pyw.ifinfo(card)
            if pyw.isup(card) is not True:
               print("Turn On wifi Actual estate:", pyw.isup(card))
               wifi_info = {'wifi': interface,
                            'card': pyw.isup(card),
                            'mac': pyw.macget(card),
                            'driver': info.get('driver'),
                            'chip': info.get('chipset'),
                            'man': info.get('manufacturer'),
                            'con': to_json(get_all_info())}
               print(texto.safe_substitute(wifi_info))


            else:
               wifi_info = {'wifi': interface,
                            'card': pyw.isup(card),
                            'mac': pyw.macget(card),
                            'driver': info.get('driver'),
                            'chip': info.get('chipset'),
                            'man': info.get('manufacturer'),
                            'con': to_json(get_all_info())}
               print(texto.safe_substitute(wifi_info))

    else:
         print('wifi no encobtrado')


def is_internet_there():
    internet = pyw.interfaces()
    internet = internet[0]

    return pyw.isinterface(internet)





def create_user():

    data = {
        "username": str(get_mac_from_this_equip()).replace(':', ''),
        "password": str(get_mac_from_this_equip())
    }

    headers = {"Content-Type":"application/json"}
    try:
       response = requests.post(url= 'http://153.92.209.82:8000/api/users/', json= data, headers= headers)
       return response
    except  requests.exceptions.ConnectionError as error:
        log.console_warning("Http error connection{}".format(error))
        return False


def get_autho_token():
    create_user()

    data = {
            "username": str(get_mac_from_this_equip()).replace(':', ''),
            "password": str(get_mac_from_this_equip())
           }

    data_json = json.dumps(data)
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url='http://153.92.209.82:8000/auth/', json=data, headers=headers)
    except  requests.exceptions.ConnectionError as error:
        log.console_warning("Http error connection{}".format(error))
        return False

    try:
       token = response.json()
       token = token['token']
    except requests.exceptions.RequestException:
       print(str(response))
       return False

    return token


def sendto_api(ssid,dates,data):

    TOKEN = get_autho_token()
    lap = {
            "mac": str(ssid),
            "date": str(dates),
            "data": str(data)
            }

    token = 'Token {}'.format(TOKEN)
    headers = {"Authorization": token}
    print(headers)
    try:
        response = requests.post(url='http://153.92.209.82:8000/api/laptop/', json=lap, headers=headers)
        return response
    except  requests.exceptions.ConnectionError as error:
        log.console_warning("Http error connection{}".format(error))
        return False




if __name__ == '__main__':
    main()
