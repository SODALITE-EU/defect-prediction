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

