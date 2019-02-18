import logging
from logging.config import fileConfig
from configparser import ConfigParser
import os, os.path

from meetup import MeetupImages
import imageworker

# Create the Working folders
working_folders = ['logs','.metadata','WorkingFolder','./Workingfolder/MeetupImages','./Workingfolder/OutputImages']
[os.makedirs(folder) for folder in working_folders if not os.path.exists(folder)]

# Load Configuration for reading parameters
Config = ConfigParser()
Config.read('settings.ini')

# Load log config
fileConfig('logging_config.ini')
logger = logging.getLogger()

def meetupworker(api_key, meetup_group):
    # meetup worker : Get the Meetup Members and then images
    meetup_worker = MeetupImages(api_key=api_key)
    members = meetup_worker.getmembers(meetup_group)
    meetup_worker.getmemberphotos(members['results'])

if __name__ == "__main__":
    
    # Read Meetup API Key and group details
    api_key = Config.get('meetup', 'api_key')
    meetup_group = Config.get('meetup', 'meetup_group')

    #meetupworker(api_key=api_key, meetup_group=meetup_group)

    encodings = imageworker.loadencodings()
    imageworker.tagmembers('WorkingFolder/test/test_image_meetup.jpeg', encodings)