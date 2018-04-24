
# Remove existent ZIP file and compress the function 
rm -f say_hi.zip && zip say_hi.zip say_hi.py

aws lambda update-function-code --function-name say_hi --zip-file fileb://say_hi.zip

