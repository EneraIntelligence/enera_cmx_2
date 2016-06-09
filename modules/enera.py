#!/usr/bin/python
# coding=utf-8
import datetime
import pprint

import pytz
from bson import ObjectId
from flask import Blueprint, request, Response
from flask.ext.api import status

from modules import Clients, CmxRaw, Branch
from modules.handle_error import logger, issues

prefix_module = 'enera'
enera = Blueprint(prefix_module, __name__)


@enera.route('/validate/<company>', methods=['GET'])
def tr(company):
    try:
        if len(company) == 24:
            # CmxUrl(url=request.url, metodo=request.method).save()
            com = str(company)
            cliente = Clients.objects(id=ObjectId(com)).first()
            if not cliente:
                print('no encontro cliente')
                issues('url no valida no se encontro cliente', request.url, {"json": "", "ap": ""})
                logger.error('Failed in enera.py', exc_info=True)
                return 'not found', status.HTTP_404_NOT_FOUND
            else:
                token = cliente.meraki['token']
                return Response(token, status.HTTP_200_OK, mimetype='text/plain')
        else:
            return 'not found', status.HTTP_404_NOT_FOUND
    except Exception as e:
        logger.error('Failed in enera.py', exc_info=True)
        issues(e, request.url, {"json": ""})


def diff_dates(date1, date2):
    # print(date1)
    # print(date2)
    return abs(date2 - date1).days


@enera.route('/validate/<company>', methods=['POST'])
def validate(company):
    json = ''
    ap = ''
    pull = []

    if len(company) == 24:
        # millis = int(round(time.time() * 1000))
        # print(millis)
        print(datetime.datetime.now())
        # CmxUrl(url=request.url, metodo=request.method).save()
        com = str(company)
        cliente = Clients.objects(id=ObjectId(com)).first()
        if not cliente:
            print('no encontro cliente')
            issues('url no valida no se encontro cliente', request.url, {"json": json, "ap": ap})
            # logger.error('Failed in enera.py', exc_info=True)
            return 'no valido', status.HTTP_404_NOT_FOUND
        else:
            # print('encontro cliente')
            # print(datetime.datetime.now())
            print('--')
            # CmxUrl(url=request.url, metodo=request.method, json=request.json).save()
            try:  # valida que sea un json
                json_info = request.json
                # pprint.pprint(json_info)
            except Exception as e:
                # pprint.pprint(request.json)
                issues('It is not JSON information', request.url, {"json": json, "ap": ap})
                logger.error('Failed in enera.py', exc_info=True)
                return {'error': 'information'}, status.HTTP_400_BAD_REQUEST
            # ------------      fin del if  --------------------------
            if json_info is None:  # valida que no este vacio
                issues('It is JSON empty', request.url, {"json": json, "ap": ap})
                # logger.error('Failed in enera.py', exc_info=True)
                return {'error': ' information'}, status.HTTP_400_BAD_REQUEST
            # ------------fin del if  --------------------------
            # se saca a que branch pertenece
            branch = Branch.objects(aps=json_info['data']['apMac']).first()
            if branch:
                print('si exite el ap' + str(datetime.datetime.now()))
                pprint.pprint(branch['id'])
            else:
                print('branch no encontrada')
                # logger.error('Failed in enera.py', exc_info=True)
                issues('el ap no esta en una branch', request.url, {"json": json, "ap": json_info['data']['apMac']})
                return {'error': ' information'}, status.HTTP_400_BAD_REQUEST
            ap = {
                "mac": json_info['data']['apMac'],
                "tags": json_info['data']['apTags'],
                "floors": json_info['data']['apFloors'],
                "branch_id": branch['id'],
            }
            devices = json_info['data']['observations']
            # tz = pytz.timezone('America/Mexico_City')  # se define la zona horaria
            device = {
                "mac": '',
                "ipv4": '',
                "ipv6": '',
                "last_seen": '',
                "ssid": '',
                "os": '',
                "manufacturer": '',
                "rssi": ''
            }
            location = {
                "lat_lng": [0, 0],
                "unc": 0
            }
            print('empieza el for' + str(datetime.datetime.now()))
            for cel in devices:  # Second Example
                device['mac'] = cel['clientMac']
                device['ipv4'] = cel['ipv4']
                device['ipv6'] = cel['ipv6']
                device['last_seen'] = datetime.datetime.fromtimestamp(cel['seenEpoch'], pytz.utc)
                device['ssid'] = cel['ssid']
                device['os'] = cel['os']
                device['manufacturer'] = cel['manufacturer']
                device['rssi'] = cel['rssi']

                if cel['location'] is not None:
                    lat = float(cel['location']['lat'])
                    lng = float(cel['location']['lng'])
                    unc = float(cel['location']['unc'])
                    location['lat_lng'] = [lat, lng]
                    location['unc'] = unc
                # print('------------------------')
                pull.append(CmxRaw(ap=ap, device=device, location=location))
            print('termina el for' + str(datetime.datetime.now()))
            CmxRaw.objects.insert(pull)
            print('termina el pull' + str(datetime.datetime.now()))
            print('total de dispositivos captados, %s' % len(devices))
            return 'ok', status.HTTP_200_OK
    else:
        print('codigo no valido')
        issues('codigo no valido', request.url, {"json": json, "ap": ap})
        return 'not found', status.HTTP_404_NOT_FOUND
