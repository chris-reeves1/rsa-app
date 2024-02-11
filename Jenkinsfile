pipeline {
    agent any
    stages {
        stage("init"){
            steps{
                sh 'docker rm $(docker ps -aq) || true'
                sh 'docker build -t frontend /rss-app/frontend'
                sh 'docker build -t backend /rss-app/backend'

                sh 'docker network create new' 

                sh 'docker run -d --network new --name backend backend'
                sh 'docker run -d -p 80:80 --network new --name frontend frontend'
            }
        }
    }
}