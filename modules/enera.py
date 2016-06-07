#!/usr/bin/python
# coding=utf-8
import pytz
from flask import Blueprint, current_app, request, Response, redirect
from flask.ext.api import status
from modules import mongo, Clients, CmxRaw, Branch, CmxUrl
from bson import ObjectId
import datetime
from modules.handle_error import logger, issues
import pprint

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
        pprint.pprint(e)
        logger.error('Failed in enera.py', exc_info=True)
        issue = {
            "title": str(e),
            "platform": "cmx-env",
            "file": {
                "line": "",
                "path": str(request.url),
                "context": ""
            }
        }
        issues(e, issue)


@enera.route('/validate/<company>', methods=['POST'])
def validate(company):
    json = ''
    ap = ''
    try:
        if len(company) == 24:
            # CmxUrl(url=request.url, metodo=request.method).save()
            com = str(company)
            cliente = Clients.objects(id=ObjectId(com)).first()
            if not cliente:
                print('no encontro cliente')
                issues('url no valida no se encontro cliente', request.url, {"json": json, "ap": ap})
                logger.error('Failed in enera.py', exc_info=True)
                return 'no valido', status.HTTP_404_NOT_FOUND
            else:
                print('--')
                # CmxUrl(url=request.url, metodo=request.method, json=request.json).save()
                try:  # valida que sea un json
                    json_info = request.json
                except Exception as e:
                    # pprint.pprint('2')
                    issues('It is not JSON information', request.url, {"json": json, "ap": ap})
                    logger.error('Failed in enera.py', exc_info=True)
                    return {'error': 'information'}, status.HTTP_400_BAD_REQUEST
                # print('3')
                if json_info is None:  # valida que no este vacio
                    issues('It is JSON vacio', request.url, {"json": json, "ap": ap})
                    logger.error('Failed in enera.py', exc_info=True)
                    return {'error': ' information'}, status.HTTP_400_BAD_REQUEST
                print('se saca el branche')
                # se saca a que branch pertenece
                branch = Branch.objects(aps=json_info['data']['apMac']).first()
                if branch:
                    pprint.pprint(branch['id'])
                else:
                    print('no existe el ap en las branche')
                    logger.error('Failed in enera.py', exc_info=True)
                    issues('el ap no esta en una branche', request.url, {"json": json, "ap": ap})
                    return {'error': ' information'}, status.HTTP_400_BAD_REQUEST
                # bi = str(branch['id'])
                ap = {
                    "mac": json_info['data']['apMac'],
                    "tags": json_info['data']['apTags'],
                    "floors": json_info['data']['apFloors'],
                    "branche_id": branch['id'],
                }
                print('datos del ap')
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
                    lat = float(cel['location']['lat'])
                    lng = float(cel['location']['lng'])
                    unc = float(cel['location']['unc'])
                    location = {
                        "lat_lng": [lat, lng],
                        "unc": unc
                    }
                    json = cel['location']
                    print('location')
                    pprint.pprint(cel['location'])
                    print('------------------------')
                    CmxRaw(ap=ap, device=device, location=location).save()
                # logger.info('total de dispositivos captados, %s')
                print('total de dispositivos captados, %s' % len(devices))
                return 'ok', status.HTTP_200_OK
        else:
            return 'not found', status.HTTP_404_NOT_FOUND
    except Exception as e:
        pprint.pprint(e)
        logger.error('Failed in enera.py', exc_info=True)
        issues(e, request.url, {"json": json, "ap": ap})
    finally:  # print('por default')
        print('//////////////////////////////')
