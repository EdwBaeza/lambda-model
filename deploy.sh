
source "/Users/$(whoami)/.zshrc"

LAMBDA_NAME='lambdamodelfunction' # must be equals into template.yaml in lower case
ENVIRONMENT=${1:-dev} # this variable will be used for docker tag and environment
REGION=us-west-2

echo "Building $LAMBDA_NAME image in $ENVIRONMENT environment by sam"

sam build --use-container --parameter-overrides DockerTag=$ENVIRONMENT

echo "Validate if exists repository $LAMBDA_NAME/$ENVIRONMENT"

aws ecr describe-repositories --repository-name $LAMBDA_NAME/$ENVIRONMENT --max-items 1  > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "Repository not found"
    echo "Creating repository...."
    aws ecr create-repository --repository-name  $LAMBDA_NAME/$ENVIRONMENT
fi

echo "Describe respository"
aws ecr describe-repositories --repository-name "$LAMBDA_NAME/$ENVIRONMENT" --max-items 1 > ecr_output.json

REPOSITORY_URI=$(python -c "import json; print(json.load(open('ecr_output.json'))['repositories'][0]['repositoryUri'])")

echo "Login repository $REPOSITORY_URI"
aws ecr get-login-password --region $REGION | docker login -u AWS --password-stdin $REPOSITORY_URI

echo "Pushing docker image $LAMBDA_NAME:$ENVIRONMENT  to aws"
docker tag $LAMBDA_NAME:$ENVIRONMENT $REPOSITORY_URI:latest
docker push $REPOSITORY_URI:latest

echo "Deploying $LAMBDA_NAME lambda function to aws"
sam deploy --stack-name $LAMBDA_NAME --region $REGION --capabilities CAPABILITY_IAM --image-repository $REPOSITORY_URI