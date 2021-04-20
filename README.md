![](https://img.shields.io/badge/python-3-lightgrey)

# scan2deploy

Just write down your docker file , take a snap and deploy the app in Kubernetes!

## Requirements

Install OpenCV by

```
pip install opencv-python
```

Do this if your Kubernetes cluster is running in aws ->

Install boto3 (calls APIs of AWS services) by

```
pip install boto3
```

Install aws command line tool by

```
pip install awscli
```

Since I am running the code on Windows machine , Docker Desktop is required to get the docker enviornment for building and pushing images
Download Docker Desktop from -> [link](https://docs.docker.com/docker-for-windows/install/)


## Enviornment settings

Docker Desktop-

After opening Docker Desktop, provide your Docker Hub credentials so that pushing images happens smoothly.

AWS-

configure AWS-CLI by -
```
aws configure
```

Create a bucket in S3 (here the snap will be uploaded)

```
aws s3api create-bucket --bucket <bucket-name> --region <region-name> --create-bucket-configuration LocationConstraint=<region-name>
```

Have the Kubernetes master key (.pem file) in the working directory, so that deployment can be made using ssh

## Working and Usage

The image of your page is uploaded in the S3 bucket. This image is then processed by ```AWS Textract``` service, which extracts the text from it line by line.
More on AWS Textract -> [link](https://aws.amazon.com/textract/)

```
textract = boto3.client('textract')

response = textract.detect_document_text(
    Document={
        
        'S3Object': {
            'Bucket': bucket_name,
            'Name': file_name,
            
        }
    }
)
```

the lines are written in the Dockerfile, which is then used to build the ```container image``` and push it to Docker Hub.

After pushing the image to Docker Hub, the code runs the command to create a deployment using the image pushed (using ssh) and expose it to create a service.

To get the port number where the service is launched, go to the master node and run ->

```
kubectl get svc
```

To get the IP of  node on which the pod is launched run this ->

```
kubectl describe pod <name-of-pod>
```

The app can be accessed by ```http://<IP-of-node>:<port_no>```
















