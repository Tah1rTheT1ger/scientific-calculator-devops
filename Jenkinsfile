pipeline {
  agent any
  environment {
    IMAGE = "docker.io/tah1rthet1ger/scientific-calculator:${env.BUILD_NUMBER}"
    LATEST = "docker.io/tah1rthet1ger/scientific-calculator:latest"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Setup Python') {
      steps { sh 'python3 -m venv .venv && . .venv/bin/activate && pip install -U pip pytest' }
    }
    stage('Test') {
      steps { sh '. .venv/bin/activate && export PYTHONPATH=. && pytest -q' }
    }
    stage('Docker Build') {
      steps {
        sh 'docker build -t $IMAGE .'
        sh 'docker tag $IMAGE $LATEST'
      }
    }
    stage('Docker Push') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin docker.io'
          sh 'docker push $IMAGE'
          sh 'docker push $LATEST'
        }
      }
    }
  }
}
