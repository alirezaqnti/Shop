from zeep import Client

try:
    from core.Private import ZARINPAL_MERCHANT as MERCHANT
except:
    MERCHANT = ""


def GetClient():
    client = Client("https://www.zarinpal.com/pg/services/WebGate/wsdl")
    try:
        return client
    except:
        client = ""
        return client
