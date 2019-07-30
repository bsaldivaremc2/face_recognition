#Version 201906141842

SAVE_FOLDER = './static/'
INPUT_IMG = 'cofunds/muhammad.jpg'
OUTPUT_IMG = SAVE_FOLDER+'output.png'
DB_FOLDER = 'db/'
REPRESENTATIONS = DB_FOLDER+'cofund_representations.pkl'
FOUND_FACES = DB_FOLDER+'cofund_faces.pkl'
FACENET_MODEL = DB_FOLDER+'facenet_model.json'
FACENET_WEIGHTS = DB_FOLDER+'facenet_weights.h5'

LABEL_FONT = {'family':'serif', 'size':'16', 'color':'red', 'weight':'normal',
              'verticalalignment':'bottom'}
DPI = 80
FIGSIZE = (20,20)
MIN_FACE_SIZE = 20


BASE_URL = '''
<!doctype html>
<title>Find your COFUND Fellow =) </title>
<h1>Please upload a picture and find if my system can detect who are you =)</h1>
<form method=post enctype=multipart/form-data>
  <p><input type=file name=file>
     <input type=submit value=Upload>
</form>
'''
