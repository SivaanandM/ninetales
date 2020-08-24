import sys
import os
sys.path.append(os.getcwd()[:os.getcwd().find("ninetales")+len("ninetales")])
from kafka import KafkaConsumer
from json import loads
import traceback
from src.loghandler.log_handler import LogHandler
from src.main.ninetales_objects import NinetalesObjects as ntaleObj
from src.writer.gsheet import GSheet

log = None
class Ninetales:
    kafka = ntaleObj.parser.get("kafka", "kafka_server") + ":" + ntaleObj.parser.get("kafka", "kafka_port")
    order_consumer = KafkaConsumer(bootstrap_servers=[str(kafka)],
                                       auto_offset_reset='earliest',
                                       enable_auto_commit=True,
                                       value_deserializer=lambda x: loads(x.decode('utf-8')))

    def __init__(self):
        try:
            LogHandler.set_logger("ninetales", name="ninetales")
            global log
            log = ntaleObj.log
            self.gsheet = GSheet(log)
            sheet_title = self.gsheet.newResultSheet()
            self.order_consumer.subscribe([str(ntaleObj.parser.get("common", "topicID"))])
            for message in self.order_consumer:
                try:
                    message = message.value
                    log.info("* Order Recevied")
                    log.info(message)
                    self.gsheet.appendRow(sheet_title, list(message.values()))
                except Exception as ex:
                    log.error(ex,traceback.format_exc())
        except Exception as ex:
            log.error(ex,traceback.format_exc())

if __name__ == '__main__':
    ninetales_obj = Ninetales()
