pipeline {
    agent any

    stages {
        stage('Clone Code') {
            steps {
                git 'https://github.com/harsh2508pandey/Whether_app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("harsh3928/whether_app")
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh "docker run -d -p 5000:5000 --name whether_container harsh3928/whether_app"
            }
        }

        stage('Notify Success') {
            steps {
                echo 'Deployment successful. Visit: https://fancy-drinks-drum.loca.lt'
            }
        }
    }
}

