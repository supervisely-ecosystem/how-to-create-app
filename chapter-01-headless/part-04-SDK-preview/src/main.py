import supervisely_lib as sly
import os
import json
from dotenv import load_dotenv  # pip install python-dotenv\

# Loading env files
load_dotenv("../debug.env")
load_dotenv("../secret_debug.env", override=True)

# Extracting variables
address = os.environ['SERVER_ADDRESS']
token = os.environ['API_TOKEN']

team_id = int(os.environ['context.teamId'])
workspace_id = int(os.environ['context.workspaceId'])
project_id = int(os.environ['modal.state.slyProjectId'])

# Initialize API object
api = sly.Api(address, token)

# Downloading Project
project_local_dir = './project_local_dir/'

if sly.fs.dir_exists(project_local_dir):
    sly.fs.clean_dir(project_local_dir)  # clean dir before download

sly.download_project(api=api,
                     project_id=project_id,
                     dest_dir=project_local_dir)

# Getting project meta (Base project information — Labels, Shapes, Colors etc.)
project_meta_json = api.project.get_meta(project_id)  # we could also open a local file ./project_local_dir/meta.json
project_meta = sly.ProjectMeta.from_json(project_meta_json)

# Getting list of datasets folders in project
project_datasets = [potential_dir for potential_dir in os.listdir(project_local_dir)
                    if os.path.isdir(os.path.join(project_local_dir, potential_dir))]


# Getting list of Annotations in project
images_annotations = []

for current_dataset in project_datasets:  # for each dataset in project
    dataset_annotations_dir_path = os.path.join(project_local_dir, current_dataset, 'ann')
    annotation_filenames = os.listdir(dataset_annotations_dir_path)

    for annotation_filename in annotation_filenames:  # for each annotation file in dataset
        with open(os.path.join(dataset_annotations_dir_path, annotation_filename), 'r') as ann_file:
            image_annotations_json = json.load(ann_file)

        image_annotations = sly.Annotation.from_json(image_annotations_json, project_meta)
        images_annotations.append(image_annotations)  # store annotation


# Let's count lemons!

count = 0
class_of_interest = 'lemon'

for image_annotation in images_annotations:
    for label in image_annotation.labels:
        if label.obj_class.name == class_of_interest:
            count += 1

print(f'{project_id=} contains {count} {class_of_interest}(-s)')
