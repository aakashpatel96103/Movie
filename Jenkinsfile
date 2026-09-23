pipeline {
    agent any

    tools {
        jdk 'JDK21'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/Movie-Theater-Booking.git'

                echo 'Source code checked out successfully.'
            }
        }

        stage('Environment') {
            steps {
                bat 'java -version'
                bat 'python --version'
                bat 'docker --version'
                bat 'docker-compose --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker-compose build'
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker-compose down --remove-orphans'
                bat 'docker-compose up -d'
            }
        }

        stage('Final Status') {
            steps {
                bat 'docker-compose ps'
                echo 'CI/CD Pipeline Completed Successfully.'
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful.'
        }

        failure {
            echo 'Pipeline Failed. Check Console Output.'
        }
    }
}
