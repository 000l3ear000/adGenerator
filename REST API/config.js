import * as firebase from 'firebase/app';
import 'firebase/storage';

config = {
    "apiKey": "AIzaSyDvYb9sgl85AgyTriAgHwLg_-uadcFXlWY",
    "authDomain": "imagepreview-aef2b.firebaseapp.com",
    "projectId": "imagepreview-aef2b",
    "databaseURL": "https://imagepreview-aef2b.firebaseio.com",
    "storageBucket": "imagepreview-aef2b.appspot.com",
    "messagingSenderId": "46502678413",
    "appId": "1:46502678413:web:650b751df6da56d46577c4",
    "measurementId": "G-W7KEVXRSG2"
}

firebase.initializeApp(config);
const storage = firebase.storage();
export { storage };