import logging
from modules import mongo, Issues
from logging.handlers import RotatingFileHandler, SMTPHandler
import pprint

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# try:

# except Exception as e:
# logger.error('Failed in enera.py', exc_info=True)

# create a RotatingFileHandler
file_error = logging.handlers.RotatingFileHandler('error.log', mode='a', maxBytes=10485760, encoding='utf8')
file_error.setLevel(logging.ERROR)

formato = logging.Formatter('**** %(asctime)s - %(pathname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')
file_error.setFormatter(formato)

logger.addHandler(file_error)

# create a smtphandler
mail_error = logging.handlers.SMTPHandler(mailhost=('smtp.mailgun.org', 587),
                                          credentials=('servers@enera-intelligence.mx', '@smtpenera2016'),
                                          fromaddr='servers@enera.mx',
                                          toaddrs='arosas@enera.mx',
                                          subject='Cmx Failed',
                                          )

mail_error.setLevel(logging.ERROR)

formato2 = logging.Formatter('**** %(asctime)s - %(pathname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')
mail_error.setFormatter(formato2)

logger.addHandler(mail_error)

# create a file handler
handler = logging.handlers.RotatingFileHandler('error.log')
handler.setLevel(logging.INFO)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


# logger.info('******************')

# logger.info('Hello baby')


def issues(error, url, datos):
    try:
        # print('hola')
        # pprint.pprint(error)
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
        # print(issue)
        Issues(lenguaje=lenguaje, issue=issue, datos=datos).save()
        print('se guardo el isue')
    except Exception as e:
        print('handle')
        pprint.pprint(e)

# class Handle:
#     def __init__(logging.handlers.BufferingHandler):

#
#
# def mail():
#     print('correo')
#     mail_handler = SMTPHandler(mailhost=('smtp.mailgun.org', 587),
#                                credentials=('servers@enera-intelligence.mx', '@smtpenera2016'),
#                                fromaddr='arosas@enera.mx',
#                                secure=('tls', 'enera-intelligence.mx', 'key-2eeac48a97fd2992ddb1e4c860d74470'),
#                                toaddrs='jose_asdrubal1@hotmail.com',
#                                subject='YourApplication Failed',
#                                )
#
#     # mail_handler.setLevel(logging.ERROR)
#     # application.logger.addHandler(mail_handler)
#     mail_handler.emit(record='prueba')
