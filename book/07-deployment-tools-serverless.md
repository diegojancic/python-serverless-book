# Chapter 7: Deployment Tools II: Serverless Framework

Manually creating Lambdas and configuring the different services and permissions is definitely something we want to avoid as our applications become more and more complex. We have explored one deployment tool that made our life easier when it comes to deploying our applications, but there are others with significant differences.

In this chapter we are going to explore another framework that lets us handle the packaging and deployment process. We will deploy the same application we did in the last chapter and also explore the different configuration options it offers.

Being one of the oldest players among these tools, it got a unique name and domain: Serverless Framework and www.serverless.com. It's probably the most mature framework and it has a pretty extensive community; it has over 3 times the number of 'Stars', 'Forks', and 'Watchers' that Zappa has on GitHub.

Let's see what this can do. Let's dive in.

## Multi-Language, Multi-Platform

The Serverless Framework (SF from now on) is an open-source, MIT Licensed, cross-platform and cross-language framework for deploying serverless applications. The company behind it supports the framework and also offers commercial support and development services.

SF can deploy applications to AWS as well as Microsoft's Azure, Google Cloud Platform, and others. Furthermore, the functions can be developed in multiple languages, including Python, NodeJS, Java, C#, and Ruby to name a few. Of course, this is not a feature specific to the SF, but an AWS Lambda one. Lambda can run functions written in any of those languages and the SF interacts with any of them seamlessly.

The framework itself is built in NodeJS, which means we will need to have the NodeJS runtime installed. On top of it, the SF works with a plugin architecture that allows setting it up in many different ways at the expense of slightly more configuration work.

SF allows deploying any function and attaching events to it and having it executed in response to changes in other AWS services or on a schedule. We'll use a plugin that provides the WSGI interface between Lambda and a Python web application framework, like Django or Flask.

## Creating the First Application

For the sake of testing the SF deployments, let's start by creating a simple Hello World application in Flask.

Before we begin, we need to download and install NodeJS, which can be found at https://nodejs.org. When installed, it will also install npm which is the *Node Package Manager* that we'll use to install the SF and other dependencies. We are using Node version 10.15 and npm version 6.4.1, even though those are LTS versions and you should be fine using the latest Node 10.x version.

Let's start by creating a Flask application as we have done before. Create the directory, a virtual environment, install Flask, save the requirements in a .txt file, and deactivate the environment (output omitted):

```bash
> mkdir first-app
> cd first-app
> virtualenv env
> source env/bin/activate
> pip install flask
> pip freeze > requirements.txt
> deactivate
```

Now, let's create the sample Hello World application as we did before. Create an app.py file as follows:

**first-app/app.py**
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
```

With our Flask application ready, the next step is to install the SF:

```bash
> npm init -f
> sudo npm install -g serverless
```

Execute this to download and install the SF on your computer; the -g flag indicates that it will be installed globally (and not just in the current directory) and will be available for any future project. For Windows, remove the sudo part as that's required only in Linux or Mac to run the install using the root account.

The `npm init` command needs to be executed in the project directory. It will create a package.json file that contains the list of installed plugins (among other things that we won't be using). Use the -f flag to skip all questions or remove it to be asked about the project name, author, license, etc.

In order to configure SF we have 2 options: start from scratch and start from a template. Most examples out there start from a template, and it might be a good idea in many cases. However, the templates also add some things that are not necessary and make it a bit harder to understand what we are doing exactly.

If you decide to start from a template, just run one of the following commands:

```bash
> serverless create --template aws-python3
> sls create -t aws-python3
```

The second line starting with `sls` is the short version of the first command. What it does is download one of the available templates to use as a starting point. You can also run `sls create -h` to see the list of available templates.

In our case, we won't start from a template and, instead, create the configuration file manually. The SF configurations are stored in a file called serverless.yml that can be created manually. This is how our configuration file begins:

**first-app/serverless.yml**
```yaml
service: first-app

provider:
  name: aws
  runtime: python3.7
