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
                sh 'javac Main.java' // Compile your Java files
            }
        }
        stage('Test') {
            steps {
                sh 'java Main' // Or run JUnit, etc.
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deployment step (can be SSH, Docker, etc)'
            }
        }
    }
}
