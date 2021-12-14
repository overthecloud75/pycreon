from cybos.util import *

try:
    from config import USER
except Exception:
    USER = {'id': None, 'pwd': None, 'pwdcert': None}
from stock import Stock


def main():
    creon = Creon()
    creon.connect(id=USER['id'], pwd=USER['pwd'], pwdcert=USER['pwdcert'])

    stock = Stock()
    stock.insertNewCode()
    stock.insertNewChart()


if __name__ == "__main__":
    main()





