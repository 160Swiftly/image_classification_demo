#Get base image from dockerhub
FROM python:3.10-slim

#Install updates and get git
RUN apt-get update && apt-get install -y git

#Select working directory
WORKDIR /app 

#Copy all file into working directory
COPY . /app

#Install dependencies 
RUN pip install -r requirements.txt 

#Expose desired port
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]