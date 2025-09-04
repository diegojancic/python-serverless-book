# Chapter 3: Environments

It wasn't evident in our to-do application, but we did something wrong from the beginning. What if in 6 months we want to start a new project and install the latest version of Django? We have installed a specific version of Python, a specific version of Django, a specific version of SimpleJSON, and we could have continued. However, by default Python doesn't support running multiple versions of the same library side-by-side.

Some technologies support this out-of-the-box; you can install different versions of a tool and run one or the other depending on what you want. With Python libraries, however, once you install a new version, it replaces the older one. That's perfectly fine as long as there are no changes in the APIs and our applications continue to work, but that's usually the exception, not the rule.

All that would be a nightmare, if it wasn't because they figured this out years ago already. In this chapter we'll talk about those different solutions. Our goal in this chapter is to explore the options we have, not only to isolate different projects, but also develop on a platform similar to the one we are going to use later in production.

We are going to examine 2 different ways to isolate our project; however, they are not mutually exclusive. At the end of the book, the complete stack will require us to use both at the same time, one on top of the other.

## Virtual Environment (virtualenv)

*Virtualenv* is a tool released in 2007 and the one that most Python web developers use. There are others, such as *conda* or even *venv* which is included in versions 3.3+ of Python. While it's perfectly fine to use the other ones, given we pick the right context to use them, *virtualenv* offers a slight advantage while I'm writing this that the others do not: it works with Zappa, a tool that we are going to introduce in Chapter 6.

What *virtualenv* does can be explained in a single line: Python and all the dependencies we need are copied into a sub-folder of our project.

Since we have all the libraries and dependencies installed in a sub-folder of our project, it's possible to run multiple versions of the same library side-by-side, and update the libraries to newer versions without breaking the code of all our other projects. There's also another problem it solves, and it's a permissions issue. If you deploy your application on a shared host, you probably won't be able to install libraries system-wide. Because the libraries are placed in a folder we have access to, we do not require root or Administrator permissions to install them.

PIP can help us install virtualenv:

```bash
pip install virtualenv
```

This is the only tool we'll install system-wide. Once we have installed it, we can start using it and create our environments. If we go back to our project, we can run:

```bash
virtualenv env
```

where '*env*' is the folder where all our dependencies will be copied or installed. We usually put just *env* or the name of the folder to create it in the same directory, but you can enter a full path to specify where the files will be placed. Run the command above to copy Python, pip, and other tools inside our new environment. That way we will always use the same version. Moreover, because both commands *python* and *pip* always look for files in the same directory first, anything we execute with those files will make changes inside our environment and not in the system.

After the environment was created, what we have to do is activate it. Activate means that the system PATH variable is changed and all our calls to any of the Python tools will execute inside our environment first.

Because we have installed Django and SimpleJSON in the last chapter, we are going to uninstall them to have them installed back inside our environment. Even though this is not necessary, it's good to do some cleanup before we go on. To uninstall, run:

```bash
pip uninstall django simplejson
```

We are uninstalling multiple packages at once there. Now, we have to reinstall them in our environment. To do so, we need to activate our environment. In Windows, we run the following in the same folder where our *env* folder is:

```bash
env\Scripts\activate.bat
```

In Linux, instead:

```bash
source env/bin/activate
```

All our commands need to be executed with the environment activated. Not just the *pip* commands, but all the Django commands as well. To reinstall the packages, this time in our environment, we execute the same command we did initially:

```bash
pip install django simplejson
```

We learned first about the basics of Python and Django and then about the virtual environments; that's why we had to uninstall and then re-install some of the packages. Usually, if you are starting from scratch, this is what you would do:

1. Install Python and PIP
2. Install virtualenv:
   ```bash
   pip install virtualenv
   ```
3. Create the virtualenv:
   ```bash
   virtualenv env
   ```
4. Activate the environment:
   ```bash
   source env/bin/activate    # Linux
   env\Scripts\activate.bat   # Windows
   ```
5. Install Django:
   ```bash
   pip install django
   ```
