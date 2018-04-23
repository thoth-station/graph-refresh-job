// Openshift project
OPENSHIFT_SERVICE_ACCOUNT = 'jenkins'
DOCKER_REGISTRY = env.CI_DOCKER_REGISTRY ?: 'docker-registry.default.svc.cluster.local:5000'
CI_NAMESPACE= env.CI_PIPELINE_NAMESPACE ?: 'ai-coe'
CI_TEST_NAMESPACE = env.CI_THOTH_TEST_NAMESPACE ?: 'ai-coe'

STABLE_LABEL = "stable"
tagMap = [:]

// Initialize
tagMap['graph-refresh-job'] = '0.1.0'

// IRC properties
IRC_NICK = "sesheta"
IRC_CHANNEL = "#thoth-station"

tokens = "${env.JOB_NAME}".tokenize('/')
org = tokens[tokens.size()-3]
repo = tokens[tokens.size()-2]
branch = tokens[tokens.size()-1]

properties(
    [
        buildDiscarder(logRotator(artifactDaysToKeepStr: '30', artifactNumToKeepStr: '', daysToKeepStr: '90', numToKeepStr: '')),
        disableConcurrentBuilds(),
    ]
)


library(identifier: "cico-pipeline-library@master",
        retriever: modernSCM([$class: 'GitSCMSource',
                              remote: "https://github.com/CentOS/cico-pipeline-library",
                              traits: [[$class: 'jenkins.plugins.git.traits.BranchDiscoveryTrait'],
                                       [$class: 'RefSpecsSCMSourceTrait',
                                        templates: [[value: '+refs/heads/*:refs/remotes/@{remote}/*']]]]])
                            )
library(identifier: "ci-pipeline@master",
        retriever: modernSCM([$class: 'GitSCMSource',
                              remote: "https://github.com/CentOS-PaaS-SIG/ci-pipeline",
                              traits: [[$class: 'jenkins.plugins.git.traits.BranchDiscoveryTrait'],
                                       [$class: 'RefSpecsSCMSourceTrait',
                                        templates: [[value: '+refs/heads/*:refs/remotes/@{remote}/*']]]]])
                            )
library(identifier: "ai-stacks-pipeline@master",
        retriever: modernSCM([$class: 'GitSCMSource',
                              remote: "https://github.com/AICoE/AI-Stacks-pipeline",
                              traits: [[$class: 'jenkins.plugins.git.traits.BranchDiscoveryTrait'],
                                       [$class: 'RefSpecsSCMSourceTrait',
                                        templates: [[value: '+refs/heads/*:refs/remotes/@{remote}/*']]]]])
                            )

