import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm

def xml_to_csv(path):
    xml_list = []
    _files = glob.glob(path + '/*.xml')
    for xml_file in tqdm(_files, total = len(_files)):
        
        image_name = os.path.basename(xml_file)
        image_name = image_name.split('.')[0] + '.jpg'
        class_name = image_name.split('_')[:-1]
        class_name = '_'.join(class_name)

        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (image_name,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     class_name,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )            
            xml_list.append(value)
            # print('',
            #     image_name,'\n',
            #     class_name,'\n',
            #     root.find('size')[0].text,'\n',
            #     root.find('size')[1].text,'\n',
            #     member[0],'\n',
            #     member[4][0],'\n',
            #     member[4][1],'\n',
            #     member[4][2],'\n',
            #     member[4][3],'\n')
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


# def main():
#     image_path = os.path.join(os.getcwd(), 'annotations')
#     xml_df = xml_to_csv(image_path)
#     xml_df.to_csv('raccoon_labels.csv', index=None)
#     print('Successfully converted xml to csv.')

def main():
    for directory in ['train','test']:
        data_path = os.path.join(os.getcwd(), 'data/{}'.format(directory))
        xml_df = xml_to_csv(data_path)
        xml_df.to_csv('data/{}_labels.csv'.format(directory), index=None)
        print('Successfully converted xml to csv.')

# def main():    
#     image_path = os.path.join(os.getcwd(), 'annotations/xmls')
#     print(image_path)
#     xml_df = xml_to_csv(image_path)
#     # xml_df.to_csv('data/{}_labels.csv'.format(directory), index=None)
#     print('Successfully converted xml to csv.')

if __name__ == '__main__':
    main()