6. Create the Django project:
   ```bash
   django-admin startproject <name> .
   ```

We added a dot at the end when we created the Django project to have everything in the same directory where the environment folder is. Then of course you will need to run the migrations to update the database, create your own app, and so on.

When we are done working with the environment, the 'deactivate' command will take our command prompt back to normal.

## Docker

Unlike the other tools or libraries we learned so far, Docker is not specific to Python. It's an application that's being used in many different places and it's becoming a standard for various use cases. Companies like Microsoft, Google, Red Hat, and Cisco among others have contributed to the source code of Docker. As a result, you can find all different kinds of tools and services that provide support for this.

Docker provides a virtual separation of CPU, memory, permissions, tools, and networking between the different applications you run on the same server. It's similar, in a sense, to a virtual machine. It provides complete separation of what's run in each of those 'machines', but without having to run another OS and all the overhead it comes with. Each of those isolated environments we run is called a container.

For example, we can set up a Linux host with multiple containers: one containing a MySQL database server, another one containing a Redis cache server, and a third one containing our web server. This way we make sure each of those containers are isolated and, if an attacker is able to gain control of the container (e.g., usually the web server), the risk in other containers is reduced. Also, we can control how much CPU or memory each container can use and what ports are exposed outside of the container.

The main advantage of using a container service (there are others besides Docker) is that it contains our application's environment fully configured. If we work in a team, other developers will be able to get started very quickly without having to set up a lot of different tools and libraries. Also, because it's a very thin layer on top of the OS, we can deploy our Docker directly to production, and we are sure it will work fine. The ease of development and the quick deployment options in production make Docker a great tool to build our applications on.

We are going to do a parenthesis here. Because Docker is built on top of some Linux kernel features, it doesn't work natively on Windows. However, it's not only possible but also very easy to make it work on Windows, simply by running a virtual machine on it. Certain versions of Windows support Hyper-V, a virtualization service that Docker uses to install its host Linux image. Windows versions that do not support Hyper-V can run Docker using VirtualBox. With that in mind, we can completely run our virtualized Linux on Windows. In those cases, we would end up with our application running on Docker, Docker running on Linux, and Linux running on Windows. The Linux virtualization is the one that's going to add more overhead, and we wouldn't recommend that in production.

Back to our Linux machine, either virtualized or not, we have our containers working and taking care of the execution of our applications. Docker also allows us to deploy multiple containers to different real servers, which means we can decide whether to host our application on one or multiple servers.

Besides the "having an isolated environment" argument, there are 2 other reasons why we are going to use Docker here. The first one is to be able to replicate the AWS Lambda environment as closely as possible and to be able to test and run our application before deploying it. The second argument is vendor lock-in; it's extremely important for us to think about the future of our application and we don't want to be locked in with Amazon AWS forever. AWS is a great service and the biggest cloud provider in the world, so it's hard to think it's going to disappear in the short term but, nevertheless, we need to have a plan 'B' and be able to publish our application in another environment if for whatever reason we decide to stop using AWS Lambda.

### Docker Terminology

There are some terms, tools, and concepts we need to define before we can start using it:

**Host**: The actual server running Docker. Either your development machine running any OS, or the server where we upload our application. The host not only controls what we run, but it also controls how the different parts of our system connect together and the resources they use.

**Image**: An image is a snapshot of our server in a specific state. Images are built on top of other images. For example, there's an image called *ubuntu* that contains an Ubuntu Linux distribution, where we can install the Apache web server and create another image called 'apache' and create another instance on top of that one that contains our application's code. Images are read-only once they are created.

**Container**: It's an isolated environment that has access to its own resources, including files, memory, and network. There's no communication between the container and the outside world, unless specifically specified. Containers can be basically running or stopped. When a container is created from an image, a read-write file system is added on top of the read-only file system of the image. That means the containers keep their state between restarts.

**Registry**: An online service hosting images. Because images bundle together all the files and configurations, having our image uploaded to a registry is very useful to deploy our application. We just need to run a few commands and the image, exactly as we tested it locally, will be run on the servers.

