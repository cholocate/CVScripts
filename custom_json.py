import os 
import json 

# Users\Bimr 

# =====================================
# PROPOSAL OF CATEGORY STANDARDIZATION 
# =====================================
# "categories": [
# {
#   "id": 0,
#   "name": "heads",
#   "supercategory": "none"
# },
# {
#   "id": 1,
#   "name": "head",
#   "supercategory": "heads"
# }
# ] 

# =====================================
# REQUIREMENTS 
# =====================================
# 1) Non-overlapping information across multiple annotation files
# 2) Consistent classification and labelling across multiple annotation files
# 3) Clear and Non-ambiguity reformatting 
#   3A) Names are labelled chronologically and in ascending order after merge. 
#   3B) Functions are separated and each serves to modify json files

# =====================================
# PRE-REQUISITE INFORMATION
# =====================================
# 1) images[id] == annotations[image_id] 
# 2) annotations[id] represents a bounding box and maybe of the same image_id
#   1) + 2) Then we need to make sure that images[id] and annotations[id]
#           are unique and consistent after merging
#           We also need to make sure that annotations[id] increments the same as
#           the two before. 


# =====================================
# FUNCTIONS 
# =====================================
# Renaming file names based on a starting number (non-zero if continuation of JSON files)
#   Keep track of number incremented til so far 
#   "000" + number

# Delete non-relevant categories, reassign category_id, 
    # update starting number of images[id]/annotations[images_id] 
    # update starting number annotations[id] of subsequent files 

# Rename and Delete should be done at the same time
#   Rename requires unique identifier to be update to date
#   Delete can be done at the same time. 
# Update images[id] and annotations[image_id] at the same time to start at previous ending number
# Update annotations[id] of subsequent files to start at previous ending number

# Merging JSON files and merging image files together

# =====================================
# FIX
# =====================================
# 0.0 : data['annotations']['image_id'] needs to match data['images']['id'] after re-indexing. 
# 0.1 : Separate loops for image id and annotation image id change. 
# 0.2 : Map to avoid per iteration error



def rename_delete_replace(starting_number_image, starting_number_anno, image_folder, annotation_file, delete_id, replace_id_from, replace_id_to):
    with open(annotation_file) as f:
        annotation_data = json.load(f)

    # Delete annotations
    annotation_data['annotations'] = [anno for anno in annotation_data['annotations'] if anno['category_id'] not in delete_id]

    # Replace category IDs in annotations
    for anno in annotation_data['annotations']:
        if anno['category_id'] in replace_id_from:
            anno['category_id'] = replace_id_to

    image_id_present = set(anno['image_id'] for anno in annotation_data['annotations'])
    images_to_keep = []

    # Delete images and keep track of the remaining ones
    for image in annotation_data['images']:
        if image['id'] in image_id_present:
            images_to_keep.append(image)
        else:
            print(image['id'])
            os.remove(os.path.join(os.getcwd(),image_folder, image['file_name']))

    annotation_data['images'] = images_to_keep
    
    # Renaming and renumbering images
    # for each image, find all annotations with the same image_id, update these annotations to the new id 
    old_to_new_img_id = {}
    for i, image in enumerate(annotation_data['images']):
        new_id = starting_number_image + i
        new_file_name = f"{new_id:012}.jpg"
        new_file_path = os.path.join(os.getcwd(), image_folder, new_file_name)
        os.rename(os.path.join(os.getcwd(),image_folder, image['file_name']), new_file_path)
        # FIX 0.2 [Try storing into map and then updating later]
        old_to_new_img_id[image['id']] = new_id

        image['file_name'] = new_file_name
        image['id'] = new_id

    # Renumbering annotation IDs and updating image_id
    for i, anno in enumerate(annotation_data['annotations']):
        anno['id'] = starting_number_anno + i
        anno['image_id'] = old_to_new_img_id[anno['image_id']] 

        

    end_number_image = starting_number_image + len(annotation_data['images'])
    end_number_anno = starting_number_anno + len(annotation_data['annotations'])

    # Save the updated annotation file
    with open(annotation_file, 'w') as f:
        json.dump(annotation_data, f, indent=4)

    return end_number_image, end_number_anno


def combine_annotation_files(annotation_files, combined_file):
    combined_data = {
        "categories": [],
        "images": [],
        "annotations": []
    }

    category_id_mapping = {}

    for annotation_file in annotation_files:
        with open(annotation_file) as f:
            annotation_data = json.load(f)

        # Update category IDs and store the mapping
        for category in annotation_data['categories']:
            if category['id'] not in category_id_mapping:
                category_id_mapping[category['id']] = len(combined_data['categories'])
                combined_data['categories'].append(category)
            
        # Update image and annotation information
        for image in annotation_data['images']:
            combined_data['images'].append(image)
        
        for annotation in annotation_data['annotations']:
            combined_data['annotations'].append(annotation)

    # Save the combined annotation data to a file
    with open(combined_file, 'w') as f:
        json.dump(combined_data, f,indent=4)

def debugging(annotation_file): 
    with open(annotation_file) as f: 
        annotation_data = json.load(f) 

    for image in annotation_data['images']: 
        assert(str(image['id']) in image['file_name'])

# do reformatting one by one for debugging purposes
def main(): 
    print(os.getcwd())
    
    # ./Desktop/merge
    # merge
    #   anno.json
    #   train/val/test folder

    # end_no_img, end_no_anno = rename_delete_replace(841, 2314,"./Desktop/merge/valid_4", "./Desktop/merge/valid_4.json", [2,3,4,6], [5], 1)
    # print(end_no_img, end_no_anno)

    # combine_annotation_files(["./Desktop/merge/train_0.json", "./Desktop/merge/train_1.json", "./Desktop/merge/train_2.json", "./Desktop/merge/train_3.json", "./Desktop/merge/train_4.json"], "./Desktop/merge/train_comb.json")

    # combine_annotation_files(["./Desktop/merge/valid_0.json", "./Desktop/merge/valid_1.json", "./Desktop/merge/valid_2.json", "./Desktop/merge/valid_3.json", "./Desktop/merge/valid_4.json"], "./Desktop/merge/valid_comb.json")
    

main()

