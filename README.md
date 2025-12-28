### Important Setup Info

## Libraries 

Spotipy
Fastapi
alembic
dotenv
panadas
sqlalchemy
uvicorn

React

# How to start the program

1. Run the api server

uvicorn app.main:app --reload

2. Then run the frontend

npm start

# When adding a new column to the database:

1. Input this into the venv cmd: 

& ~/Spootifooy/venv/Scripts/Activate.ps1; alembic revision --autogenerate -m "initial schema with image_url"  

2.  Then Input this:

alembic upgrade head

3. Then fetch the data again

python -m app.fetch_data     

4. Then start the server

uvicorn app.main:app --reload     