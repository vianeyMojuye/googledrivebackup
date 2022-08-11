#!/usr/bin/python


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil, os, multiprocessing, json

gauth = GoogleAuth()
drive = GoogleDrive(gauth)


def upload_files(folders, records):
    #this function is used to upload files to google drive
    # this.folders : list of folders to traverse , this.records: list of folders to be deleted
    #@except : print message if an error is found during file uploading

    try :
        for (root,dirs,files) in os.walk('record', topdown=True):
            for i in folders :
                #initial the check value to 0 when we start parsing a folder
                # check.value = 0
                #since our folder is like folder_name-file_name:
                # Here we check if we've found a folder present in our folder name dictionary
                ab = str((root.split("-")[0])).split("\\") #for windows System
                ab1 = str((root.split("-")[0])).split("/") #for Linux System

                # ab = "asasasas"
                # ab1 = "asasasas"

                # print(folders[i], " -- ",ab[-1])
                if folders[i] == ab[-1]  or folders[i] == ab1[-1]:
                    for file_name in files :
                        # print(file_name)
                        if file_name.endswith(".mp4") :
                            # print(file_name)
                            #absolute path of the source file
                            source = os.path.join(root, file_name)
                            # print("Root : ", root)
                            #Move the file to google drive
                            # 1- Create the file into google drive location with the same name present on our machine
                            file1 = drive.CreateFile({'parents': [{'id': i}], 'title': file_name,"mimeType":"video/mp4"})
                            #2- set the content of the file == to the content of the source file
                            file1.SetContentFile(source)
                            #upload the file
                            file1.Upload()
                            print('Moved:', file_name)

                            #add the folder name to the list of folder to be deleted
                            if  root not in records:
                                records.append(root)
                            # if folders[i] == ab1[-1] and folders[i] not in records:
                            #     records.append(ab1[-1])
    except Exception as e:
        # check.value = 1
        print(" -- Error During Upload \n\n error : ", e)




def delete_folder_files(folders, records):
    # this function is used to delete folder and files already uploaded
    # @folders : list of folders traversed , @records: list of folders to be deleted
    # @except : print message if an error is found during file deletion

    print('--------------------------------')
    try:
        for (root, dirs, files) in os.walk('record', topdown=True):
            # for i in folders:
            #     ab = str((root.split("-")[0])).split("\\")  # for windows System
            #     ab1 = str((root.split("-")[0])).split("/")  # for Linux System
            #     # print(folders[i], " -- ",ab[-1])
            #     if folders[i] == ab[-1] or folders[i] == ab1[-1]:
                    # delete the file and the folder from where it belongs to
                    # print(records)
                    if root in records :
                        shutil.rmtree(root)
                        print('Deleted:', root)

    except Exception as e:
        print("error during deletion : ", e)


if __name__ == "__main__":

    #shared data between processus p1 and p2 using Manager
    #used to make sure that data have been uploaded before deletion
    with multiprocessing.Manager() as manager :

        #records will keep the list of folders to be deleted
        records =manager.list([])


        # Opening JSON file
        file = open('config_folders.json')

        # returns JSON object as
        # a dictionary
        folders = json.load(file)

        # Closing file
        file.close()

        #process to upload files
        p1 = multiprocessing.Process(target=upload_files, args=(folders,records))
        #process to delete folders related
        p2 = multiprocessing.Process(target=delete_folder_files, args=(folders,records))

        # starting process 1
        p1.start()
        # wait until process 1 is finished
        p1.join()
        # print("\n*** : ",check.value)
        #delete folder if uploading was sucessfull( check.value should be equal to 100)

        # starting process 2
        p2.start()
        # wait until process 2 is finished
        p2.join()

        # both processes finished
        print('--------------------------------\n')
        print("Done!")

