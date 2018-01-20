
ssd mobilenet checkpoint: http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2017_11_17.tar.gz

dataset source: http://www.robots.ox.ac.uk/~vgg/data/pets/
*note: dataset file name format 'image_class_name_ID.[jpg|gif|png]', class label with first letter as capital are
	cat images, otherwise dog images. Some images also have the wrong format(e.g. .jpg image but it's .png)
	if image_formater.py works as expected on other machine, it should throw error with the file names
	

tensorflow object detection api repo: https://github.com/tensorflow/models/tree/master/research/object_detection
*note: important to remember, generate_tfrecord.py depends on tensorflow object detection api, you need to export this path(ubuntu)
export PYTHONPATH=$PYTHONPATH:full/path/to/models/research:full/path/to/models/research/slim

generate_tfrecord.py original source: https://github.com/datitran/raccoon_dataset

xml_to_csv.py original source: https://github.com/datitran/raccoon_dataset

*note: generate_tfrecord.py and xml_to_csv.py is slightly modified to fit our annotation file format

folder structure:
./data/annotation -- annotation xml files
./data/test -- test data, images and xmls
./data/train -- training data, images and xmls
./data/train.record -- generated TFRecord data for training
./data/test.record -- generated TFRecord data for test
./data/[test|train]_labels.csv -- TFRecord generated using all files listed in this file
./data_info -- contains csv with all label available in the dataset (ID, BREED_TYPE, SPECIES[1 for cat, 2 for dog])
./training -- contains config file used in our project, original source: https://github.com/tensorflow/models/blob/master/research/object_detection/samples/configs/ssd_mobilenet_v1_coco.config
./images -- image to be processed

step to reproduce the data(ubuntu machine):
run > python3 image_formater.py
run > python3 data_maker_util.py
run > python3 xml_to_csv.py
run > python3 generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=data/train.record
run > python3 generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=data/test.record

before running the step above:
> copy all images from oxford-IIIT Pets Dataset to ./images or copy the images folder to this directory
> copy all xmls files from annotations/xmls to ./data/annotations
> export PYTHONPATH=$PYTHONPATH:full/path/to/models/research:full/path/to/models/research/slim

*note: before running all the scripts listed above, make sure you've installed 
all of the required libraries listed in requirement file


