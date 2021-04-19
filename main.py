import cv2
import boto3
import numpy as np
import subprocess

#click photo
cap = cv2.VideoCapture(0)

cap.set(3 , 1920)
cap.set(4 , 1080)

ret , photo = cap.read() 

cv2.imwrite("page.png",photo)

#photo = cv2.imread('page.png', cv2.IMREAD_GRAYSCALE)

cv2.imwrite("page.png",photo)

print(ret)
cap.release()

#upload photo in s3
#enter s3 bucket name
bucket_name = "" 
file_name = "page.png"

s3 = boto3.resource("s3") 
s3.Bucket(bucket_name).upload_file(file_name , file_name)

# Call Amazon Textract
textract = boto3.client('textract')

response = textract.detect_document_text(
    Document={
        
        'S3Object': {
            'Bucket': bucket_name,
            'Name': file_name,
            
        }
    }
)


with open('Dockerfile' , 'a' ) as dockerfile:

    for blocks in response['Blocks']:
      if blocks['BlockType'] == 'LINE':
          #print(blocks['Text'])
          dockerfile.write(blocks['Text'] + ' \n')

      elif blocks['BlockType'] == 'WORD':
          break 

    dockerfile.close()


#build image
#enter container image name
image_name = ''
build_image_status = subprocess.getstatusoutput(f'docker build -t {image_name} .')
print('image build!' if build_image_status[0] == 0 else 'error building image')

#push image
push_image = subprocess.getstatusoutput(f'docker push {image_name}')
print('image pushed to DockerHub' if push_image[0] == 0 else 'error pushing image')

#creating deployment
#Kubernetes master DNS
instance = ''

#Kubernetes deployment name
deployment_name = ''

#Kubernetes master key (.pem file)
master_key = ''
deployment_status = subprocess.getstatusoutput(
    f'ssh -i {master_key} {instance} sudo kubectl create deployment {deployment_name} --image {image_name} -- sleep infinity'
    )
    
print(
       'Deployment successful!' 
       if deployment_status[0] == 0 else
       'error'
     )
