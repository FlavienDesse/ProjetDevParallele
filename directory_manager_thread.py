import Directory
import os
import threading

def thingModified(self, listAllThingModified, lock):
    while listAllThingModified:
        with lock:
            elem = listAllThingModified.pop()
        if elem[0] == "file":
            if elem[1] == "deleteAndCreate":
                self.ftp.remove_file(elem[3])
                self.ftp.file_transfer(elem[2], elem[3], elem[4])
            elif elem[1] == "create":
                self.ftp.file_transfer(elem[2], elem[3], elem[4])
        else:
            if elem[1] == "created":
                self.ftp.create_folder(elem[2])