pipeline {
    agent {
        kubernetes {
            cloud 'openshift'
            label 'thoth'
            serviceAccount OPENSHIFT_SERVICE_ACCOUNT
            containerTemplate {
                name 'jnlp'
                args '${computer.jnlpmac} ${computer.name}'
                image DOCKER_REGISTRY + '/'+ CI_NAMESPACE +'/jenkins-aicoe-slave:latest'
                ttyEnabled false
                command ''
            }
        }
    }
    stages {
        stage("Create Tempaltes") {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(CI_TEST_NAMESPACE) {
                            if (!openshift.selector("template/graph-refresh-job-buildconfig").exists()) {
                                openshift.apply(readFile('openshift/buildConfig-template.yaml'))
                                echo "BuildConfig Template created!"
                            }    

                            if (!openshift.selector("template/graph-refresh-job-cronjob").exists()) {
                                openshift.apply(readFile('openshift/cronJob-template.yaml'))
                                echo "CronJob Template created!"
                            }
                        }
                    }                    
                }
            }
        }
        stage("Setup BuildConfig") {
            steps {
                script {                    
                    env.TAG = "test"
                    env.REF = "master"

                    // TODO check if this works with branches that are not included in a PR
                    if (env.BRANCH_NAME != 'master') {
                        env.TAG = env.BRANCH_NAME.replace("/", "-")

                        if (env.Tag.startsWith("PR")) {
                            env.REF = "refs/pull/${env.CHANGE_ID}/head"
                        } else {
                            env.REF = branch.replace("%2F", "/")
                        }
                    }

                    openshift.withCluster() {
                        openshift.withProject(CI_TEST_NAMESPACE) {
                            /* Process the template and return the Map of the result */
                            def model = openshift.process('graph-refresh-job-buildconfig',
                                    "-p", 
                                    "IMAGE_STREAM_TAG=${env.TAG}",
                                    "GITHUB_URL=https://github.com/${org}/${repo}",
                                    "GITHUB_REF=${env.REF}")

                            createdObjects = openshift.apply(model) // FIXME This will fail if the BC is not present
                        }
                    }
                }
            } // steps
        } // stage
        stage("Setup ImageStream") {
           steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(CI_TEST_NAMESPACE) {
                            if (!openshift.selector("imagestream/graph-refresh-job").exists()) {
                                def model = openshift.process('graph-refresh-job-cronjob')

                                echo "----"
                                echo "${model}"
                                echo "----"

                                createdObjects = openshift.apply(model)

                                echo "${createdObjects}"
                                echo "----"
                            }
                        }
                    }
                }
           }
        }
        stage("Get Changelog") {
            steps {
                node('master') {
                    script {
                        env.changeLogStr = pipelineUtils.getChangeLogFromCurrentBuild()
                        echo env.changeLogStr
                    }
                    writeFile file: 'changelog.txt', text: env.changeLogStr
                    archiveArtifacts allowEmptyArchive: true, artifacts: 'changelog.txt'
                } // node: master
            } // steps
        } // stage
        stage("Build Container Images") {
            parallel {
                stage("Graph Refresh Job") {
                    steps {
                        echo "Building Thoth Graph Refresh Job container image..."
                        script {
                            tagMap['graph-refresh-job'] = aIStacksPipelineUtils.buildImageWithTag(CI_TEST_NAMESPACE, "graph-refresh-job", "${env.TAG}")
                        }

                    } // steps
                } // stage
            } // 
        } // stage
        stage("Tag Container Image as Test") {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(CI_TEST_NAMESPACE) {
                            echo "Creating test tag from graph-refresh-job:${env.TAG}"

                            openshift.tag("${CI_TEST_NAMESPACE}/graph-refresh-job:${env.TAG}", "${CI_TEST_NAMESPACE}/graph-refresh-job:test")
                        }
                    } // withCluster
                }
            }
        } // stage
        stage("Image Tag Report") {
            steps {
                script {
                    pipelineUtils.printLabelMap(tagMap)
                }
            }
        } // stage
        stage("Tag stable image") {
            steps {
                script {
                    // Tag ImageStreamTag ${env.TAG} as our new :stable
                    openshift.withCluster() {
                        openshift.withProject(CI_TEST_NAMESPACE) {
                            echo "Creating stable tag from graph-refresh-job:${env.TAG}"

                            openshift.tag("${CI_TEST_NAMESPACE}/graph-refresh-job:${env.TAG}", "${CI_TEST_NAMESPACE}/graph-refresh-job:stable")
                        }
                    } // withCluster
                } // script
            } // steps
        } // stage
        stage("Promotion to Stage") {
            steps {
                script {
                    echo 'Promoting Container Image to Stage Environment'
                } // script
            } // steps
        } // stage
    }
    post {
        always {
            script {
                // junit 'reports/*.xml'

                pipelineUtils.sendIRCNotification("${IRC_NICK}", 
                    IRC_CHANNEL,
                    "${JOB_NAME} #${BUILD_NUMBER}: ${currentBuild.currentResult}: ${BUILD_URL}")
            }
        }
        success {
            echo "All Systems GO!"
        }
    }
}
