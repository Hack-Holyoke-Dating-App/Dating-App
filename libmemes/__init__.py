from models.meme import Meme

BASE_MEME_PATH='/static/memes/'
MEME_PATHS = [
    'drunk_baby.jpg',
    'keep_calm_vader.jpg',
    'wood_face.jpg',
    'catching_shrimp.jpg',
    'harry_potter.jpg',
    'success_kid.jpg',
    'house_fire_kid.jpeg',
    'the_office.jpeg',
    'trump_newspaper_mouth.jpg',
    'death_grips.jpeg',
    'keep_calm_trump.png',
    'time_travel.jpg',
    'trump_wifi.jpeg'
]

def make_meme_models():
    memes = []

    for meme_path in MEME_PATHS:
        meme = Meme(id=None,
                    image_path="{}{}".format(BASE_MEME_PATH, meme_path))
        memes.append(meme)

    return memes
