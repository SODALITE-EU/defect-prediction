pipeline {
  options { disableConcurrentBuilds() }
  agent { label 'docker-slave' }
  stages {
    stage ('Pull repo code from github') {
      steps {
        checkout scm
      }
    }
    stage ('Build semantic-reasoner') {
      when { 
          not { 
                triggeredBy 'UpstreamCause' 
          }
      }
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
	
	stage('Build docker images') {
            steps {
                sh "cd tosca; docker build -t toscasmells  -f Dockerfile ."
                sh "cd ansible; docker build -t ansiblesmells -f Dockerfile ."
            }
    }
   
    stage('Push Dockerfile to DockerHub') {
            when {
               branch "master"
            }
            steps {
                withDockerRegistry(credentialsId: 'jenkins-sodalite.docker_token', url: '') {
                    sh  """#!/bin/bash                       
                            docker tag toscasmells sodaliteh2020/toscasmells:${BUILD_NUMBER}
                            docker tag toscasmells sodaliteh2020/toscasmells
                            docker push sodaliteh2020/toscasmells:${BUILD_NUMBER}
                            docker push sodaliteh2020/toscasmells
                            docker tag ansiblesmells sodaliteh2020/ansiblesmells:${BUILD_NUMBER}
                            docker tag ansiblesmells sodaliteh2020/ansiblesmells
                            docker push sodaliteh2020/ansiblesmells:${BUILD_NUMBER}
                            docker push sodaliteh2020/ansiblesmells
                        """
                }
            }
    }
  }
  post {
    failure {
        slackSend (channel: '@Indika (JADS)', color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
    }
    fixed {
        slackSend (channel: '@Indika (JADS)', color: '#6d3be3', message: "FIXED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})") 
    }
  }
}
