# MeetupMemberVerification

(In-Progress)

**Installation Instructions**
- Python 3+
- face-recognition module (follow the installation instructions from [here](https://github.com/ageitgey/face_recognition))
- PIL, requests libraries

**Details required for running the solution**
- Meetup API key from Meetup [site](https://secure.meetup.com/meetup_api/key/)
- Meetup Group Name (check example on settings.ini)

Comment the below line for simultaneous runs to avoid download the User Image profiles again
```python
#meetupworker(api_key=api_key, meetup_group=meetup_group)
```

Set retrain=True to recalculate the encodings and save them under .metadata
```python
encodings = imageworker.loadencodings(retrain=True)
```

Location of the image to be tagged
```python
imageworker.tagmembers('WorkingFolder/test/test_image_meetup.jpeg', encodings)
```
Output will be under 'WorkingFolder/OutputImages' folder

**Work in Progress**:
- More documentation to follow.
- Meetup API has a limitation of 200 results. Working to update the solution to retrieve all images
- Logging messages and Error handling

_**Credits**_:
- https://github.com/ageitgey/face_recognition
- https://github.com/davisking/dlib