**Repository**: Think of it as a catalog for one type of our images. The repository name can be prefixed with a namespace. So, for example, we can create a repository called *acme/todo*, where *acme* is our company's name and namespace and *todo* is the name of our image.

**Tag**: Each version of our images can be tagged. If we build the same image, with the same name (same *repository*), we can add a tag to each of those versions. For example, if we check Docker's official repository for Ubuntu images, we will find tags for versions 17.04, 16.04, and so on. The tags are specified with a colon (:) after the image name; for Ubuntu, we would have the images *ubuntu:17.04* and *ubuntu:16.04*. There's also a special tag *:latest* that is used by default if we don't specify one.

**Docker**: Here we are talking about the *docker* command, not about the Docker product. We will be using the docker command in a terminal to manage our images and containers.

**Docker Compose**: Docker itself has several tools and Compose is one of them. It lets us define multiple containers and link them together. This way we can manage our entire stack together. The terminal command we will be using is called *docker-compose*.

**Docker Machine, Swarm & More**: There are other very powerful tools provided in the package. With Docker Machine we can run multiple virtual machines (or nodes), with Swarm we can create a cluster of containers. We won't be using these here as we will be deploying serverless.

### Docker: Run!

Now that we have defined the basic terminology, let's jump in and create our first container:

```
> docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
5b0f327be733: Pull complete
Digest: sha256:07d5f7800dfe37b8c2196c7b1c524c33808ce2e0f74e7aa00e603295ca9a0972
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
...
```

What we did here with this simple command is indeed very complex. The docker run command is used to start a new container. hello-world refers to the image we are using. Once executed, Docker looked for the image on our local machine, but it couldn't find it. You can see that it actually looked for an image named hello-world and tagged latest (hello-world:latest). Because it's the first time we try to execute that image, it pulled it from an online repository and then it used it to create and run a container. The "Hello from Docker!" message is coming actually from the execution of the container.

That's not a very useful image really other than for testing Docker works. Let's try with something more useful. Ever installed Redis? Let's do it the Docker way.

```
> docker run -p 6379:6379 --name redis-server -d redis
Unable to find image 'redis:latest' locally
latest: Pulling from library/redis
d13d02fa248d: Pull complete
039f8341839e: Pull complete
21b9cdda7eb9: Pull complete
c3eba3e5fbc2: Pull complete
7778a0753f87: Pull complete
b052cf77de81: Pull complete
Digest: sha256:cd277716dbff2c0211c8366687d275d2b53112fecbf9d6c86e9853edb0900956
Status: Downloaded newer image for redis:latest
04217ee6babc9acbd695ce720dc1615ff6f37e3f6c6d34f5c7239779f4bfe74b
```

Redis is a popular in-memory database that's used for caching. We'll explain what happened there in a minute but, before, let's connect to it to see how it works.

First, install Python's Redis library. If you are not in a virtual environment, remember to either add sudo (for Linux/Mac) or run the cmd as Administrator:

```bash
pip install redis
```

With Redis installed, we can run a Python command line (i.e., run python) and test it by issuing a few commands. You can also create a .py file and execute the file.

```python
> python
(content removed for readability)
>>> import redis
>>> r = redis.StrictRedis()
>>> r.ping()
True
>>> r.set("my-key", "Hello Redis!")
True
>>> r.get("my-key")
b'Hello Redis!'
```

One common question people, including myself, ask when learning a new technology is '*how did he know the library/method/class was called like that?*'. Indeed, there's no need to memorize all the class and function names. In this case we can follow the documentation in the Python Redis package site.

In the Python command line, we imported the 'redis' package and then created a client by calling redis.StrictRedis(). Then the functions are called using the same names as the Redis commands. The full list of commands is in the Redis website. We can ping the server, set and get variables as in any key-value store, use counters, lists, and more.

Going back to our Docker container, our command had some interesting parameters:

```bash
docker run -p 6379:6379 --name redis-server -d redis
```

