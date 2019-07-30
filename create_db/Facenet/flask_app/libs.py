import numpy as np
import matplotlib.pyplot as plt
import keras
import os
from vars import *
from keras.models import model_from_json
model = model_from_json(open(FACENET_MODEL, "r").read())
model.load_weights(FACENET_WEIGHTS)
model.summary()
model.predict(np.random.rand(1,160,160,3))

def save_obj(obj,name):
    import pickle
    with open(name+'.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        print(name+".pkl saved")

def load_obj(name):
    import pickle
    with open(name, 'rb') as f:
        return pickle.load(f)


def get_representation(inp,min_face_size=MIN_FACE_SIZE):
    from skimage.transform import rescale, resize, downscale_local_mean
    from mtcnn.mtcnn import MTCNN
    if 'model' in locals():
        #del model
        pass
    # create the detector, using default weights
    detector = MTCNN(min_face_size=min_face_size)
    # detect faces in the image
    faces = detector.detect_faces(inp)
    if len(faces)<1:
        return None
    output = []
    #from keras.models import model_from_json
    #facenet model structure: https://github.com/serengil/tensorflow-101/blob/master/model/facenet_model.json
    #model = model_from_json(open(FACENET_MODEL, "r").read())
    #pre-trained weights https://drive.google.com/file/d/1971Xk5RwedbudGgTIrGAL4F7Aifu7id1/view?usp=sharing
    #model.load_weights(FACENET_WEIGHTS)
    for face in faces:
        x,y,w,d = face['box']
        facex = inp[y:y+d,x:x+w,:]
        img = resize(facex, (160, 160), anti_aliasing=True)
        img = img.reshape(1,160,160,3).copy()
        representation = model.predict(img)
        pyplot_box = [[x,y],w,d]
        output.append({'box':[y,y+d,x,x+w],'representation':representation.copy(),'pyplot_box':pyplot_box[:]})
    return output[:]

def get_top_similar(irepx,ireprs,faces_db,top=3,):
    distances = abs(irepx-ireprs).sum(1)
    distances_sorted = np.argsort(distances)
    output = []
    for _ in range(top):
        min_index = distances_sorted[_]
        name = faces_db[min_index]['name']
        image = faces_db[min_index]['face']
        output.append({'distance':distances[min_index],'name':name,'image':image.copy()})
    return output[:]

def load_image_and_save(imagefile,irepresentations,ifound_faces):
    pixels = plt.imread(imagefile)
    fig = plt.figure(figsize=FIGSIZE,dpi=DPI,frameon=False)
    plt.axis('off')
    plt.imshow(pixels)
    faces = get_representation(pixels[:,:,:3])
    if type(faces)==list:
        for face in faces:
            repx = face['representation'].copy()
            plt.gca().add_patch(
                plt.Rectangle(*face['pyplot_box'],fill=False,color='red',)
              )
            top_images = get_top_similar(repx,irepresentations,ifound_faces,top=1)
            for found in top_images:
                plt.text(*face['pyplot_box'][0],found['name'],**LABEL_FONT)
    #plt.show()
    fig.savefig(OUTPUT_IMG,dpi=DPI,frameon=False,bbox_inches='tight', pad_inches=0)
    plt.close()
