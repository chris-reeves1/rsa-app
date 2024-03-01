pipeline {
    agent any

    environment {
        // Removed database connection environment variables
        CUSTOM_NETWORK = 'my_app_network'
    }

    stages {
        stage('Setup Custom Network') {
            steps {
                script {
                    // Create a custom network for your app
                    sh "docker network create ${CUSTOM_NETWORK} || true"
                    sh 'docker rm -f $(docker ps -aq) || true' 
                }
            }
        }

        stage('Start MySQL') {
            steps {
                script {
                    // Pull MySQL image and run the container within the custom network
                    sh "docker run -d --name mysql --network ${CUSTOM_NETWORK} -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=mydatabase -e MYSQL_USER=admin -e MYSQL_PASSWORD=password mysql:5.7"
                    // Wait for MySQL to fully start. Implement a health check loop here if possible.
                    sh "sleep 30" // Adjust timing as necessary
                }
            }
        }

        stage('Build and Run Backend') {
            steps {
                script {
                    // Navigate to the backend directory
                    dir('backend') {
                        // Build the Docker image for the backend
                        sh 'docker build -t backend-app .'
                        // Run the backend container in the custom network
                        // Removed the DATABASE_URI environment variable since it's hardcoded in the app
                        sh "docker run -d --name backend --network ${CUSTOM_NETWORK} -p 5000:5000 backend-app"
                    }
                }
            }
        }

        stage('Build and Run Frontend') {
            steps {
                script {
                    // Navigate to the frontend directory
                    dir('frontend') {
                        // Build the Docker image for the frontend
                        sh 'docker build -t frontend-app .'
                        // Run the frontend container in the custom network
                        sh "docker run -d --name frontend --network ${CUSTOM_NETWORK} -p 80:80 frontend-app"
                    }
                }
            }
        }
    }
}
