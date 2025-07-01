pipeline {
    agent any

    environment {
        IMAGE_NAME = 'weatherapp-image'
        CONTAINER_NAME = 'weatherapp-container'
    }

    stages {

        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/harsh2508pandey/Whether_app.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Stop and remove any old container
                    sh '''
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true
                        docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo 'Deployment failed.'
        }
        success {
            echo 'Deployment succeeded!'
        }
    }
}