```

We have specified the name of the application using the 'service' attribute. Then, the provider, which in our case is AWS, and the language or runtime is Python 3.7. Other available options are 'stage' which defaults to 'dev'; 'region' which defaults to 'us-east-1'; and memorySize which defaults to '1024'.

Once we have the configuration file created, we can run commands using the SF CLI. For example, we are going to need 2 plugins in order to run our Flask application, which will be installed with the `sls plugin install` command:

```bash
> sls plugin install -n serverless-wsgi
> sls plugin install -n serverless-python-requirements
```

The -n flag stands for 'Name'. The first plugin, serverless-wsgi, will be used to interface between the Lambda environment and any WSGI type of application. Both Flask and Django applications will require this. The second plugin, serverless-python-requirements, packages the requirements in the requirements.txt file along with the application files.

Using the SF plugin install command will perform 2 actions internally: the package is installed using NPM and the plugin name is added to the yml configuration file. In other words, instead of executing those commands, we could run `npm install --save-dev [plugin-name]` and then add them to the configuration file:

**first-app/serverless.yml**
```yaml
...
plugins:
  - serverless-wsgi
  - serverless-python-requirements
```

Once the plugins are in place, they need to be configured. Also in the serverless.yml:

**first-app/serverless.yml**
```yaml
...
custom:
  wsgi:
    app: app.app
  pythonRequirements:
    dockerizePip: non-linux
```

There are 2 subsections under the 'custom' section; one for each plugin. The WSGI only requires one parameter and that's the name of the application to run. Since our application is in app.py and the Flask variable is called 'app', the resulting application name will be app.app. While it might sound confusing, most examples follow this convention of using 'app' as the name for both the file and the Flask application.

The pythonRequirements subsection allows us to specify how the requirements will be packaged. By default the requirements will be downloaded or compiled to be included in the deployment package. However, because the packages need to be compiled in the same OS that Lambda uses, the plugin allows compiling the packages automatically using Docker. The dockerizePip option can then be set to 'true' or 'false' to enable or disable Docker, or to the special value of 'non-linux'. The 'non-linux' keyword tells the plugin to use Docker only if the OS we run the deploy on is not running Linux.

The final step before we can actually deploy our application is to configure the Lambda function that will be created:

**first-app/serverless.yml**
```yaml
...
functions:
  app:
    handler: wsgi.handler
    events:
      - http: ANY /
      - http: 'ANY {proxy+}'
```

We only have one function called 'app' that will respond to all HTTP events by calling the 'wsgi.handler' handler, which is provided by the WSGI plugin we installed before.

We can test our server locally, using the WSGI test server:

```bash
> sls wsgi serve
```

Now everything is set. To deploy the application, just run:

```bash
> sls deploy
```

If you're lucky and made no mistakes, the deployment will succeed and a URL will be provided.

## Deploying Our Django To-Do App

In the last chapter we configured our to-do application to connect to a PostgreSQL database and deployed it using Zappa. Here, we'll try to do the same thing, but this time using the SF.

We are going to use as a starting point the exact same code we used in the last chapter, but removing the env directory, the Zappa configuration file, and the requirements.txt file. You should only have 2 directories (todo and website) and one file (manage.py).

Let's create a virtual environment and install Django, psycopg2 (required to connect to the PostgreSQL server), and werkzeug (required to run the WSGI test server):

```bash
> virtualenv env
> source env/bin/activate
> pip install django==1.11 psycopg2 werkzeug
> pip freeze > requirements.txt
```

Let's create the initial serverless.yml configuration file, very similar to the one we used before:

**db-connect/serverless.yml**
```yaml
service: sls-db-connect

provider:
  name: aws
  runtime: python3.6

custom:
  wsgi:
    app: website.wsgi.application
  pythonRequirements:
    dockerizePip: non-linux

functions:
  app:
    handler: wsgi.handler
    events:
      - http: ANY /
      - http: 'ANY {proxy+}'
```

The only difference with the configuration file we used in our first application is the WSGI app attribute. While for Flask we used app.app, here we are using website.wsgi.application because our project/directory is called 'website', and the 'wsgi.py' defines the 'application' variable.

Also, we need to create our NPM environment and install the same plugins we used in our previous application:

```bash
> npm init -f
> sls plugin install -n serverless-wsgi
> sls plugin install -n serverless-python-requirements
```

If you took the RDS server down (you should have), then you will have to create the database using the AWS Console again. Once the PostgreSQL server is running, we need to update the application configurations. In settings.py, we need to update the database location, username, and password. In the serverless.yml, we need to include the VPC and Security Groups name.

Let's recap a little bit. The Lambda function will connect to our database and, unless the database is publicly accessible (not recommended), both the Lambda and the database server should be in a VPC. Also, the DB server can be configured to allow connections only from a certain IP-range, or from a group of computers/services (a.k.a. Security Groups).

Then, in order to update our configurations, we need to know where the VPC and the SG where our database is. If you made your database publicly available and you don't mind the risk of exposing your data to the world, you can skip this step. Since the data of our to-do application is very sensitive, let's find the IDs of our VPC subnets and SGs:

```bash
> aws rds describe-db-instances | grep "subnet"
        "SubnetIdentifier": "subnet-10714f2f",
        "SubnetIdentifier": "subnet-62e73e28",
        "SubnetIdentifier": "subnet-cd55e5c2",
        "SubnetIdentifier": "subnet-d290858f",
        "SubnetIdentifier": "subnet-ed9f88c2",
        "SubnetIdentifier": "subnet-b30fe2d4",

