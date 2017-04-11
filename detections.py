import boto3
import os
import time
import cv2
import numpy as np
import scipy
import caffe
import coreset_structure
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect




# return list of file names that are new
def monitor_directory(path,files):
	existing_file_set = set(os.listdir(path))
	new_file_set = []
	for f in files:
		if f not in existing_file_set:
			new_file_set.append(f)
			existing_file_set.add(f)
	return new_file_set, existing_file_set

def process_coreset(path,net):
	# walk the coreset
	coreset = CoresetStructure(path)
	keyframes = coreset.get_keyframes()
	for keyframe in keyframes:
		print keyframe
	# for all the frame numbers in the leaves - grab as just an image

	# get the detections for a specific image

	# add detections to db


# run detections for given file and add to database
def run_detections(net,im):
	#objects = ("accordion","airplane" ,"ant" ,"antelope" ,"apple" ,"armadillo" ,"artichoke" ,"axe" ,"baby bed" ,"backpack" ,"bagel" ,"balance beam" ,"banana" ,"band aid" ,"banjo" ,"baseball" ,"basketball" ,"bathing cap" ,"beaker" ,"bear" ,"bee" ,"bell pepper" ,"bench" ,"bicycle" ,"binder" ,"bird" ,"bookshelf" ,"bow" ,"bow tie" ,"bowl" ,"brassiere" ,"burrito" ,"bus" ,"butterfly" ,"camel" ,"can opener" ,"car" ,"cart" ,"cattle" ,"cello" ,"centipede" ,"chain saw" ,"chair" ,"chime" ,"cocktail shaker" ,"coffee maker" ,"computer keyboard" ,"computer mouse" ,"corkscrew" ,"cream" ,"croquet ball" ,"crutch" ,"cucumber" ,"cup or mug" ,"diaper" ,"digital clock" ,"dishwasher" ,"dog" ,"domestic cat" ,"dragonfly" ,"drum" ,"dumbbell" ,"electric fan" ,"elephant" ,"face powder" ,"fig" ,"filing cabinet" ,"flower pot" ,"flute" ,"fox" ,"french horn" ,"frog" ,"frying pan" ,"giant panda" ,"goldfish" ,"golf ball" ,"golfcart" ,"guacamole" ,"guitar" ,"hair dryer" ,"hair spray" ,"hamburger" ,"hammer" ,"hamster" ,"harmonica" ,"harp" ,"hat with a wide brim" ,"head cabbage" ,"helmet" ,"hippopotamus" ,"horizontal bar" ,"horse" ,"hotdog" ,"iPod" ,"isopod" ,"jellyfish" ,"koala bear" ,"ladle" ,"ladybug" ,"lamp" ,"laptop" ,"lemon" ,"lion" ,"lipstick" ,"lizard" ,"lobster" ,"maillot" ,"maraca" ,"microphone" ,"microwave" ,"milk can" ,"miniskirt" ,"monkey" ,"motorcycle" ,"mushroom" ,"nail" ,"neck brace" ,"oboe" ,"orange" ,"otter" ,"pencil box" ,"pencil sharpener" ,"perfume" ,"person" ,"piano" ,"pineapple" ,"ping-pong ball" ,"pitcher" ,"pizza" ,"plastic bag" ,"plate rack" ,"pomegranate" ,"popsicle" ,"porcupine" ,"power drill" ,"pretzel" ,"printer" ,"puck" ,"punching bag" ,"purse" ,"rabbit" ,"racket" ,"ray" ,"red panda" ,"refrigerator" ,"remote control" ,"rubber eraser" ,"rugby ball" ,"ruler" ,"salt or pepper shaker" ,"saxophone" ,"scorpion" ,"screwdriver" ,"seal" ,"sheep" ,"ski" ,"skunk" ,"snail" ,"snake" ,"snowmobile" ,"snowplow" ,"soap dispenser" ,"soccer ball" ,"sofa" ,"spatula" ,"squirrel" ,"starfish" ,"stethoscope" ,"stove" ,"strainer" ,"strawberry" ,"stretcher" ,"sunglasses" ,"swimming trunks" ,"swine" ,"syringe" ,"table" ,"tape player" ,"tennis ball" ,"tick" ,"tie" ,"tiger" ,"toaster" ,"traffic light" ,"train" ,"trombone" ,"trumpet" ,"turtle" ,"tv or monitor" ,"unicycle" ,"vacuum" ,"violin" ,"volleyball" ,"waffle iron" ,"washer" ,"water bottle" ,"watercraft" ,"whale" ,"wine bottle" ,"zebra")
	scores, boxes = im_detect(net,im)

def init_net():
	cfg.TEST.HAS_RPN = True
	prototxt = os.path.join(cfg.MODELS_DIR, 'VGG16,
                            'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
	caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                              'VGG16_faster_rcnn_final.caffemodel')
	caffe.set_mode_gpu()
	return caffe.Net(prototxt, caffemodel, caffe.TEST)

def add_to_db():
	pass

def get_frame_from_video(path,frame_no):
	cap = cv2.VideoCapture(path)
	frame_total = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
	frame_no = (float(frame_no) /float(frame_total))
	cap.set(2,frame_no)
	ret, frame = cap.read()
	return frame

if __name__=="__main__":
	path = ""
	files = set([])
	net = init_net()
	while True:
		new_files, files = monitor_directory(path,files)
		for f in new_files:
			process_coreset(path + f)
		time.sleep(5)