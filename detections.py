import _init_paths
import boto3
import os
import time
import cv2
import numpy as np
import scipy
import coreset_structure
import db_accessor
import caffe
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect_array
from fast_rcnn.nms_wrapper import nms



# return list of file names that are new
def monitor_directory(path,existing_file_set):
	files = set(os.listdir(path))
	new_file_set = []
	for f in files:
		if f not in existing_file_set:
			new_file_set.append(f)
			existing_file_set.add(f)
	return new_file_set, existing_file_set

def process_coreset(path,net):
	# walk the coreset
	coreset = coreset_structure.CoresetStructure(path)
	db = db_accessor.DB()
	#print coreset.get_video_info()
	#scene_info = db.add_scene(coreset.get_video_info())
	paths = {}
	#print coreset.get_results_name()
	
	paths['results'] = tree_path + coreset.get_results_name()
	paths['tree'] = tree_path + coreset.get_tree_name()
	paths['simple'] = path
	#db.add_coreset(scene_info,paths)
	keyframes = coreset.get_keyframes()
	#print coreset.get_video_info()
	for keyframe in keyframes:
		im = get_frame_from_video(video_path + coreset.get_video_info()[0][0],keyframe)
		scores,boxes = im_detect_array(net,[im])
		scores = scores[0]
		boxes = boxes[0]
		print len(scores)
		#db.add_detections_from_frame(scores,boxes,scene_info,keyframe)
	db.close()
		
	# for all the frame numbers in the leaves - grab as just an image

	# get the detections for a specific image

	# add detections to db


# run detections for given file and add to database
def run_detections(net,im):
	#objects = ("accordion","airplane" ,"ant" ,"antelope" ,"apple" ,"armadillo" ,"artichoke" ,"axe" ,"baby bed" ,"backpack" ,"bagel" ,"balance beam" ,"banana" ,"band aid" ,"banjo" ,"baseball" ,"basketball" ,"bathing cap" ,"beaker" ,"bear" ,"bee" ,"bell pepper" ,"bench" ,"bicycle" ,"binder" ,"bird" ,"bookshelf" ,"bow" ,"bow tie" ,"bowl" ,"brassiere" ,"burrito" ,"bus" ,"butterfly" ,"camel" ,"can opener" ,"car" ,"cart" ,"cattle" ,"cello" ,"centipede" ,"chain saw" ,"chair" ,"chime" ,"cocktail shaker" ,"coffee maker" ,"computer keyboard" ,"computer mouse" ,"corkscrew" ,"cream" ,"croquet ball" ,"crutch" ,"cucumber" ,"cup or mug" ,"diaper" ,"digital clock" ,"dishwasher" ,"dog" ,"domestic cat" ,"dragonfly" ,"drum" ,"dumbbell" ,"electric fan" ,"elephant" ,"face powder" ,"fig" ,"filing cabinet" ,"flower pot" ,"flute" ,"fox" ,"french horn" ,"frog" ,"frying pan" ,"giant panda" ,"goldfish" ,"golf ball" ,"golfcart" ,"guacamole" ,"guitar" ,"hair dryer" ,"hair spray" ,"hamburger" ,"hammer" ,"hamster" ,"harmonica" ,"harp" ,"hat with a wide brim" ,"head cabbage" ,"helmet" ,"hippopotamus" ,"horizontal bar" ,"horse" ,"hotdog" ,"iPod" ,"isopod" ,"jellyfish" ,"koala bear" ,"ladle" ,"ladybug" ,"lamp" ,"laptop" ,"lemon" ,"lion" ,"lipstick" ,"lizard" ,"lobster" ,"maillot" ,"maraca" ,"microphone" ,"microwave" ,"milk can" ,"miniskirt" ,"monkey" ,"motorcycle" ,"mushroom" ,"nail" ,"neck brace" ,"oboe" ,"orange" ,"otter" ,"pencil box" ,"pencil sharpener" ,"perfume" ,"person" ,"piano" ,"pineapple" ,"ping-pong ball" ,"pitcher" ,"pizza" ,"plastic bag" ,"plate rack" ,"pomegranate" ,"popsicle" ,"porcupine" ,"power drill" ,"pretzel" ,"printer" ,"puck" ,"punching bag" ,"purse" ,"rabbit" ,"racket" ,"ray" ,"red panda" ,"refrigerator" ,"remote control" ,"rubber eraser" ,"rugby ball" ,"ruler" ,"salt or pepper shaker" ,"saxophone" ,"scorpion" ,"screwdriver" ,"seal" ,"sheep" ,"ski" ,"skunk" ,"snail" ,"snake" ,"snowmobile" ,"snowplow" ,"soap dispenser" ,"soccer ball" ,"sofa" ,"spatula" ,"squirrel" ,"starfish" ,"stethoscope" ,"stove" ,"strainer" ,"strawberry" ,"stretcher" ,"sunglasses" ,"swimming trunks" ,"swine" ,"syringe" ,"table" ,"tape player" ,"tennis ball" ,"tick" ,"tie" ,"tiger" ,"toaster" ,"traffic light" ,"train" ,"trombone" ,"trumpet" ,"turtle" ,"tv or monitor" ,"unicycle" ,"vacuum" ,"violin" ,"volleyball" ,"waffle iron" ,"washer" ,"water bottle" ,"watercraft" ,"whale" ,"wine bottle" ,"zebra")
	scores, boxes = im_detect(net,im)

def init_net():
	cfg.TEST.HAS_RPN = True
	prototxt = os.path.join(cfg.MODELS_DIR, 'VGG16',
                            'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
	caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                              'VGG16_faster_rcnn_final.caffemodel')
	caffe.set_mode_gpu()
	return caffe.Net(prototxt, caffemodel, caffe.TEST)

def add_to_db():
	pass

def get_frame_from_video(path,frame_no):
	cap = cv2.VideoCapture(path)
	#frame_total = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
	#frame_no = (float(frame_no) /float(frame_total)
	cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,frame_no-1)
	ret, frame = cap.read()
	return frame

if __name__=="__main__":
	path = "/home/ubuntu/data/simple_coresets/"
	tree_path = "/home/ubuntu/data/coresets/"
	video_path = "/home/ubuntu/data/videos/"
	CLASSES = ('__background__',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')
	#Classes_Dict = {1:2,2:24,3:26,4:?,5:?,6:33,7:37,8:?,9:43,10:?,11:?,12:58,13:92,14:114,15:124,16:?,17:155,18:164,19:185,20:189}
	files = set([])
	net = init_net()
	while True:
		new_files, files = monitor_directory(path,files)
		for f in new_files:
			process_coreset(path + f,net)
		time.sleep(5)
