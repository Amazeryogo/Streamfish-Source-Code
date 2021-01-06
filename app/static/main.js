function darkMode(){
 var element = document.body;
  element.classList.toggle("dark-mode");
}

service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read, write: if request.auth != null;
    }
  }
} 