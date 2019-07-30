from vars import *
from libs import *


REPRESENTATIONS = load_obj(REPRESENTATIONS)
FOUND_FACES = load_obj(FOUND_FACES)
load_image_and_save(INPUT_IMG,REPRESENTATIONS,FOUND_FACES)
