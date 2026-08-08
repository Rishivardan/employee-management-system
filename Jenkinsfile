pipeline {
    agent any

    environment {
        IMAGE_NAME = "rishiadl29/employee-management-system"
        IMAGE_TAG  = "v${BUILD_NUMBER}"

        HELM_RELEASE = "employee-app"
        HELM_CHART   = "./employee-management-chart"
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
                    kubectl version --client
                    helm version
                    kubectl config current-context
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

        stage('Verify Kubernetes') {
            steps {
                sh '''
                    kubectl get nodes
                    kubectl get pods
                '''
            }
        }

        stage('Deploy with Helm') {
            steps {
                sh '''
                    set -e

                    helm upgrade --install \
                      "$HELM_RELEASE" \
                      "$HELM_CHART" \
                      --set image.repository="$IMAGE_NAME" \
                      --set image.tag="$IMAGE_TAG" \
                      --wait
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl rollout status \
                      deployment/employee-management \
                      --timeout=120s

                    kubectl get pods
                    kubectl get services
                    helm list
                '''
            }
        }
    }

    post {

        success {
            echo "CI/CD SUCCESS ✅"
            echo "Deployed image: ${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo "CI/CD FAILED ❌"
            echo "Check the failed stage in Jenkins Console Output."
        }

        always {
            sh 'docker logout || true'
        }
    }
}