The `-p` parameter is used to map ports between the host and the container. First the host port, then the container port. If we have a web server running on port 80 in a container, we can map to the host's port 8080 simply by entering `-p 8080:80`.

The `--name` parameter is just for what it says: give the container a name. Containers can be identified in 3 different ways: a long 64-character UUID, a shorter 12-character version of the same UUID, or a name. Docker assigns a random name if we don't specify one; while it's fine for some cases, giving our container a name allows us to link it from other containers and to stop the container without having to look for what name it was given.

Finally, the `-d` flag tells Docker to run our container in detached mode. That means we can continue using our terminal while the container is being executed. Containers stop when the command running in the container stops, which in some cases can never happen.

The command executed was somewhat more complex than our initial hello-world for another reason: it printed several times "*<random text>: Pull complete*". The reason for that is Docker images are built on top of other images. When an image is created, it is built upon an existing image, and when an image is downloaded, all the images in the hierarchy are also downloaded. Because different images share some of the underlying images, Docker will not download the same file twice, avoiding duplication and saving space. Docker supports up to 127 layers of images, something that will be relevant very soon when we create our own image.

Because our container is still running, we can now stop it by using the name we gave to it:

```bash
docker stop redis-server
```

If we don't know what's the name of our container, we can execute `docker ps` to see the list of the running containers.

### Dockerfiles

Plain, standard images are good for certain things, but certainly not for running a web application or custom code. Docker provides a way to customize these images by creating a file called *Dockerfile*. The file, with no extension, is the one that Docker is going to look for by default.

All images are created from a Dockerfile, even the ones that we downloaded when we executed our Hello World or our Redis instance. However, the file is used only for building the image; once it was built and packaged, the Dockerfile is no longer necessary.

A simple Dockerfile can look like this:

**Dockerfile1**
```dockerfile
FROM alpine
CMD ["sh"]
```

The number after the name is because we will be creating several Dockerfiles for different examples. For a simple web application, you would usually need a single file and, if so, it would be recommended to use the default name for it: Dockerfile.

Dockerfiles are a simple list of commands that are executed in order to build the image. `FROM <something>` is how the files will always start. The FROM command just tells Docker what is the starting point to build our image. There are several images we can start from: there are images for complete OS such as Ubuntu, Debian, or CentOS; images for pre-configured servers such as Redis, MongoDB, MySQL, or even WordPress; and images with pre-configured environments, such as Python, NodeJS, or Ruby. In the example above we used Alpine because it's a popular distribution of Linux that takes only very little space (~5MB).

The CMD command is used to tell the container what to execute when it starts. The command receives a list of arguments that tells Docker not only what program to execute, but also what parameters to pass to the executable, for example:

```dockerfile
CMD ["/path/to/file", "--param1", "--param2"]
```

Now, let's build our image:

```bash
docker build -t simple-image -f Dockerfile1 .
```

The format of the command is: `docker build [OPTIONS] PATH`. Note the dot at the end of the command we used to build the image; that's the PATH. The `-t` parameter is used to tag (or give a name to) the image, in the format namespace/name:tag, where the namespace is optional and the tag defaults to :latest if omitted. The `-f` parameter is used to specify the file name used to build the image; we would normally just call the file Dockerfile and omit this parameter.

Once the image is built, we can run a container based on that image:

```bash
docker run -it simple-image
```

simple-image is the name of the image used to start the container, as we tagged it during the build. The `-it` flags are to make the execution interactive or, in other words, to be able to use the terminal executed in the container.

Let's go a step further and run our 'todo' application in a container. This time we are going to base our image on python:3.6-alpine. That image is based on Alpine Linux and has Python 3.6 installed already, so it will be smaller than other Linux distributions and easy to set up at the same time. That image is suitable for production usage, but there are others that can be used as well for both development and production. In the Docker Hub page, there's a list of repositories and, inside the Python repository, a list of the images that have Python pre-installed, including different versions of both Python and Alpine, and others based on different distributions of Linux.

Our new Dockerfile will look like this:

