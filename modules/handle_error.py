import logging
from modules import mongo, Issues
from logging.handlers import RotatingFileHandler, SMTPHandler
import pprint


def issues(error, url):
    try:
        print('hola')
        pprint.pprint(error)
        lenguaje = {'lenguaje': 'python',
                    "plataforma": "cmx"
                    }
        issue = {
            "title": str(error),
            "platform": "cmx-env",
            "file": {
                "line": "",
                "path": str(url),
                "context": ""
            }
        }
        print(issue)
        # pprint.pprint({data})
        Issues(lenguaje=lenguaje, issue=issue).save()
        print('se supone guardo')
    except Exception as e:
        print('handle')
        pprint.pprint(e)
        # class Handle:
        #     def __init__(logging.handlers.BufferingHandler):
