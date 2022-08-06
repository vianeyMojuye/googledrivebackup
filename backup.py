from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil, os, multiprocessing, json

gauth = GoogleAuth()
drive = GoogleDrive(gauth)



def upload_files(folders):
    #this function is used to upload files to google drive
    #@except : print message if an error is found during file uploading

    try :
        for (root,dirs,files) in os.walk('record', topdown=True):
            for i in folders :
                #since our folder is like folder_name-file_name:
                # Here we check if we've found a folder present in our folder name dictionary
                ab = str((root.split("-")[0])).split("\\")
                # print(folders[i], " -- ",ab[-1])
                if folders[i] == ab[-1] :
                    for file_name in files :
                        #absolute path of the source file
                        source = os.path.join(root, file_name)

                        #Move the file to google drive
                        # 1- Create the file into google drive location with the same name present on our machine
                        file1 = drive.CreateFile({'parents': [{'id': i}], 'title': file_name})
                        #2- set the content of the file == to the content of the source file
                        file1.SetContentFile(source)
                        #upload the file
                        file1.Upload()
                        print('Moved:', file_name)
    except Exception as e:
        print("error ", e.message())


def delete_folder_files(folders):
    # this function is used to delete folder and files already uploaded
    # @except : print message if an error is found during file deletion
    print('--------------------------------')
    try:
        for (root, dirs, files) in os.walk('record', topdown=True):
            for i in folders:
                if folders[i] == str((root.split("-")[0])).split("\\")[-1]:
                    # delete the file and the folder from where it belongs to
                    shutil.rmtree(root)
                    print('Deleted:', root)

    except Exception as e:
        print("error ", e.message())


if __name__ == "__main__":

    # Opening JSON file
    file = open('config_folders.json')

    # returns JSON object as
    # a dictionary
    folders = json.load(file)

    # Closing file
    file.close()

    #process to upload files
    p1 = multiprocessing.Process(target=upload_files, args=(folders,))
    #process to delete folders related
    p2 = multiprocessing.Process(target=delete_folder_files, args=(folders,))

    # starting process 1
    p1.start()
    # wait until process 1 is finished
    p1.join()
    # starting process 2
    p2.start()
    # wait until process 2 is finished
    p2.join()

    # both processes finished
    print('--------------------------------\n')
    print("Done!")

