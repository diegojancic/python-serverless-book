docker build . -t django_ch3

docker run -p 8000:8000 django_ch3

docker run -it -p 8000:8000 django_ch3 "sh"