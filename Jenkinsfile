pipeline {
    agent any

    stages {
        stage('Clone Code') {
            steps {
                git 'https://github.com/YOUR_USERNAME/YOUR_REPO.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("weather-app")
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh 'docker stop weather-app || true && docker rm weather-app || true'
                    sh 'docker run -d -p 5000:5000 --name weather-app weather-app'
                }
            }
        }
    }
}


