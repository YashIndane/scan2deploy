import cv2
import boto3
import subprocess

#click photo
cap = cv2.VideoCapture(0)

cap.set(3 , 1920)
cap.set(4 , 1080)

ret , photo = cap.read()

#name of captured image file
file_name = ""

cv2.imwrite(file_name,photo)

print(ret)
cap.release()

#upload photo in s3

#enter s3 bucket name
bucket_name = "" 

s3 = boto3.resource("s3") 
s3.Bucket(bucket_name).upload_file(file_name , file_name)

#Call Amazon Textract
textract = boto3.client('textract')

response = textract.detect_document_text(
    Document={
        
        'S3Object': {
            'Bucket': bucket_name,
            'Name': file_name,
            
        }
    }
)

#Writing commands to the docker file from Textract response
with open('Dockerfile' , 'a' ) as dockerfile:

    for blocks in response['Blocks']:
      if blocks['BlockType'] == 'LINE':
          
          dockerfile.write(blocks['Text'] + ' \n')

      elif blocks['BlockType'] == 'WORD':
          break 

    dockerfile.close()

#build image

#container image name (username/repo:version)
image_name = ''

build_image_status = subprocess.getstatusoutput(f'docker build -t {image_name} .')
print('image build!' if build_image_status[0] == 0 else 'error building image')

#push image
push_image = subprocess.getstatusoutput(f'docker push {image_name}')
print('image pushed to DockerHub' if push_image[0] == 0 else 'error pushing image')

#creating deployment

#Kubernetes master DNS
master_DNS = ''

#Kubernetes master key path (.pem file)
key = ''

#Kubernetes deployment name
deployment_name = ''

deployment_status = subprocess.getstatusoutput(
    f'ssh -i "{key}" {master_DNS} sudo kubectl create deployment {deployment_name} --image {image_name}'
)

#exposing the deployment

#port at which the service inside container is running
port_no=

#type of service
TYPE=''

service_status = subprocess.getstatusoutput(
    f'ssh -i "{key}" {master_DNS} sudo kubectl expose deployment {deployment_name} --port={port_no} --type={TYPE}'
)    
    
print(
       'Deployment successful!' 
       if deployment_status[0] == 0 else
       'error'
)     
