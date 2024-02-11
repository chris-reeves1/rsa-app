pipeline {
    agent any
    stages {
        stage("init"){
            steps{
                sh 'ls -lah frontend'
                sh 'ls -lah backend'
                sh 'docker rm $(docker ps -aq) || true'
                sh 'docker build -t frontend ./frontend'
                sh 'docker build -t backend ./backend'

                sh 'docker network create new' 

                sh 'docker run -d --network new --name backend backend'
                sh 'docker run -d -p 80:80 --network new --name frontend frontend'
            }
        }
    }
}