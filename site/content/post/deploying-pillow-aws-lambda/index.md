+++
showonlyimage = false
draft = false
image = "img/posts/pillow.jpg"
date = "2017-11-21T18:25:22+05:30"
title = "Deploying PIL/Pillow to AWS Lambda "
author = "diego"
tags = ["python", "pil", "pillow", "aws-lambda"]
categories = ["articles"]
weight = 0
+++

When going serverless with Python and AWS Lambda, one of the first things we want to do is upload libraries, such as PIL. There are amazing tools to do this, such as Zappa, but... what if we want to do it with that?
<!--more-->

We are going to use Docker to build our libraries. If it doesn't work for the library you are trying to compile, you should do the same using one the Amazon EC2 instances as described [in the documentation](http://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html).

Let's create a file `ProcessMediaFile.py` that grabs an image as soon as it's uploaded, resizes it, and puts it in another bucket:

	import boto3
	import os
	import sys
	import uuid
	from PIL import Image, ImageOps
	    
	s3_client = boto3.client('s3')
	    
	def resize_image(image_path, resized_path):
	    with Image.open(image_path) as image:
	        thumb = ImageOps.fit(image, (200,200), Image.ANTIALIAS)
	        thumb.save(resized_path)
	    
	def lambda_handler(event, context):
	    for record in event['Records']:
	        bucket_input = record['s3']['bucket']['name']
	        bucket_output = "output-bucket-name"
	               
	        key = record['s3']['object']['key']
	        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
	        upload_path = '/tmp/resized-{}'.format(key)
	       
	        s3_client.download_file(bucket_input, key, download_path)
	        resize_image(download_path, upload_path)
	        s3_client.upload_file(upload_path, bucket_output, key)

The entrypoint will be the `lambda_handler` function, which we will set later.

Then, we launch a Docker container, as follows:

	docker run --rm -it -v "%cd%:/code" lambci/lambda:build-python3.6 sh

That's if we are using Windows, because of the `%cd%` part. If you are on Linux use `${PWD}` instead.

There we will launch an shell in a container, running an image that is pretty similar to Lambda's, although it might not always work (in those cases, use an EC2 instance).

Then, navigate to our `/code` directory, create a Python virtual environment, activate it, and install the library you want. Or, basically, this:

	cd /code
	virtualenv env
	source env/bin/activate
	pip install pillow

Once you have installed Pillow, you can press `Ctrl-C` to kill the container. Back on the host, you need to put the libraries folders in the root directory. So, for example, move the folder `env/lib/python3.6/site-packages/PIL` to the root directory where your .py file is.

It should look like this:

- ProcessMediaFile.py
- PIL/...

ZIP those 2 things and upload them to AWS Lambda. The name of your handler will be ProcessMediaFile.lambda_handler. Also, don't forget to give access to your Service Role in IAM. In my case, my policy looks something like this:

	{
	    "Version": "2012-10-17",
	    "Statement": [
	        {
	            "Effect": "Allow",
	            "Action": [
	                "logs:CreateLogGroup",
	                "logs:CreateLogStream",
	                "logs:PutLogEvents"
	            ],
	            "Resource": "arn:aws:logs:*:*:*"
	        },
	        {
	            "Effect": "Allow",
	            "Action": [
	                "*"
	            ],
	            "Resource": [
	                "arn:aws:s3:::input-bucket/*",
	                "arn:aws:s3:::output-bucket/*"
	            ]
	        }
	    ]
	}