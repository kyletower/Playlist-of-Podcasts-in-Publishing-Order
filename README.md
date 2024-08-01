# Playlist-of-Podcasts-in-Publishing-Order

This app will create a publishing ordered playlist from a list of podcast shows on Spotify.

NOTE: If you attempt to create a playlist with a name that already exists using the Spotify API, the API will still create a new playlist, even if a playlist with the same name already exists. It does not check for duplicate names.

You may update the code to handle that case how you wish (i.e. update the playlist if it already exists or delete and recreate the playlist).

## Setup

1. Clone the repo to your local device.
2. Open the repo in your preferred IDE or editor.
3. Open your command line and navigate to the directory where you cloned this project.
4. Create a Virtual Environment using `venv`. You may replace `spotify` with your preffered name for the environment.

   ```bash
   python3 -m venv spotify
   ```
   
6. Activate on Linux/macOS

   ```bash
   source spotify/bin/activate
   ```

7. Install dependencies.
   via the `requirements.txt` file
   
   ```bash
   pip install -r requirements.txt
   ```

   or manually

   ```bash
   pip install --upgrade pip
   pip install spotipy
   pip install python-dev
   ```

8. Create (or use) your Spotify Developer Account
9. Sign up at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and create an application to get your Client ID and Client Secret.
10. Rename `.env.example` to `.env` and update it with your Client ID, Client Secret, and Redirect URI.

    ```env
    SPOTIPY_CLIENT_ID=your_client_id
    SPOTIPY_CLIENT_SECRET=your_client_secret
    SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
    ```

11. Run the app in the command line

    ```bash
    python app.py
    ````

12. Open the Spotify Web App, Mobile App, or Desktop App and view the new playlist. 
