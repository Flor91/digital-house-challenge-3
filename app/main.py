from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from library import crud, models, schemas, helpers
from library.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Music Genre recognition",
              description="This is a very fancy project, with auto docs for the API and everything",
              version="1.0.0",)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.get('/', response_class=HTMLResponse)
@app.get('/home', response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    data = helpers.openfile("home.md")
    songs=crud.get_songs(db, skip=0, limit=10)
    print(f'Loading {len(songs)} songs')
    return templates.TemplateResponse("index.html", {"request": request, "songs": songs, "data": data})

@app.get('/new_song', response_class=HTMLResponse)
def new_song_form(request: Request):
    return templates.TemplateResponse('new_song.html', context={'request': request})

@app.post('/new_song_m1', response_class=HTMLResponse)
def new_song_form(request: Request, spotify_id: str = Form(...), genre: str = Form(...), db: Session = Depends(get_db)):
    song = post_spotify_song(schemas.SpotifySongCreate(spotify_id=spotify_id, genre=genre), db)

    return templates.TemplateResponse("song.html", {"request": request,
                                                    "song": song,
                                                    "filepath": '/songs/' + song.filename})

@app.post('/new_song_m2', response_class=HTMLResponse)
def new_song_form(request: Request, name: str = Form(...), url: str = Form(...), genre: str = Form(...),
                  db: Session = Depends(get_db)):
    song = post_song(schemas.SongCreate(name=name, genre=genre, url=url), db)

    return templates.TemplateResponse("song.html", {"request": request,
                                                    "song": song,
                                                    "filepath": '/songs/' + song.filename})

@app.get('/search_song', response_class=HTMLResponse)
def search_song_form(request: Request):
    return templates.TemplateResponse('search_song.html', context={'request': request})

@app.post('/search_song', response_class=HTMLResponse)
def search_song_form(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    song=read_song(song_name=name, db=db)

    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")

    return templates.TemplateResponse("song.html", {"request": request,
                                                    "song": song,
                                                    "filepath":  '/songs/' + song.filename})

@app.get("/song/{song_name}/play", response_class=HTMLResponse)
def play_song(request: Request, song_name: str, db: Session = Depends(get_db)):
    db_song = read_song(song_name=song_name, db=db)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")

    filepath = '/songs/' + db_song.filename
    imgpath = '/img/melspectrograms/' + db_song.filename.split('.')[0] + '.png'

    return templates.TemplateResponse("song.html", {"request": request,
                                                    "song": db_song,
                                                    "imgpath": imgpath,
                                                    "filepath":  filepath})

@app.get("/page/{page_name}", response_class=HTMLResponse)
async def page(request: Request, page_name: str):
    data = helpers.openfile(page_name + ".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

@app.post("/song/", response_model=schemas.Song)
def post_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    db_song = crud.get_song_by_name(db, name=song.name)
    if not db_song:
        db_song = crud.create_song(db=db, song=song)
    return db_song

@app.post("/spotify_song/", response_model=schemas.SpotifySong)
def post_spotify_song(song: schemas.SpotifySongCreate, db: Session = Depends(get_db)):
    db_song = crud.get_song_by_url(db, url=song.spotify_id)
    if not db_song:
        db_song = crud.create_spotify_song(db=db, song=song)
    return db_song

@app.post("/spotify_playlist/", response_model=List[schemas.SpotifySong])
def post_spotify_playlist(playlist_id: str, genre: str = 'unknown', db: Session = Depends(get_db)):
    playlist = crud.create_songs_from_playlist(db=db, playlist_id=playlist_id, genre=genre)
    print(f'Created {len(playlist)} tracks')
    return playlist

@app.get("/songs/", response_model=List[schemas.SpotifySong])
def read_songs_list(skip: int = 0, limit: int = 100, q: Optional[str] = None, db: Session = Depends(get_db)):
    songs = crud.get_songs(db, skip=skip, limit=limit, q=q)
    return songs


@app.get("/song/{song_name}", response_model=schemas.SpotifySong)
def read_song(song_name: str, db: Session = Depends(get_db)):
    db_song = crud.get_song_by_name(db, name=song_name)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return db_song

