## defect-prediction

This module predicts the smells, anti-patterns, and bugs in IaC (Ansible) and TOSCA. It also recommends the fixes. 

## Prerequisites
This module depends on the SODALITE sub-project “semantic-reasoner”. Thus, first built it

The information about building semantic reasoner can be found at
 ` https://github.com/SODALITE-EU/semantic-reasoner `

## Build Process 

Ansible Smell detection extends Ansible-Lint tool by adding custom detection rules. Thus, first need to install Ansible-Lint

pip install ansible-lint

To build and run Ansible Smells Tests:
 
Go to the directory “defect-prediction\ansible” (via cd command) and run

```
python -m unittest tests/Test*.py

```
This requires Python 3.X with unittest module.
 
To build TOSCA smell detection modules:

Go to directory “defect-prediction\tosca” and run

```
mvn clean install 

```
This requires maven 3.x 

## Deployment

The built artifact for TOSCA is a web application (.war file) that can be deployed in any Web server. 

The built artifact for Ansible is a Flask Web application.

## Docker Image Building and Usage: Ansible Smell Detector 
```
sudo docker build -t sodalite/ansiblesmells .
sudo docker run -p 5000:5000 -d --name=anssAPI sodalite/ansiblesmells
sudo docker start anssAPI
sudo docker logs anssAPI
sudo docker stop anssAPI
sudo docker rm  anssAPI
```

## Docker Image Building and Usage: TOSCA Smell Detector 
```
sudo docker build -t sodalite/toscasmells .
sudo docker run -p 8080:8080 -d --name=tossAPI sodalite/toscasmells
sudo docker start tossAPI
sudo docker logs tossAPI
sudo docker stop tossAPI
sudo docker rm  tossAPI
```
## Run Docker Compose

```
sudo docker-compose up
sudo docker image ls
```

## REST APIs

# TOSCA Smells

```
POST http://ip:8080/bug-predictor-api/v0.1/bugs/tosca/jsonv2
```
A sample request
```
{
	"aadmid": "z",
	"repository": "x", # optional
	"server" : "y" # optional
}
```

Or, Send the TOSCA file as multipart/form-data (name:” file”, value: actual file)

```
POST http://{serverIP}:8080/bug-predictor-api/v0.1/bugs/tosca/file
```


# Ansible Smells 
```
http://{serverIP}:5000/bugs/ansible/file
```
Send the Ansible file as multipart/form-data (name:” file”, value: actual file)

# Ansible Linguistic Anti-patterns

To retrain the deep learning models (optinal)

```
http://{serverIP}:5000/bugs/ansible/linguistic/train
```

To detect/predict linguistic anti-patterns, send the Ansible file as multipart/form-data (name:” file”, value: actual file)

```
http://{serverIP}:5000/bugs/ansible/linguistic/file
```
 
