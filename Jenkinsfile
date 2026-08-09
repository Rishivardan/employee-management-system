pipeline {
    agent any

    environment {
        IMAGE_NAME = "rishiadl29/employee-management-system"
        IMAGE_TAG  = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Tools') {
            steps {
                sh '''
                    docker --version
                    git --version
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    set -e

                    docker build \
                      -t "$IMAGE_NAME:$IMAGE_TAG" .

                    docker tag \
                      "$IMAGE_NAME:$IMAGE_TAG" \
                      "$IMAGE_NAME:latest"
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

                        echo "$DOCKERHUB_PASSWORD" | \
                        docker login \
                          --username "$DOCKERHUB_USERNAME" \
                          --password-stdin

                        docker push "$IMAGE_NAME:$IMAGE_TAG"
                        docker push "$IMAGE_NAME:latest"
                    '''
                }
            }
        }


        stage('Update Helm Image Tag') {
            steps {
                sh '''
                    set -e

                    sed -i \
                      's/tag: "v[0-9]*"/tag: "'"$IMAGE_TAG"'"/' \
                      employee-management-chart/values.yaml

                    git config user.name "jenkins"
                    git config user.email "jenkins@local"

                    git add employee-management-chart/values.yaml

                    git commit \
                      -m "Deploy $IMAGE_TAG via Jenkins" \
                      || echo "No changes to commit"
                '''
            }
        }
    }

    post {
        success {
            echo "CI SUCCESS ✅"
            echo "Built and pushed image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo "CI FAILED ❌"
            echo "Check the failed stage in Jenkins Console Output."
        }

        always {
            sh 'docker logout || true'
        }
    }
}