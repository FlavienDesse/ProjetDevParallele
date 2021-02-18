from talk_to_ftp import TalkToFTP
import os

def thingModified(self, listAllThingModified, lock, ftp_website):
    while listAllThingModified:
        with lock:
            try:
                elem = listAllThingModified.pop(0)
                # print(elem)
            except:
                break

        ftp = TalkToFTP(ftp_website)

        if elem:
            ftp.connect()
            if elem[0] == "file":
                if elem[1] == "updateAndCreate":
                    ftp.remove_file(elem[3])
                    ftp.file_transfer(*elem[2:])
                elif elem[1] == "create":
                    ftp.file_transfer(*elem[2:])
                elif elem[1] == "delete":
                    ftp.remove_file(elem[2])
            else:
                if elem[1] == "create":
                    ftp.create_folder(elem[2])                   
                elif elem[1] == "delete":
                    ftp.remove_folder(elem[2])

            ftp.disconnect()