**Dockerfile**
```dockerfile
FROM python:3.6-alpine

COPY requirements.txt /
EXPOSE 80

RUN pip install virtualenv \
    && virtualenv /var/venv \
    && source /var/venv/bin/activate \
    && pip install -r requirements.txt

RUN mkdir /code/
WORKDIR /code/
COPY . /code/

CMD ["/var/venv/bin/python", "/code/manage.py", "runserver", "0.0.0.0:80"]
```

Before we explain what it does, let's build an image using it and break the output into each step to understand what it does. Build the image:

```bash
docker build -t todo-app .
```

The output should look something like this:

```
Sending build context to Docker daemon  120.3kB
Step 1/8 : FROM python:3.6-alpine
---> 83da41380580
```

First, we see it's step 1 out of 8. Each of our commands in the Dockerfile is a step and its output will be a new, intermediary, image.

```
Step 2/8 : COPY requirements.txt /
---> 7d00749d61b4
```

The COPY command is used to copy files from the host to the container. Because the host and the container do not share the same file system, it's necessary to copy our files to the container to run the application. There we are copying the requirements.txt file from the host to the root directory in the container.

You might have noticed that we are copying the files in two parts: the requirements.txt first and then all the other files. The reason for this has to do with optimizing the build speed and reducing the amount of intermediary images. Because any changes in the files will make Docker discard the intermediary images and build them again, we want to avoid installing all the Python libraries as much as possible. That's why the requirements file is copied first, then the dependencies are installed, and then all the other files are copied. If an image or an HTML file is changed, the dependencies will not be installed again as Docker will use the existing intermediary image from the cache.

```
Step 3/8 : EXPOSE 80
---> 54556a2baab6
```

The EXPOSE command is used to publish a port to other containers. The image doesn't decide what ports are available from the host as that would be too many permissions for the container. When we expose a port we make it available for other containers and—when used in conjunction with the `-p` parameter in the run command—to the host.

```
Step 4/8 : RUN pip install virtualenv && virtualenv /var/venv && source /var/venv/bin/activate && pip install -r requirements.txt
...
```

The RUN command is used to do exactly that: run a command. Because each instruction in our Dockerfile creates a new layer and there's a limit on the number of layers an image can have, it's common to execute multiple commands in the same line, joined together with &&.

Because Python and PIP are already installed in the base image, we can use PIP to install virtualenv (`pip install virtualenv`). Then, create (`virtualenv /var/venv`) and activate the environment (`source /var/venv/bin/activate`) as we did at the beginning of this chapter, and lastly install all the requirements in our environment (`pip install -r requirements.txt`).

Is it redundant to use a virtual environment inside an already isolated container? Might be. In many cases it would not be necessary to create a virtualenv, but one of the reasons we do this is because one of the tools we use later in chapter 6, Zappa, requires a virtual environment in place.

```
Step 5/8 : RUN mkdir /code/
...
Step 6/8 : WORKDIR /code/
...
Step 7/8 : COPY . /code/
...
```

Once we have installed all the dependencies, we create a new folder, set the working directory (so all future commands will execute in that directory by default), and copy all the project files from the host to the container.

```
Step 8/8 : CMD /var/venv/bin/python /code/manage.py runserver 0.0.0.0:80
...
```

Our last step is to set up the CMD. The executable will be the python file located in our virtual environment, that way we don't have to activate it explicitly. Then start the server as we did in chapter 2, but this time we are also specifying the network interface where to listen. Because the embedded web server that Django provides only accepts requests from the same computer, it is necessary to make it respond to requests from any network.

To test our web application, we can now run the container. Remember the need to explicitly make the ports public, as the EXPOSE command we used in our Dockerfile will only make it available to other containers.

```bash
docker run -p 8000:80 --name webapp todo-app
```

Now, launch a web browser and access http://localhost:8000/ to view the app working.

Please note that the Django web server is not suitable for production usage, as "*It has not gone through security audits or performance tests.*" In production you should use something like uWSGI and NGINX, or any other production-ready web server. For production usage, check Appendix A for full configuration files.

