#!/usr/bin/python
# coding=utf-8
import pytz
from flask import Blueprint, current_app, request, Response, redirect
from flask.ext.api import status
from modules import mongo, Clients, CmxRaw, Branch, CmxUrl
from bson import ObjectId
import datetime

prefix_module = 'enera'
enera = Blueprint(prefix_module, __name__)


@enera.route('/validate/<company>', methods=['GET', 'POST'])
# @enera.route('/validate/<secret>', methods=['GET', 'POST'])
def validate(company):
    if len(company) == 24:
        # CmxUrl(url=request.url, metodo=request.method).save()
        com = str(company)
        cliente = Clients.objects(id=ObjectId(com)).first()
        if not cliente:
            print('no encontro nada')
            return 'no valido', status.HTTP_404_NOT_FOUND
        else:
            # print('no esta vacio')
            # print('--')
            if request.method == 'GET':
                # CmxUrl(url=request.url, metodo=request.method, data=request.data, json=request.json).save()
                # print('Hello, is post %s' % request.method)
                # CmxUrl(url=url, metodo=request.method).save()
                return Response(token, status.HTTP_200_OK, mimetype='text/plain')
            else:  # return 'Hello, is  %s' % request.method
                if request.method == 'POST':
                    # print('Hello, is post %s' % request.method)
                    # CmxUrl(url=request.url, metodo=request.method, json=request.json).save()
                    try:  # valida que sea un json
                        json_info = request.json
                    except Exception as e:
                        # pprint.pprint('2')
                        return {'error': 'It is not JSON information'}, status.HTTP_400_BAD_REQUEST
                    # pprint.pprint('3')
                    if json_info is None:  # valida que no este vacio
                        return {'error': 'It is not JSON information'}, status.HTTP_400_BAD_REQUEST
                    branch = Branch.objects(aps=json_info['data']['apMac']).first()  # se saca a que branch pertenece
                    ap = {
                        "mac": json_info['data']['apMac'],
                        "tags": json_info['data']['apTags'],
                        "floors": json_info['data']['apFloors'],
                        "branche_id": branch['id'],
                    }
                    devices = json_info['data']['observations']
                    # tz = pytz.timezone('America/Mexico_City')  # se define la zona horaria
                    for cel in devices:  # Second Example
                        device = {
                            "mac": cel['clientMac'],
                            "ipv4": cel['ipv4'],
                            "ipv6": cel['ipv6'],
                            "last_seen": datetime.datetime.fromtimestamp(cel['seenEpoch'], pytz.utc),
                            "ssid": cel['ssid'],
                            "os": cel['os'],
                            "manufacturer": cel['manufacturer'],
                            "rssi": cel['rssi'],
                        }
                        location = {
                            "lat_lng": [cel['location']['lat'], cel['location']['lng']],
                            "unc": cel['location']['unc']
                        }
                        CmxRaw(ap=ap, device=device, location=location).save()
                    # return 'total de device se guardaron, %s' % len(devices)
                    return 'ok', status.HTTP_200_OK
    else:
        print('no funciona')
        return 'no encontrado', status.HTTP_404_NOT_FOUND
