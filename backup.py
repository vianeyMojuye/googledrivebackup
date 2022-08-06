from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil, os, multiprocessing

gauth = GoogleAuth()
drive = GoogleDrive(gauth)



folder = '1Ss1nmv_wiTW-DHLtI8qUkQR-9YBk-FNP'


def upload_file():
    #this function is used to upload files to google drive
    #@except : print message if an error is found during file uploading

    try :
        for (root,dirs,files) in os.walk('record', topdown=True):

            if folder in root:
                for file_name in files :
                    #absolute path of the source file
                    source = os.path.join(root, file_name)

                    #Move the file to google drive
                    # 1- Create the file into google drive location with the same name present on our machine
                    file1 = drive.CreateFile({'parents': [{'id': folder}], 'title': file_name})
                    #2- set the content of the file == to the content of the source file
                    file1.SetContentFile(source)
                    #upload the file
                    file1.Upload()
                    print('Moved:', file_name)
    except Exception as e:
        print("error ", e.message())


def delete_folder_files():
    # this function is used to delete folder and files already uploaded
    # @except : print message if an error is found during file deletion
    try:
        for (root, dirs, files) in os.walk('record', topdown=True):
            if folder in root:
                # delete the file and the folder from where it belongs to
                shutil.rmtree(root)
                print('--------------------------------')
                print('Deleted:', root)

    except Exception as e:
        print("error ", e.message())


if __name__ == "__main__":
    #process to upload files
    p1 = multiprocessing.Process(target=upload_file(), args=())
    #process to delete folders related
    p2 = multiprocessing.Process(target=delete_folder_files(), args=())

    # starting process 1
    p1.start()
    # wait until process 1 is finished
    p1.join()
    # starting process 2
    p2.start()
    # wait until process 2 is finished
    p2.join()

    # both processes finished
    print("Done!")

