from pycybos.cputil import *
try:
    from config import *
except Exception:
    USER = {'id': None, 'pwd': None, 'pwdcert': None}
    MONGOURL = 'mongodb://localhost:27017/'
from stock import Stock


def main():
    creon = Creon()
    creon.connect(id=USER['id'], pwd=USER['pwd'], pwdcert=USER['pwdcert'])

    stock = Stock()
    stock.insertNewCode()


if __name__ == "__main__":
    main()





