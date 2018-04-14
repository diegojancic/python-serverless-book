FROM lambci/lambda:build-python3.6

# Copy in your requirements file
COPY requirements.txt /requirements.txt
    
    
# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
COPY . /code/

ENV PS1 'zappa@$(pwd | sed "s@^/var/task/\?@@")\$ '

ENV DJANGO_SETTINGS_MODULE=website.settings

RUN virtualenv /var/venv && \
    source /var/venv/bin/activate && \
    pip install -U pip zappa && \
    pip install -r /requirements.txt 
    
USER root

EXPOSE 8000

CMD source /var/venv/bin/activate && python manage.py runserver 0.0.0.0:8000

