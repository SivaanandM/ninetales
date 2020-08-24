import os
from configparser import ConfigParser


class NinetalesObjects(object):
    parser = ConfigParser()
    os.environ['NINETALES_CONFIG'] = os.getcwd()[:os.getcwd().find("ninetales") + len("ninetales")] + '/config/ninetales.ini'
    parser.read(os.getenv("NINETALES_CONFIG"))
    ninetales_path = os.getcwd()[:os.getcwd().find("ninetales") + len("ninetales")]
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(str(ninetales_path), parser.get("common", "gkey"))
    log = None
    result_sheet_head = ["Algo", "Symbol", "Condition",
                         "Time", "Price", "Position",
                         "Net", "Trade"]