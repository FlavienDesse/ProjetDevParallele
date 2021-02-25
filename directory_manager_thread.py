from talk_to_ftp import TalkToFTP
import os
from pathlib import Path
import time
import traceback

_TIME_SLEEP = 0.002


def ThingModified(self, listAllThingModified, lock, ftp_website):
    while listAllThingModified:
        with lock:
            try:
                elem = listAllThingModified.pop()
            except:
                break

        ftp = TalkToFTP(ftp_website)

        if elem:
            ftp.connect()
            if elem[0] == "file":
                if elem[1] == "updateAndCreate":
                    try:
                        ftp.remove_file(elem[3])
                        ftp.file_transfer(*elem[2:])
                    except:
                        print('\033[33m' + "Cannot update and create " + elem[2])
                elif elem[1] == "create":
                    try:
                        ftp.file_transfer(*elem[2:])
                    except:
                        print('\033[33m' + "Cannot create file")

                elif elem[1] == "delete":
                    try:
                        ftp.remove_file(elem[2])
                    except:
                        print('\033[33m' + "Cannot delete file" + elem[2])
                        traceback.print_exc()

            else:
                if elem[1] == "create":
                    try:
                        path = Path(elem[2])
                        error = False
                        while path != path.parent:
                            if not os.path.exists(path.parent):
                                error = True
                                break
                            path = path.parent

                        if not error:
                            if not ftp.if_exist(elem[2], ftp.get_folder_content(elem[2].rsplit(os.path.sep, 1)[0])):
                                ftp.create_folder(*elem[2:])
                        else:
                            time.sleep(_TIME_SLEEP)
                            listAllThingModified.insert(0, elem)
                    except:
                        print('\033[33m' + "Cannot create dir" + elem[2])

                elif elem[1] == "delete":
                    try:
                        if not os.listdir(elem[2]):
                            ftp.remove_folder(elem[2])
                        else:
                            time.sleep(_TIME_SLEEP)
                            listAllThingModified.insert(0, elem)
                    except:
                        print('\033[33m' + "Cannot delete dir" + elem[2])

            ftp.disconnect()
