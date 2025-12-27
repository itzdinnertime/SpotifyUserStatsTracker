from flask import Flask, redirect, request, session, url_for, jsonify
import os
from dotenv import load_dotenv

# Import auth functions from auth.py
from app.auth import (
    get_auth_url,
    get_access_token,
    create_spotify_client,
    get_valid_client
)

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management


# ============== ROUTES ==============

@app.route("/")
def home():
    """Home page - shows login link or user info if logged in"""
    if "token_info" in session:
        return jsonify({
            "message": "You are logged in!",
            "endpoints": {
                "profile": "/me",
                "top_tracks": "/top-tracks",
                "top_artists": "/top-artists",
                "recently_played": "/recently-played",
                "logout": "/logout"
            }
        })
    return jsonify({
        "message": "Welcome to Spotify Stats Tracker",
        "login": "/login"
    })


@app.route("/login")
def login():
    """Redirect user to Spotify login page"""
    auth_url = get_auth_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    """Handle Spotify's redirect after user authorizes"""
    # Get the authorization code from URL
    code = request.args.get("code")
    
    if not code:
        return jsonify({"error": "No authorization code received"}), 400
    
    # Exchange code for access token
    token_info = get_access_token(code)
    
    # Store token in session
    session["token_info"] = token_info
    
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    """Clear session and log out"""
    session.clear()
    return jsonify({"message": "Logged out successfully"})


@app.route("/me")
def get_current_user():
    """Get current user's profile"""
    if "token_info" not in session:
        return jsonify({"error": "Not logged in", "login": "/login"}), 401
    
    try:
        sp, token_info = get_valid_client(session["token_info"])
        session["token_info"] = token_info  # Update in case of refresh
        
        user = sp.current_user()
        return jsonify({
            "display_name": user["display_name"],
            "email": user.get("email"),
            "followers": user["followers"]["total"],
            "profile_image": user["images"][0]["url"] if user["images"] else None,
            "spotify_url": user["external_urls"]["spotify"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/top-tracks")
def get_top_tracks():
    """Get user's top tracks"""
    if "token_info" not in session:
        return jsonify({"error": "Not logged in", "login": "/login"}), 401
    
    # Get optional query params
    time_range = request.args.get("time_range", "medium_term")  # short_term, medium_term, long_term
    limit = request.args.get("limit", 10, type=int)
    
    try:
        sp, token_info = get_valid_client(session["token_info"])
        session["token_info"] = token_info
        
        results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
        
        tracks = []
        for i, track in enumerate(results["items"], 1):
            tracks.append({
                "rank": i,
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                "spotify_url": track["external_urls"]["spotify"]
            })
        
        return jsonify({
            "time_range": time_range,
            "tracks": tracks
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/top-artists")
def get_top_artists():
    """Get user's top artists"""
    if "token_info" not in session:
        return jsonify({"error": "Not logged in", "login": "/login"}), 401
    
    time_range = request.args.get("time_range", "medium_term")
    limit = request.args.get("limit", 10, type=int)
    
    try:
        sp, token_info = get_valid_client(session["token_info"])
        session["token_info"] = token_info
        
        results = sp.current_user_top_artists(limit=limit, time_range=time_range)
        
        artists = []
        for i, artist in enumerate(results["items"], 1):
            artists.append({
                "rank": i,
                "name": artist["name"],
                "genres": artist["genres"][:3],  # Top 3 genres
                "followers": artist["followers"]["total"],
                "popularity": artist["popularity"],
                "image": artist["images"][0]["url"] if artist["images"] else None,
                "spotify_url": artist["external_urls"]["spotify"]
            })
        
        return jsonify({
            "time_range": time_range,
            "artists": artists
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/recently-played")
def get_recently_played():
    """Get user's recently played tracks"""
    if "token_info" not in session:
        return jsonify({"error": "Not logged in", "login": "/login"}), 401
    
    limit = request.args.get("limit", 20, type=int)
    
    try:
        sp, token_info = get_valid_client(session["token_info"])
        session["token_info"] = token_info
        
        results = sp.current_user_recently_played(limit=limit)
        
        tracks = []
        for item in results["items"]:
            track = item["track"]
            tracks.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"],
                "played_at": item["played_at"],
                "image": track["album"]["images"][0]["url"] if track["album"]["images"] else None,
                "spotify_url": track["external_urls"]["spotify"]
            })
        
        return jsonify({"recently_played": tracks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============== RUN APP ==============

if __name__ == "__main__":
    app.run(debug=True, port=8000)