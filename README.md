# README

## Project Description

SpotifyStatTracker (will rename in the future) is a webapp that allows the user to track  view their spotify stats such as

1. Top tracks
2. Top artists
3. Recently played songs
4. Playlist [Not implemented]

It will also use the users data to generate a custom played appropriate for the user (not implemented) and compare stats with other users to generate a custom playlist (not implemented). 

This is project is wip and hopefully will implement all of the features stated above (plz speed I need this)

Project started in December 
Author: itz_dinnertime (d_nnertime)


## App Setup Instructions


### Setting up virtual environment

1. Input into (powershell/bash): python -m venv venv

2. Activate the virtual environment:

    On Windows: venv\bin\activate

    On macOs/Linux: source venv/bin/activate


### Setting up all dependencies

1. Input into (powershell/bash) : pip install -r requirments.txt


### Setting up backend

1. Input into (powershell/bash): uvicorn app.main:app --reload


### Setting up frontend

1. Move to the frontend directory: cd frontend/

2. Install dependencies: npm install

3. Then run: npm install react-router-dom

4. Run: npm start


### Updating database schema

1. In the root directory: alembic revision --autogenerate -m "put action message here"

2. Apply the latest migrations to database: alembic upgrade head

3. To fetch the data: python -m app.fetch_data



## How to run

# Via script

1. In your root directory (bash) run: .\start.sh

OR

# Manually

1. In your virtual environment run: uvicorn app.main:app --reload

2. Open a separate terminal.

3. Move to frontend/ directory: cd frontend/

4. Run: npm start