### Developing in Docker

If for some reason something is not working or you want to inspect what's going on in the server, you can launch a shell at any time just by appending "*sh*" at the end of the run command we just executed.

Another useful trick is to map our project (or any other) directory in the container. This allows the container to read and modify files that are on the host computer. This has 2 main benefits:

1. Project files can be changed during development without having to re-build the Docker image, which is time-consuming, allowing faster development.
2. It's possible to move generated files to the host. For example, if you want to do a pip freeze to save the list of dependencies, or execute Django's *makemigrations* command, you can do it with a shell in the container and see the files on the host automatically.

To do so, we need to run the container adding the `-v` parameter. For instance:

```bash
docker run -v /home/user:/code web-server
```

That tells Docker to map the directory /home/user from our host to the directory /code in the container.

### Compose

The last of our Docker tools we are going to use is Docker Compose. With Compose we can define, link, and manage multiple containers at the same time. It allows us to orchestrate the different servers we need to run.

Docker Compose configurations are stored in a YAML file; a file we usually call docker-compose.yml as it's the default name Docker uses.

**docker-compose.yml**
```yaml
version: '3'

services:
  database:
    image: postgres
  
  web:
    build: .
    volumes:
      - .:/code
    ports:
      - "80:80"
    depends_on:
      - database
```

Here we are using two servers: "*database*" and "*web*". The database server is very simple; we are just going to use the postgres image, which contains a PostgreSQL database server. That's going to be an upgrade from our current SQLite database.

Each of the items under the *services* root node in the file is a server, and we can specify more or less the same parameters we have been specifying in the docker run command. For the web, we are building the Dockerfile located in the current directory (i.e., that's what a single *dot* means), specifying a volume mapping, publishing ports, and setting the dependency between the different containers.

Now, we just need to start our containers, running in the same directory where our .yml file is:

```bash
docker-compose up
```

As a first step, that will build our images. In the case of our PostgreSQL image, it will download it from the Docker official registry.

That's going to work, but with the *detail* that it will still use our SQLite database file. Fortunately, we have mapped our current directory, so changing the connection settings won't require rebuilding the image.

Open settings.py in our application and change the connection information to something like this:

**website/settings.py**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'database',
        'PORT': 5432
    }
}
```

We set our connection options to PostgreSQL, in a host called *'database'* since that's the name of our database server (check the *docker-compose.yml* file). The port, name, and username are defaults. We could set a database password. However, since this is just for development, we are fine. In a production environment, a database with password, backups, and configured better will be used. After all, if the container is stopped, we would lose all our data if configured as we have it now.

Try to run it now again, run `docker-compose up`, and... Oops! It doesn't work. Let's investigate why.

One way to investigate problems in one container is to execute a shell and try to run the command ourselves. The container should still be running, but we can check that by running the `docker ps` command. We can also add the `-a` flag to list all the containers, including those that have been stopped.

```
> docker ps
CONTAINER_ID  IMAGE             ...  NAMES
xxxxxxxxxx    5compose_web      ...  5compose_web_1
xxxxxxxxxx    postgres          ...  5compose_database_1
```

In the last column, the names of the containers are displayed. With those, we can run a command in the same container as follows (if the container is running):

```bash
docker exec -it -p 80:80 -v .:/code/ 5compose_web_1 sh
```

The exec command's format is similar to the run command: `[OPTIONS] container_name [COMMAND]`. As before, we are using `-it` to have interactive access, `-p` to map the ports, and `-v` to map the volume from the host to the container. If the container is stopped, we need to use the run command instead, but paying attention that in this case it will ask for the image name, not the container's name. The name of the image is listed in the docker ps command that we just executed. Alternatively, run `docker images` to have a full list of the images on the local machine.

Once in the container's shell, we try to launch our web server using the same command that's set in the Dockerfile:

```
> /var/venv/bin/python manage.py runserver 0.0.0.0:80
...
Error: ModuleNotFoundError: No module named 'psycopg2'
...
```

Django will complain with a long, hard to see, message. Among those lines, the missing module message will be displayed.

*A note on daily development workflow*: we are doing things a little bit more complicated than what it really is here, because we are doing it backwards really. Instead of launching a container, waiting for it to fail, and then seeing how we fix it, it's easier to launch a shell and the web server right there. If something fails, for example because a module is missing, we just do a *pip install* followed by a *pip freeze* as we have done before to have our requirements.txt file updated. Of course, we need to make sure to map our drive from the host to the container. That way all our changes are kept between restarts.

To fix the missing dependency error, we need to add *psycopg2* to our requirements.txt file. Unfortunately, that will not be enough though. Installing that module requires having the compiler, Postgres binaries, the Python dev libraries, and a compiler. In our Dockerfile, before the RUN command that installs all the Python dependencies, we have to add another RUN command that installs those dependencies:

```dockerfile
RUN apk add --no-cache python-dev gcc musl-dev postgresql-dev
```

APK is the Linux package manager used here because it's the only one available in the Alpine distribution. The last names after the no-cache flag are the packages we are required to install the Postgres library (*psycopg2*), and many other libraries that require compilation from the source. Because some libraries can be hard to install as they have many dependencies, an easier alternative is to start our image FROM python:3 instead of using the current Alpine image. That depends on how much effort we want to put in and how we want our final image to look like.

Rebuild the image and run our container again (`docker-compose build && docker-compose up`). This time the web server will start, but we are going to have another error. Now, our Django application is telling us that there's a database error, that the table was not found in our PostgreSQL database. Makes sense; we've never run our database migration script!

Instead of launching the web server directly, we need a start script where we can: a) test the database server is up and running, b) run the migration scripts, and, finally, c) start the web server.

Then, let's change our Dockerfile CMD line at the end to this:

```dockerfile
CMD ["sh", "docker-entrypoint.sh"]
```

And create the following files:

**docker-entrypoint.sh**
```bash
#!/bin/sh

