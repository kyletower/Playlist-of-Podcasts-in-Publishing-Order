# Import required libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

# Declare the name of the playlist
PLAYLIST_NAME = "Type the desired name of the playlist here"


def create_podcast_playlist(podcast_shows):
    try:
        # Set up authentication
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="playlist-modify-public",
            )
        )

        # Retrieve and combine episodes from all podcast shows with pagination
        episodes = []
        for show in podcast_shows:
            offset = 0

            while True:
                try:
                    # Get show information
                    show_info = sp.show(show)

                    # Retrieve the show's name
                    show_name = show_info["name"]

                    # Retrieve the publisher's name
                    publisher_name = show_info["publisher"]
                  
                    # Retrieve the total number of episodes
                    total_episodes = show_info["total_episodes"]

                    # Log the details
                    print(
                        f"{show_name} published by {publisher_name} has {total_episodes} episodes. Processing episodes {offset + 1} to {offset + 50}."
                    )

                    # Use the total_episodes as the limit for retrieving episodes
                    show_episodes = sp.show_episodes(show, limit=50, offset=offset)
                    episodes.extend(show_episodes["items"])

                    # Check if there are more episodes to retrieve
                    if len(show_episodes["items"]) < 50:
                        break

                    # Increment the offset to get the next batch of episodes
                    offset += 50
                except SpotifyException as e:
                    print(f"Error retrieving episodes for show {show}: {e}")
                    continue  # Skip this show and move on to the next

        if not episodes:
            print(
                "No episodes retrieved. Please check your podcast URIs or network connection."
            )
            return

        # Sort episodes by publishing date
        episodes_sorted = sorted(episodes, key=lambda x: x["release_date"])

        # Create a new playlist
        try:
            user_id = sp.current_user()["id"]
            playlist = sp.user_playlist_create(user_id, PLAYLIST_NAME, public=True)
        except SpotifyException as e:
            print(f"Error creating playlist: {e}")
            return

        # Add sorted episodes to the playlist in batches of 100 to avoid 400 Too many ids requested
        try:
            episode_uris = [episode["uri"] for episode in episodes_sorted]
            # sp.playlist_add_items(playlist['id'], episode_uris)
            for i in range(0, len(episode_uris), 100):
                sp.playlist_add_items(playlist["id"], episode_uris[i : i + 100])

            # Output results
            print(
                f"Playlist '{playlist['name']}' created with {len(episode_uris)} episodes."
            )
        except SpotifyException as e:
            print(f"Error adding episodes to playlist: {e}")
    except SpotifyException as e:
        print(f"Authentication failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Define the list of podcast shows
podcast_shows = [
    "spotify:show:5gbxj8Q5cCDizBSDgMoNM1",  # What Have You   March 2017-Present, 224+ eps
    "spotify:show:2BdnGS5qBs8h3BEY3wSRFp",  # Plodcast        July 2017-Present, 337+ eps
]

# Run the function
create_podcast_playlist(podcast_shows)
