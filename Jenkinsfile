pipeline {
    agent any

    environment {
        IMAGE_NAME = "rishivardan/employee-management-system"
        IMAGE_TAG = "v${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Files') {
            steps {
                sh '''
                    set -e
                    pwd
                    ls -la
                    test -f Dockerfile
                    test -f requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'No automated tests configured yet.'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -e
                    docker build -t "$IMAGE_NAME:$IMAGE_TAG" .
                    docker tag "$IMAGE_NAME:$IMAGE_TAG" "$IMAGE_NAME:latest"
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_PASSWORD'
                    )
                ]) {
                    sh '''
                        set -e

                        echo "$DOCKERHUB_PASSWORD" | docker login \
                          --username "$DOCKERHUB_USERNAME" \
                          --password-stdin

                        docker push "$IMAGE_NAME:$IMAGE_TAG"
                        docker push "$IMAGE_NAME:latest"
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Successfully pushed ${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }

        always {
            sh 'docker logout || true'
            echo 'Pipeline completed.'
        }
    }
}