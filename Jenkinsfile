pipeline {
    agent any

    environment {
        IMAGE_NAME = "weather-app"
        CONTAINER_NAME = "weather-container"
    }

    stages {
        stage('Clone Code') {
            steps {
                git credentialsId: 'github-token', url: 'https://github.com/harsh2508pandey/Whether_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                    docker rm -f $CONTAINER_NAME || true
                    docker run -d -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME
                '''
            }
        }
    }
}


