import Directory
import os
import threading
from logger import Logger

import time


def thingModified(self, listAllThingModified, lock):

    while listAllThingModified:

        with lock:
            try:
                elem = listAllThingModified.pop()
            except:
                break
        print(len(listAllThingModified))

        if elem:
            self.ftp.connect()
            if elem[0] == "file":
                if elem[1] == "deleteAndCreate":
                    self.ftp.remove_file(elem[3])
                    self.ftp.file_transfer(*elem[2:])
                elif elem[1] == "create":
                    self.ftp.file_transfer(*elem[2:])
            else:
                if elem[1] == "created":
                    self.ftp.create_folder(elem[2])

            self.ftp.disconnect()
