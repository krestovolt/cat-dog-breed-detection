import os
import glob
import pandas as pd
import shutil
import operator

'''
important note: all functions in this file are tested only using ubuntu 16.04 environtment using python 3.4
'''

# function for writing log, per class training and test image count
# write output to data_distribution.txt file
def test_value(_train, _test, label_files):
    with open('data/data_distribution.txt','w') as log:
        msg = 'label count: {}'.format(len(label_files.keys()))
        print(msg)
        log.write(msg+'\n')
        msg = ('='*20)+'all data'+('='*20)
        print(msg)
        log.write(msg+'\n')
        for label, files in label_files.items():
            print(label,':',len(files))
            log.write('{} : {}\n'.format(label, len(files)))

        msg = ('='*20)+'train data'+('='*20)
        print(msg)
        log.write(msg+'\n')
        for label, files in _train.items():
            print(label,':',len(files))
            log.write('{} : {}\n'.format(label, len(files)))

        msg = ('='*20)+'test data'+('='*20)
        print(msg)
        log.write(msg+'\n')
        for label, files in _test.items():
            print(label,':',len(files))
            log.write('{} : {}\n'.format(label, len(files)))

# function for getting image class from image file name(e.g. "path/to/images/file/Abyssinian_1.jpg" => "Abyssinian")
def _extract_label(path, sep = '_'):
    file_name = os.path.basename(path)
    class_name = file_name.split(sep)[:-1]
    class_name = '_'.join(class_name)
    return class_name, file_name

# training and test data maker
# return both dictionary with image label as key map
# and list of images path used for that particular class label
def make_train_test_data(label_files_dict, train_ratio, test_ratio):
    train = {}
    test  = {}

    for label, files in label_files_dict.items():
        total_count = len(files)
        train_count = int(total_count * train_ratio)
        if label in train:
            train[label].extend(files[:train_count])
        else:
            train[label] = files[:train_count]
            
        if label in test:
            test[label].extend(files[train_count:])
        else:
            test[label] = files[train_count:]


    return train, test

# how to:
# make_lookup_dict(file_path=INSERT_ANNOTATIONS_FOLDER, label_dataframe_path=INSERT_CSV_LABEL_FILE)
def make_lookup_dict(file_path = 'data/annotations', label_dataframe_path = 'data_info/dataframe_label_breeds.csv'):
    data_info = pd.read_csv(label_dataframe_path, header=0)
    file_path = os.path.join(os.getcwd(), file_path)
    files = glob.glob(file_path + '/*.xml')
    label_to_id = {}
    id_to_label = {}
    label_to_files = {}

    for id, label in zip(data_info.head(50)['ID'],data_info.head(50)['BREED_TYPE']):    
        label_to_id[label] = id
        id_to_label[id] = label
        label_to_files[label] = []

    for file in files:
        label, image_file_name = _extract_label(file)

        label_to_files[label].append(image_file_name)

    data_info = None

    return label_to_id, id_to_label, label_to_files

# utility function for copying all files
def copy_to(dest, srcfiles, srcdir=None):
    for src in srcfiles:
        if srcdir != None:
            src = os.path.join(srcdir, src)
        dest_path = os.path.join(dest, os.path.basename(src))
        shutil.copy(src, dest_path)        

# utility function to create labels_lookup_val.pbtxt content (important)
def _item_writer(label, label_id):
    text = 'item {\n'
    text += '\tid: {}\n'.format(label_id)
    text += '\tname: \'{}\'\n'.format(label)
    text += '}\n'
    return text

def make_map_pbtxt_file(dest = 'data/labels_lookup_val.pbtxt'):
    label_to_id, _, _ = make_lookup_dict()
    sorted_label_to_id = sorted(label_to_id.items(), key=operator.itemgetter(1))    

    with open(dest, 'w') as f:
        for label, lid in sorted_label_to_id:
            f.write(_item_writer(label, lid))
####################################

# return dictionary with structure {class_name:[array_of_images_path_to_be_used]}
# each for traning and test with separated dictionary
def make_data(train_ratio, test_ratio, return_original = False):
    
    label_to_id, id_to_label, label_to_files = make_lookup_dict()    

    train, test = make_train_test_data(label_to_files, train_ratio = train_ratio, test_ratio = test_ratio)

    if return_original:
        return train, test, label_to_files
    else:
        return train, test

if __name__ == '__main__':
    train, test, label_to_files = make_data(0.8, 0.2, return_original = True)
    test_value(train, test, label_to_files)

    #annotation folder path
    xml_path = os.path.join(os.getcwd(), 'data/annotations')
    #images path
    image_path = os.path.join(os.getcwd(), 'data/new_images')
    #folder for outputing training image and xml
    train_dst = os.path.join(os.getcwd(), 'data/train')
    os.makedirs(train_dst, exist_ok=True)
    #folder for outputing test image and xml
    test_dst = os.path.join(os.getcwd(), 'data/test')
    os.makedirs(test_dst, exist_ok=True)

    print('copying file training and testing in progres... please wait....')
    #copy data to train or test directory
    for label, files in train.items():
        copy_to(train_dst, files, xml_path)
        img_file = [file.split('.')[0]+'.jpg' for file in files]
        copy_to(train_dst, img_file, image_path)        

    for label, files in test.items():
        copy_to(test_dst, files, xml_path)
        img_file = [file.split('.')[0]+'.jpg' for file in files]
        copy_to(test_dst, img_file, image_path)
    ######################################