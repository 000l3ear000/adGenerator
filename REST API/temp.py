
import pyrebase
import uuid

FRAME_FILENAME = "framePreview.png"

config = {
    "apiKey": "AIzaSyDvYb9sgl85AgyTriAgHwLg_-uadcFXlWY",
    "authDomain": "imagepreview-aef2b.firebaseapp.com",
    "projectId": "imagepreview-aef2b",
    "databaseURL": "https://imagepreview-aef2b-default-rtdb.firebaseio.com/",
    "storageBucket": "imagepreview-aef2b.appspot.com",
    "messagingSenderId": "46502678413",
    "appId": "1:46502678413:web:650b751df6da56d46577c4",
    "measurementId": "G-W7KEVXRSG2",
    "serviceAccount": './firebase-creds.json'
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()
id = uuid.uuid4()
email = "testuser@gmail.com"
password = "123456"

# def saveFrame():
#     getResult = composeVideo()
#     getResult.save_frame( FRAME_FILENAME, t = saveFrameTime )

# def getImageUrl():
#     # print("I ma here")
#     auth = firebase.auth()
#     # userCreated = auth.create_user_with_email_and_password(email, password)
#     user = auth.sign_in_with_email_and_password(email, password)
#     url = storage.child(FRAME_FILENAME).get_url(user['idToken'])
#     # storage.delete(url)
#     print(url)

# def deletePreviewImage():
storage.child(FRAME_FILENAME).delete(FRAME_FILENAME)
# data = { str(id): FRAME_FILENAME}
# db.child("images").set(data)
    

# def uploadPreviewImage():
#     saveFrame()
#     # print("asdasd")
    
#     storage.child(FRAME_FILENAME).put(FRAME_FILENAME)
#     getImageUrl()
#     deletePreviewImage()