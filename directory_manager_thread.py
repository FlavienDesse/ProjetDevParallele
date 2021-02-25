from talk_to_ftp import TalkToFTP
import os
from pathlib import Path
import time
import traceback

_TIME_SLEEP = 0.002

"""
    Principal function 
    it is this function which is called by our threads.
    Each thread shares a list of all the tasks to be performed (creation, deletion, update).
    When a thread is available, it takes an element in our list and execute the action
"""


def ThingModified(self, listAllThingModified, lock, ftp_website):
    # we loop until our list is empty
    while listAllThingModified:
        # Only one thread at a time takes an element in our list.
        with lock:
            try:
                # we unstack the last element of our list
                # elem => [ type of the element ( file or directory ) ,
                #           what we have to do ( create , update , delete ) ,
                #           path of the file ,
                #           optionnal : full path ,
                #           optionnal : file name
                elem = listAllThingModified.pop()
            except:
                break


        ftp = TalkToFTP(ftp_website)

        if elem:
            # connection to the FTP
            ftp.connect()

            # we check if our element is a file
            if elem[0] == "file":
                # if we have to update the file
                if elem[1] == "updateAndCreate":
                    try:
                        ftp.remove_file(elem[3])
                        ftp.file_transfer(*elem[2:])
                    except:
                        print('\033[33m' + "Cannot update and create " + elem[2])

                # if we have to create the file
                elif elem[1] == "create":
                    try:
                        ftp.file_transfer(*elem[2:])
                    except:
                        print('\033[33m' + "Cannot create file")
                # if we have to delete the file
                elif elem[1] == "delete":
                    try:
                        ftp.remove_file(elem[2])
                    except:
                        print('\033[33m' + "Cannot delete file" + elem[2])
                        traceback.print_exc()

            else:
                # if we have to create the directory
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
                # if we have to delete the directory
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
