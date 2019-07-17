import sys
sys.path.insert(0,'/hiddenx/Toolkit/toolkitlogs')
import logger
import json
logger = logger.get_logger(__name__)
def unknown_mimetype(mimeType):
    config_path = "Google_Drive/config.json"
    # We will write a JSON file for the mimetype checks.
    try :
        with open(config_path,'r') as in_file:
            data = json.load(in_file)
            d1 = {mimeType : mimeType}
            data['mimeType'].update(d1)
        with open(config_path, mode='w') as out_file:
            out_file.write(json.dumps(data))
    except IOError as e :
        logger.error(f"File does not exist. {e.errno}{e.strerror}")
    except :
        raise

unknown_mimetype("mimetype.txt")
