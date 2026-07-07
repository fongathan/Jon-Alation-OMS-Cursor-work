/**
 * Firebase config for live shared comments on countdown-july-9.html
 *
 * Firestore rules (Console → Firestore → Rules):
 *   match /july9-comments/{id} {
 *     allow read, create, delete: if true;
 *     allow update: if false;
 *   }
 *   match /july9-meta/{id} {
 *     allow read, create, update: if true;
 *   }
 *
 * Storage rules (Console → Storage → Rules):
 *   match /july9-comments/{fileName} {
 *     allow read: if true;
 *     allow write: if request.resource.size < 3 * 1024 * 1024
 *       && request.resource.contentType.matches('image/.*');
 *   }
 */
window.COUNTDOWN_FIREBASE = {
  apiKey: "AIzaSyBwXQy7Oxo5C1jHyg5FgL-PVplEeGVVGCI",
  authDomain: "jonlizcountdown.firebaseapp.com",
  projectId: "jonlizcountdown",
  storageBucket: "jonlizcountdown.firebasestorage.app",
  messagingSenderId: "756309325437",
  appId: "1:756309325437:web:279ad0b423e7f75d2b6314"
};

/** Giphy search uses COUNTDOWN_GIPHY_API_KEY in giphy-config.js */
