#Get base image from dockerhub
FROM python:3.10-slim

#Install updates and get git
RUN apt-get update && apt-get install -y git

#Get source files from repo
RUN git clone "https://github.com/160Swiftly/image_classification_demo.git" /app

#Select working directory
WORKDIR /app 

#Install dependencies 
RUN pip install -r requirements.txt 

#Expose desired port
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]