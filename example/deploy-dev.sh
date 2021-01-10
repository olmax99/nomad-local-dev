#!/bin/bash

ENVIRONMENT_SLUG="job0"
#COMMIT_SHORT_SHA=$(git rev-parse HEAD | cut -c 1-8)
#echo "Git sha: ${COMMIT_SHORT_SHA}"
DOCKER_IMAGE="python:3.6.4-alpine3.7"
echo "Docker image: ${DOCKER_IMAGE}"
#DEPLOY_URL="$simpleserver.{ENVIRONMENT_SLUG}.dev"
#echo "Deploy URL: ${DEPLOY_URL}"
levant deploy -var docker_image="${DOCKER_IMAGE}" -var environment_slug="${ENVIRONMENT_SLUG}" simpleserver.nomad 
#-var git_sha="${COMMIT_SHORT_SHA}" \
#-var deploy_url="${DEPLOY_URL}" \

