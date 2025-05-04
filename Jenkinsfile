pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/akhilp90/AkakikeAssignment.git'
            }
        }

        stage('Build') {
            steps {
                // Replace Unix 'sh' with Windows 'bat'
                bat 'echo Building project...'
                // Add actual build commands here (e.g., mvn clean install or whatever you use)
            }
        }

        stage('Test') {
            steps {
                bat 'echo Running tests...'
                // Add actual test commands here
            }
        }

        stage('Deploy') {
            steps {
                bat 'echo Deploying...'
                // Add deployment steps
            }
        }
    }
}
