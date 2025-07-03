pipeline {
    agent any

    environment {
        IMAGE_NAME = "weather-app"
        CONTAINER_NAME = "weather-app-container"
        PORT = "5000"
    }

    stages {
        stage('Clone Code') {
            steps {
                git branch: 'main', 
                    credentialsId: 'github-token', 
                    url: 'https://github.com/harsh2508pandey/Whether_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    // Stop & remove existing container (if any)
                    sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                    """

                    // Run container
                    sh "docker run -d -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                }
            }
        }
    }

    post {
        failure {
            echo "Build failed. Check the logs."
        }
        success {
            echo "Build and deployment successful!"
        }
    }
}

