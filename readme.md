
### Folder Structure:
| Path | Description |
|------|------|
|./data/annotation | annotation xml files |
|./data/test | test data, images and xmls |
|./data/train | training data, images and xmls |
|./data/train.record | generated TFRecord data for training|
|./data/test.record | generated TFRecord data for test|
|./data/[test/train]_labels.csv | TFRecord generated using all files listed in this file|
|./data_info | contains csv with all label available in the dataset (ID, BREED_TYPE, SPECIES[1 for cat, 2 for dog])|
|./training | contains config file used in this project and checkpoint file, original source:[ssd_mobilenet_v1_coco.config](https://github.com/tensorflow/models/blob/master/research/object_detection/samples/configs/ssd_mobilenet_v1_coco.config) |
|./images | image to be processed |

### Step To Reproduce TFRecord Data(ubuntu machine):
- download [oxford-IIIT Pets Dataset](http://www.robots.ox.ac.uk/~vgg/data/pets/), both [images](http://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz) and [annotations](http://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz)
- copy all images from oxford-IIIT Pets Dataset to ./images or copy the images folder to this directory
- copy all xmls files from annotations/xmls to ./data/annotations
- then run this command on your terminal:

```sh
$ python3 image_formater.py
$ python3 data_maker_util.py
$ python3 xml_to_csv.py
$ export PYTHONPATH=$PYTHONPATH:FULL/PATH/TO/models/research:FULL/PATH/TO/models/research/slim
$ python3 generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=data/train.record
$ python3 generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=data/test.record
```

- after that, copy folder: ./training; ./data; ./eval; to models/research/object_detection
- also put your fine tune checkpoint to models/research/object_detection, or change the 'fine_tune_checkpoint' value in breed_detect.config
*note: this is assuming the working directory is in this project folder root

### Training
```py
# breed_detect.config  line 158, make sure this pointing to the checkpoint you want to use
# in this case ssd_mobilenet_v1_coco_2017_11_17
fine_tune_checkpoint: "ssd_mobilenet_v1_coco_2017_11_17/model.ckpt"
```
```sh
$ cd PATH/TO/models/research/object_detection
$ export PYTHONPATH=$PYTHONPATH:FULL/PATH/TO/models/research:FULL/PATH/TO/models/research/slim
$ python3 train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/breed_detect.config
```
### Eval
```sh
$ cd PATH/TO/models/research/object_detection
$ export PYTHONPATH=$PYTHONPATH:FULL/PATH/TO/models/research:FULL/PATH/TO/models/research/slim
$ python3 eval.py --logtostderr --checkpoint_dir=./training \
--eval_dir=./eval --pipeline_config_path=./training/pipeline.config
```

### Resource
xml_to_csv.py and generate_tfrecord.py source: [datitran's repo](https://github.com/datitran/raccoon_dataset)
[tensorflow models](https://github.com/tensorflow/models)
[tf object detection api](https://github.com/tensorflow/models/tree/master/research/object_detection)
[SSD(Single Shot Detector)](https://arxiv.org/abs/1512.02325)
[MobileNets](https://arxiv.org/abs/1704.04861)
