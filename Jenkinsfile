pipeline {
  options { 
	  disableConcurrentBuilds() 
	  buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '30', daysToKeepStr: '', numToKeepStr: '')
  }
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
    stage('Test ansible-defect') {
        steps {
            sh  """ #!/bin/bash
			        cd ansible
                    python3 -mvenv .venv
					. .venv/bin/activate
					python3 -m pip install --upgrade pip
					python3 -m pip install -r requirements.txt                     				
                    python3 -m pytest --pyargs -s ./tests --junitxml="results.xml" --cov=ansiblelints --cov-report xml tests/
					cp *.xml $WORKSPACE
                """
            junit 'results.xml'
        }
    }
	stage('Test ansible-misconfiguration') {
        steps {
            sh  """ #!/bin/bash
			        cd ansible
                    python3 -mvenv .venv
					. .venv/bin/activate
					python3 -m pip install --upgrade pip
					python3 -m pip install -r requirements.txt  
					python3 -m pip install -U pip setuptools wheel --user
					python3 -m spacy download en_core_web_sm					                   				
                    python3 -m pytest --pyargs -s ./tests --junitxml="results2.xml" --cov=ansiblelints --cov-report xml tests/
					cp *.xml $WORKSPACE
                """
            junit 'results2.xml'
        }
    }
    stage ('Build defect-prediction') {
      steps {
        sh  """ #!/bin/bash
                cd tosca
                mvn  clean install -Ddefault.min.distinct.threshold=104857600
            """
      }
    }
    stage('SonarQube analysis TOSCA'){
        environment {
          scannerHome = tool 'SonarQubeScanner'
        }
        steps {
            withSonarQubeEnv('SonarCloud') {
                sh  """ #!/bin/bash
                        cd "tosca"
                        ${scannerHome}/bin/sonar-scanner
                    """
            }
        }
    }
    stage('SonarQube analysis Ansible'){
        environment {
          scannerHome = tool 'SonarQubeScanner'
        }
        steps {
            withSonarQubeEnv('SonarCloud') {
                sh  """ #!/bin/bash
                        cd "ansible"
                        ${scannerHome}/bin/sonar-scanner
                    """
            }
        }
    }
   stage('SonarQube analysis AnsibleMisconfig'){
        environment {
          scannerHome = tool 'SonarQubeScanner'
        }
        steps {
            withSonarQubeEnv('SonarCloud') {
                sh  """ #!/bin/bash
                        cd "ansible-misconfig"
                        ${scannerHome}/bin/sonar-scanner
                    """
            }
        }
    }
   stage('Build docker images') {
   	        when {
				allOf {
				// Triggered on every tag
					expression{tag "*"}
				   }
            } 
            steps {
                sh "cd tosca; docker build -t toscasmells  -f Dockerfile ."
                sh "cd ansible; docker build -t ansiblesmells -f Dockerfile ."
				sh "cd ansible-misconfig; docker build -t ansiblemisconfigs -f Dockerfile ."
            }
    }
   
    stage('Push Dockerfile to DockerHub') {
	        when {
				allOf {
				// Triggered on every tag
					expression{tag "*"}
				   }
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
							docker tag ansiblemisconfigs sodaliteh2020/ansiblemisconfigs:${BUILD_NUMBER}
                            docker tag ansiblemisconfigs sodaliteh2020/ansiblemisconfigs
                            docker push sodaliteh2020/ansiblemisconfigs:${BUILD_NUMBER}
                            docker push sodaliteh2020/ansiblemisconfigs
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
