pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/harsh2508pandey/Whether_app'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('whether_app')
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker stop whether_app || true'
                    sh 'docker rm whether_app || true'
                    sh 'docker run -d --name whether_app -p 5000:5000 whether_app'
                }
            }
        }
    }
}

