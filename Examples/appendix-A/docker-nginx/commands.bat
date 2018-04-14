cd server
docker build -t aws-server .
docker run -d -p 8000:8000 --name aws-server aws-server

cd ..\proxy
docker build -t aws-proxy .
docker run -p 80:80 --link aws-server:server --name aws-proxy aws-proxy


aws ecr get-login --no-include-email --region us-east-1
REM Result of previous command, run it:
docker login -u AWS -p ..................... https://XXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com


docker tag aws-server:latest XXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/engineerica/testserver:latest
docker tag aws-proxy:latest XXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/engineerica/testproxy:latest


docker push XXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/engineerica/testserver:latest
docker push XXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/engineerica/testproxy:latest