from zeep import Client


MERCHANT = "896002e4-8b1f-4059-aa25-0008ebf970cb"


def GetClient():
    client = Client("https://www.zarinpal.com/pg/services/WebGate/wsdl")
    try:
        return client
    except:
        client = ""
        return client