/var/venv/bin/python test-db-connection.py
echo "Apply database migrations"
/var/venv/bin/python manage.py migrate
echo "Starting server"
/var/venv/bin/python manage.py runserver 0.0.0.0:80
```

**test-db-connection.py**
```python
import psycopg2
import time

connected = False
while not connected:
    try:
        conn = psycopg2.connect("host=database dbname=postgres user=postgres")
        conn.close()
        print("Connection to Postgres succeed!")
        connected = True
    except psycopg2.OperationalError:
        print("Unable to connect to Postgres. Retrying...")
        time.sleep(1)
```

With the shell file we are performing the 3 steps we mentioned above. When the *test-db-connection.py* file is called, it will attempt to connect to the database until it succeeds, then exit to continue the execution of the *.sh* file.

Now, if we build our containers (i.e., `docker-compose build`) and run them, we should see the application running. This time, using PostgreSQL to store the data.

## Wrap-up

There were a lot of new things here. Using virtualenv is pretty straightforward: we create an environment, activate it, and install everything there. It allows us to keep all the information we need to run our project in the same folder and it also solves a few permission issues along the way.

Docker is a completely different story. It's harder to install, uses more memory, and it's harder to set up. However, if you were able to follow the examples in the chapter, you probably have discovered its beauty. With Docker we are not just packaging the list of dependencies; we are packaging everything we need to run our application. The OS, its tools, our code, and, if we use Docker Compose, we can even include the additional services our app needs to run.

It's fair to wonder, however, what does it have to do with *serverless*. Our development process will require using these tools, not only because of the benefits we have already discovered, but also because other tools we will use in the next chapters will depend on them. For example, to publish our site to a serverless environment, we are going to package everything in our virtual environment and upload it directly to the cloud!

Our next step is to get used to the Amazon Web Services ecosystem. We'll explore the different services it provides before we can move on to the serverless-specific services.

---

[← Previous: Chapter 2 - Web Development Essentials](02-web-development-essentials.md) | [Next: Chapter 4 - AWS Ecosystem →](04-aws-ecosystem.md)