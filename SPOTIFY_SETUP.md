# Self-hosting the Spotify "Now playing" card

Based on https://github.com/kittinan/spotify-github-profile (the public instance moved to
spotify-github-profile.kittinanx.com, but you are hosting your own copy so you don't depend on it).
You need 3 free accounts: GitHub, Vercel, Firebase (Google) + a Spotify developer app.

## 1. Fork and deploy on Vercel
1. Fork kittinan/spotify-github-profile to your GitHub (Fork button).
2. Go to https://vercel.com/import, log in with GitHub, import your fork.
3. Don't deploy yet if it asks for env vars. Note the project name; your URL will be
   https://PROJECT-NAME.vercel.app (check it on the project dashboard after the first deploy).

## 2. Firebase (stores your Spotify tokens)
1. https://console.firebase.google.com -> Add project.
2. Build -> Firestore Database -> Create database (production mode is fine).
3. Project settings (gear) -> Service accounts -> Generate new private key -> downloads a .json file.
4. Convert that file to base64 (one line, no line breaks):
   - Mac/Linux:  base64 -i your-key.json | tr -d '\n'
   - Windows PowerShell:  [Convert]::ToBase64String([IO.File]::ReadAllBytes("your-key.json"))
   Keep this value secret.

## 3. Spotify developer app
1. https://developer.spotify.com/dashboard -> Create app.
2. Redirect URI: https://PROJECT-NAME.vercel.app/api/callback  (exactly, with /api/callback)
3. Tick "Web API". Save, then copy the Client ID and Client Secret.
4. Spotify apps start in development mode: only users you add under User Management
   (your own Spotify account email) can log in. That's fine, since it's only you.

## 4. Environment variables (Vercel -> Project -> Settings -> Environment Variables)
BASE_URL            = https://PROJECT-NAME.vercel.app/api
SPOTIFY_CLIENT_ID   = (from step 3)
SPOTIFY_SECRET_ID   = (client secret from step 3)
FIREBASE            = (base64 string from step 2)

Then Deployments -> Redeploy so the variables take effect.

## 5. Connect your account and get your uid
1. Open https://PROJECT-NAME.vercel.app/api/login and log in with Spotify.
2. The page gives you an embed link containing uid=XXXXXXXX. Copy that uid.

## 6. Put it in the README
In README.md replace YOUR-APP with PROJECT-NAME and YOUR_SPOTIFY_ID with your uid.
Play a song and refresh your profile. If nothing is playing the card is blank
(set show_offline=true in the URL to show an offline card instead).

## Troubleshooting
- "redirect_uri mismatch": the Spotify redirect URI must match exactly, including /api/callback.
- Blank image: open the image URL directly in your browser to see the error message.
- 500 error: usually FIREBASE is wrong (must be base64 of the whole JSON file) or Firestore wasn't created.
