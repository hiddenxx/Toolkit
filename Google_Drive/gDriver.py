import sys
sys.path.insert(0,'/hiddenx/Toolkit/toolkitlogs')
import logger
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import *
from googleapiclient.errors import HttpError
from collections import defaultdict
from pprint import pprint
import json
logger = logger.get_logger(__name__)

logger.info("Configuring Paths.")
config_path = "Google_Drive/config.json"

def load_mimetype_json() :
    with open(config_path,'r') as in_file:
        data = json.load(in_file)
        MimeType = data['mimeType']
        return MimeType
    # MimeType = {"application/vnd.google-apps.folder":"folder","image/jpeg":"image",
    #             "application/vnd.google-apps.spreadsheet":"spreadsheet","text/plain":"text","application/pdf":"pdf"}

def exceptionWrapper(function):
    try :
        function()
    except Exception as e:
        logger.error(f"{e} - Error")
def authenticate():
    """
		Authenticate to Google API
	"""
    logger.info("Authenticating Google Drive API.")
    gauth = GoogleAuth()
    # Try to load saved client credentials
    logger.info("Checking for credential file.")
    gauth.LoadCredentialsFile("mycreds_googleDrive.txt")

    if gauth.credentials is None:
        # Authenticate if they're not there
        logger.info("Authenticating using Local Web Server.")
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        logger.info("Refreshing Auth Token.")
        gauth.Refresh()
    else:
        # Initialize the saved creds
        logger.info("Authorizing Saved credentials.")
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds_googleDrive.txt")
    logger.info("Authorization Complete.")
    return GoogleDrive(gauth)

def get_folders(drive, parent_folder_id = "root"):
    # Auto-iterate through all files in the parent folder.
    file_list = GoogleDriveFileList()
    try:
        logger.info(f"Searching Drive for {parent_folder_id}")
        file_list = drive.ListFile(
			{'q': "'{0}' in parents and trashed=false".format(parent_folder_id)}
		).GetList()
        logger.info(f"{file_list}")
	# Exit if the parent folder doesn't exist
    except googleapiclient.errors.HttpError as err:
		# Parse error message
        message = ast.literal_eval(err.content)['error']['message']
        if message == 'File not found: ':
            print(message)
            logger.info(message + "not found in drive.")
            return
		# Exit with stacktrace in case of other error
        else:
            logger.info(f"Exiting : {message}")
            raise

    return file_list

def display_folder(file_list) :
    if file_list is None :
        print("No Folders in drive", sep=' ', end='n', file=sys.stdout, flush=False)
    else :
        count = 1
        for file1 in file_list:
                logger.debug(f"Title : {file1['title']} , ID : {file1['id']} , mimeType : {file1['mimeType']}")
                MimeType = load_mimetype_json()
                mimetype = MimeType.get(file1['mimeType'], "Unknown")
                if mimetype == "Unknown" :
                    unknown_mimetype(file1['mimeType']) #Sends mimetype.
                print(f"{count}.{file1['title']} - {mimetype}",end='\n')
                count += 1

def unknown_mimetype(mimeType):
    # We will write a JSON file for the mimetype checks.
    try :
        with open(config_path,'r') as in_file:
            data = json.load(in_file)
            d1 = {mimeType : mimeType}
            data['mimeType'].update(d1)
        with open(config_path, mode='w') as out_file:
            out_file.write(json.dumps(data,indent=4,sort_keys=True))
    except IOError as e :
        logger.error(f"File does not exist. {e.errno}{e.strerror}")
    except :
        raise

def remove_all_duplicateFiles():
    # if file1['mimeType'] != "application/vnd.google-apps.folder" :
    #     print(f"{file1['md5Checksum']} - {file1['title']}")
    # else :
    # and store those duplicate files list of what u deleted and from where it was deleted.
    pass


def get_folder_id(drive, parent_folder_id, parent_folder_name):
    """
		Check if destination folder exists and return it's ID
	"""

    # Auto-iterate through all files in the parent folder.
    file_list = GoogleDriveFileList()
    try:
        file_list = drive.ListFile(
			{'q': "'{0}' in parents and trashed=false".format(parent_folder_id)}
		).GetList()
	# Exit if the parent folder doesn't exist
    except googleapiclient.errors.HttpError as err:
		# Parse error message
        message = ast.literal_eval(err.content)['error']['message']
        if message == 'File not found: ':
            print(message + parent_folder_name)
            logger.info(message + parent_folder_name + "not found in drive.")
            exit(1)
		# Exit with stacktrace in case of other error
        else:
            raise

	# Find the the destination folder in the parent folder's files
    for file1 in file_list:
        if file1['title'] == parent_folder_name:
            print('title: %s, id: %s' % (file1['title'], file1['id']))
            logger.info('title: %s, id: %s' % (file1['title'], file1['id']))
            return file1['id']


def create_folder(drive, folder_name, parent_folder_id):
    """
		Create folder on Google Drive
	"""
    folder_metadata ={'title': folder_name,
        # Define the file type as folder
        'mimeType': 'application/vnd.google-apps.folder',
		# ID of the parent folder
		'parents': [{"kind": "drive#fileLink", "id": parent_folder_id}]}

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()

    # Return folder informations
    print('title: %s, id: %s' % (folder['title'], folder['id']))
    return folder['id']


def upload_files(drive, folder_id, src_folder_name):
    """
		Upload files in the local folder to Google Drive
	"""

	# Enter the source folder
    try:
        chdir(src_folder_name)
	# Print error if source folder doesn't exist
    except OSError:
        print(src_folder_name + 'is missing')
        logger.error("Source folder doesn't exist.")
	# Auto-iterate through all files in the folder.
    for file1 in listdir('.'):
		# Check the file's size
        statinfo = stat(file1)
        if statinfo.st_size > 0:
            print('Uploading ' + file1)
            # Upload file to folder.
            f = drive.CreateFile(
                {"parents": [{"kind": "drive#fileLink", "id": folder_id}]})
            f.SetContentFile(file1)
            f.Upload()
		# Skip the file if it's empty
        else:
            print('File {0} is empty'.format(file1))
            logger.info('File {0} is empty'.format(file1))

def display_files_and_folders():
    return display_folder(get_folders(drive))

drive = authenticate()
