pipeline {
  agent { label 'docker-slave' }
  stages {
    stage ('Pull repo code from github') {
      steps {
        checkout scm
      }
    }
    stage ('Build semantic-reasoner') {
      steps {
        build 'semantic-reasoner/master'
      }
    }
    stage ('Run Ansible Smells Tests') {
      steps {
        sh  """ #!/bin/bash
                cd ansible
                python3 -m unittest tests/Test*.py
            """
      }
    }
    stage ('Build defect-prediction') {
      steps {
        sh  """ #!/bin/bash
                cd tosca
                mvn clean install
            """
        archiveArtifacts artifacts: '**/*.war, **/*.jar', onlyIfSuccessful: true
      }
    }
  }
  post {
    failure {
        slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
    }
    fixed {
        slackSend (color: '#6d3be3', message: "FIXED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})") 
    }
  }
}