> aws rds describe-db-instances | grep "sg-"
    "VpcSecurityGroupId": "sg-2c439565"
```

With those IDs (starting with subnet- or sg-), we can update the SF configuration file:

**db-connect/serverless.yml**
```yaml
...
provider:
  name: aws
  runtime: python3.6
  vpc:
    securityGroupIds:
      - sg-2c439565
    subnetIds:
      - subnet-10714f2f
      - subnet-62e73e28
...
```

With the VPC options set, let's deploy our application:

```bash
> sls deploy
```

During the deployment, you should see something like this:

```
...
Serverless: Uploading service .zip file to S3 (38.89 MB)
...
```

Almost 40MB for a simple application? That's way too much. The generated package is located inside a hidden .serverless directory. Looking into it, we can see that the env folder is being included, while it's not necessary.

Fortunately, it's possible to manually include or exclude the files that need to be deployed. Update our .yml file one more time:

**db-connect/serverless.yml**
```yaml
...
package:
  exclude:
    - env/**
```

When that directory gets excluded, the package size goes down to 12.68 MB. Much better! All the dependencies will still be deployed and placed in the root of our package, so there's no need for that virtual environment folder that includes, among other things, the Python runtime.

After the function gets deployed and for it to work, we need to execute the database migrations. If the database can be accessed remotely, we can execute `python manage.py migrate` to execute the migrations locally and connect to the remote database. If that's not possible, the migrations need to be executed from the Lambda, as follows:

```bash
> sls wsgi manage --command migrate
```

Launch the URL provided after executing the *deploy* command and you should have the Django application working serverlessly again, this time using the Serverless Framework.

## Environment Setup & Workflow

As an application becomes more and more complex, we need to make things more automatic, dynamic, and customizable. Using Lambda Environment Variables is one of the options to store configurations that are needed during runtime. The recommendation is to set up different stages for, at least, 'development' and 'production', and use different AWS accounts for them. With the environments being completely isolated, there's less risk of configurations mixing between environments (such as connecting to the same database).

Environment variables are useful to define where our application has to connect to (whether we are talking about a database or a remote API endpoint), what email server to use, whether a specific feature is enabled or not, and many other things that define how the application will work.

SF uses a 'dev' stage by default, but we can define as many as we want. Also, we can make environment variables change depending on the stage. I'll leave it up to you to set up the new project, create the virtual environment, install Flask, and set up NPM with the 2 serverless plugins we used before.

Our application will be trivially simple as we don't want to get distracted with all the code not specific to this particular subject. The example below will just print out 2 variables—DATABASE_URL and REMOTE_API. In a real-world application, you would use such information to connect to remote servers, but for the sake of simplicity, just see how we can configure those variables:

**stages/app.py**
```python
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def print_env_vars():
    db_url = os.environ.get("DATABASE_URL")
    remote_api = os.environ.get("REMOTE_API")
    return "DB URL {db_url}<br>Connected to {remote_api}" \
        .format(db_url=db_url, remote_api=remote_api)
```

Now, let's see how we define the stage and the environment variables.

### Setting the Stage

The stage name can be set at 3 levels:

- **Default stage name**: dev.
- **Configuration file**: use 'stage: production' under the 'provider' option to set a global stage name.
- **CLI**: Execute the CLI commands using the --stage parameter. For example, `sls deploy --stage prod`.

### Variables

We can define as many additional options as we want under the 'custom' section in the serverless.yml file:

**stages/serverless.yml**
```yaml
...
custom:
  vars:
    CURRENT_STAGE: dev
```

We have defined a variable called *custom.vars.CURRENT_STAGE* and assigned the stage name 'dev'.

Let's see how we can reference a variable before we continue:

**${opt:name}**: references a command line argument.

**${self:name}**: references variables in the same serverless.yml file, where *name* is the full name of the variable, *custom.vars.CURRENT_STAGE* in the previous example.

**${env:name}**: references an environment variable.

**${ssm:name}**: references a variable stored in AWS Secure System Parameter Store, which we haven't talked about, but it's trivially easy if you want to jump in and store your configurations there.

**${s3:bucket/key}**: references a file stored in S3.

**${file(../filename):name}**: references a property stored in an external file. YML, JSON, and even JavaScript files are supported.

Also, it's possible to specify more than one parameter name with default values, in case the first one (or preceding ones) is empty, separating them by commas. For example:

```
${opt:stage, env:stage, self:provider.stage, 'dev'}
```

SF will try to read the --stage CLI argument; if not present, then the environment variable called 'stage'; if not present, the property 'stage' under the 'provider' section; lastly, if none is available, it would use 'dev' as a default.

Another cool trick that SF does is allowing the use of variables inside variables. If we want to define multiple options for each environment, one way would be to define them using the stage name:

**stages/serverless.yml**
```yaml
...
custom:
  mystage: ${opt:stage, 'dev'}
  stage-dev:
    url: http://sandbox.example.com/
    db: devdb
  stage-prod:
    url: http://api.example.com/
    db: realdb
```

Then, we can use the 'environment' section to create environment variables that can be read by our application (using os.environ in Python). For example, to define them for all the functions:

**stages/serverless.yml**
```yaml
...
provider:
  name: aws
  environment:
    url: ${self:custom.stage-${self:custom.mystage}.url}
    db: ${self:custom.stage-${self:custom.mystage}.db}
```

The URL will be *sandbox.example.com* if the stage is 'dev' and *api.example.com* for the production stage. The variable name assigned to both environment variables will depend on another variable, this time set in the configuration file or using the CLI.

The options are many now: the parameters can be read from different sources and combined together. For more complex scenarios, a JavaScript function can be used to generate the resulting value, extending the limits even further.

## Multiple Functions and Packaging

Lambda functions need to be fast. Fast means that only the required code is deployed in the function code, making it lightweight and reducing the cold starts. As an application becomes larger and larger, more dependencies are added and deployments become slower; cold starts take longer; and we get closer to the 50MB code size limitation that Lambda has.

To reduce these issues and keep our application working fast, we can split the code into multiple different functions. Imagine our application has 2 parts: first, a simple web backend that lets the user upload and view images and second, a background process that resizes and optimizes the images uploaded for faster delivery. This is a very common use case as most modern cameras and phones produce pictures that are at least 5MB, while websites usually shouldn't deliver images that are larger than 500KB as a general rule.

We'll develop a full example in a future chapter, including the full website and the background Lambda function that processes the images, so we aren't going to go through the code details for now. However, for one of those Lambda functions, we are going to use Flask and it's important to keep startup times to a minimum. For the other function, we are going to use Pillow, which is a library for image processing. Pillow, as well as many other useful libraries in Python, is pretty big and, as we need more external libraries, the Lambda functions might start to slow down.

### The Web App

The web application will use Flask and have 3 routes configured. The first one will return a form with the following HTML:

```html
<form action='/upload' method='POST' enctype='multipart/form-data'>
   <input type='file' name='image'/>
   <button>Submit</button>
</form>
```

That's a basic form that allows selecting one file and submitting it. When submitted, the file is POSTed to the second path, which is /upload.

When the file is received via an HTTP POST in the /upload route, it's sent to S3 and stored there. The 3rd route in the application will return an HTML \<img /\> with the link to the image.

### The S3 Event Handler

When a file gets uploaded to the S3 bucket, the second Lambda function that has the Pillow library installed needs to be executed. This function will download the recently uploaded file, resize it to specific dimensions, and then re-upload it.

With this 2-function process, the images get processed asynchronously. The web application will only have the bare minimum requirements while the non-essential libraries will run with a small delay without affecting the response times of the main function.

In the simple example developed in this chapter, we will handle only one file. When uploaded, it will be stored as uploaded.jpg in the S3 bucket and, after being processed by the resize function, the resized version of the file will be saved as resized.jpg.

### Configurations

The code for handling the file upload from the client, then to S3, and resizing the images would be a bit long and distract us from the core SF configurations. Check the full source code in the GitHub repository for complete examples.

To configure our application, we need to do the following. Both of our functions need to be placed in one subdirectory of our project, each with its own virtual environment and Python files.

Now, we are ready to configure it:

**packaging/serverless.yml**
```yaml
service: image-uploader

provider:
  name: aws
  runtime: python3.6
  environment:
    bucket_name: ${self:custom.vars.bucket_name}
  iamRoleStatements:
    - Effect: "Allow"
      Action:
        - "s3:PutObject"
        - "s3:GetObject"
      Resource:
        - "arn:aws:s3:::${self:custom.vars.bucket_name}/*"
```

The service name, provider, and runtime are set as usual. An environment variable is also added to pass the name of the bucket where the files will be stored.

SF also allows configuring the IAM that's created during deployment. The IAM statement allows the application to read and write files into that specific bucket (GetObject and PutObject), which is required to upload and read the images the user submits.

The next step is to define our functions. The first function will be the end-user facing Flask application, located in the 'web' directory. The second function will be in the 'imageprocessor' directory. In the YML config file, the directories are specified with the 'module' attribute. The functions would end up defined like this:

**packaging/serverless.yml**
```yaml
...
functions:
  app:
    module: web
    handler: wsgi_handler.handler
    events:
      - http: ANY /
      - http: 'ANY {proxy+}'
  image_processor:
    module: imageprocessor
    handler: process.lambda_handler
    events:
      - existingS3:
          bucket: ${self:custom.vars.bucket_name}
          events:
            - s3:ObjectCreated:*
          rules:
            - prefix: uploaded.jpg
...
```

We also defined events for both functions. The web function will respond to standard HTTP requests, while the image processor function will respond to ObjectCreated S3 events. The 'existingS3' event is an event created by another SF plugin and as such, we need to install it:

```bash
> sls plugin install -n serverless-plugin-existing-s3
```

The plugin creates the trigger in an existing S3 bucket. It's possible to do something similar without a plugin, but with the only catch that it needs to create the bucket during deploy and remove it when undeploying. Since creating and deleting an S3 bucket can be a problem (e.g., data loss, bucket name taken, etc.), the existing-S3 plugin is really useful.

Also, 3 other plugins will be needed, which are listed in the YML file:

**packaging/serverless.yml**
```yaml
...
plugins:
  - serverless-python-requirements
  - serverless-wsgi
  - serverless-plugin-existing-s3
  - serverless-apigw-binary
...
```

We have used the first 2 plugins and just explained the 3rd one. The 4th plugin is required to configure API Gateway to accept binary requests and responses.

Configure the plugins in addition with the custom variable under the 'custom' section:

**packaging/serverless.yml**
```yaml
...
custom:
  wsgi:
    app: web/app.app
  pythonRequirements:
    dockerizePip: non-linux
  apigwBinary:
    types:
      - 'multipart/form-data'
  vars:
    bucket_name: serverless-perftests
...
```

API Gateway requires specifying which MIME types will be treated as binary and which ones as text (default). The plugin obviously needs the same information to send to APIG and we need to specify the MIME type (multipart/form-data) our form will be submitting.

The last configuration needed to complete our setup is to tell SF to package our functions individually. The 'serverless-python-requirements' plugin loads the libraries from a requirements.txt file located at the root of our project. By packaging the functions individually, it will look for a requirements.txt file located in each of the functions' folders.

**packaging/serverless.yml**
```yaml
...
package:
  individually: true
  exclude:
    - node_modules/**
    - web/env/**
    - imageprocessor/env/**
...
```

Also, we can exclude or include other files we consider appropriate to fine-tune our deployments.

Once everything is set up, we can deploy our functions by executing `sls deploy`. Because the existing-S3 plugin is being used, there's an extra step in this case to attach the Lambda function to the S3 bucket. Run `sls s3deploy` as well.

```bash
> sls deploy
> sls s3deploy
```

## Wrap-Up

As you can see, the Serverless Framework offers a lot of options. The plugins and configurations can quickly add up and become longer and longer.

While developing these examples, a bug popped up and was reported to the WSGI plugin GitHub. Impressively, it was fixed in just 4 days. On the other hand, something as simple as a minor indentation issue can become a headache while developing with SF.

Overall, SF is incredibly configurable and fast. It's suitable for small and large projects and has a very large and active community behind it. You can expect to have some issues while learning because of the big number of configurations that are required to build a simple project, but it's a safe bet to start any new project.

---

[← Previous: Chapter 6 - Deployment Tools I: Zappa](06-deployment-tools-zappa.md) | [Next: Chapter 8 - Chalice →](08-chalice.md)