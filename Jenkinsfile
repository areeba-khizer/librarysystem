pipeline {
    agent any

    environment {
        APP_NAME = 'library-system'
        IMAGE_NAME = "library-management-system"
        DOCKER_USERNAME = "areebakhizer"
        TAG = "${env.GIT_COMMIT}"
        REMOTE_HOST = 'ubuntu@54.172.53.178'
    }

    stages {

        stage('Build Image') {
            steps {
                script {
                    def app = docker.build("${DOCKER_USERNAME}/${IMAGE_Name}:${TAG}")
                }
            }
        }

        stage('Push Image') {
            steps {
                script {
                    docker.withRegistry("https://index.docker.io/v1/", "0b2b6711-2eb7-4d9c-bfda-2992715c4582") {
                        def app = docker.image("${DOCKER_USERNAME}/${IMAGE_NAME}:${TAG}")
                        app.push()
                    }
                }
            }
        }
        stage('Reload docker compose') {
            steps {
                sshagent (credentials: ['6193a4d2-cd41-440a-a455-8e72bc500da4']) {
                    sh 'chmod +x ./deploy.sh && ./deploy.sh ${TAG}'
                }
            }
        }
    }

    post {
        success {
            echo 'Build completed successfully.'
        }
        failure {
            echo 'Build failed.'
        }
        always {
            echo 'Cleaning up...'
        }
    }
}

