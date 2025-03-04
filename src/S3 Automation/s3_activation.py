import boto3
import os 

#Information to access the bucket
s3 = boto3.client(
    "s3",
    aws_access_key_id="", # Replace with access key
    aws_secret_access_key="", # Replace with secret access key
    region_name="" # Replace with region 
)

# Getting your local project folder 
LOCAL_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))


# Bucket Name
bucket_name = 'mini-sumo-bucket'

def upload_photos(flag,sumo,not_sumo):
    folders_to_upload = []
    if flag:
        folders_to_upload.append('Flag/')
    if sumo:
        folders_to_upload.append('MiniSumo/')
    if not_sumo:
        folders_to_upload.append('NotMiniSumo/')

    for folder in folders_to_upload:
        folder_path = os.path.join(LOCAL_FOLDER_PATH,folder)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.startswith('.'):
                    continue
                else:
                    local_file_path = os.path.join(root,file)
                    s3_key = os.path.relpath(local_file_path, LOCAL_FOLDER_PATH)
                    s3.upload_file(local_file_path,bucket_name,s3_key)
                    print(f'Uploaded {local_file_path} to s3://{bucket_name}/{s3_key}')
                    

def main():
    flag = input("You want to upload to Flag folder?[Y/N]: ").strip().lower()
    flag = flag in ['y','yes'] #Convert to true or false
    sumo = input("You want to upload to Sumo folder?[Y/N]: ").strip().lower()
    sumo = sumo in ['y','yes']
    not_sumo = input("You want to upload to Not Sumo folder?[Y/N]: ").strip().lower()
    not_sumo = not_sumo in ['y','yes']
    print("########### UPLOADING FILES ###########\n")
    upload_photos(flag,sumo,not_sumo)
    print("\n########### PROCCESS DONE ###########")

if __name__ == '__main__':
    main()


    


