FILE=docker-compose.yml
if [ ! -f "$FILE" ]
then
    echo "$FILE DOES NOT EXIST"
    echo "EXITING SCRIPT"
    exit 1
fi 
BUILD_DATE=`date -u +'%Y-%m-%dT%H:%M:%SZ'`
COMMIT_ID=$(git rev-parse --verify HEAD)
COMMIT_ID=${COMMIT_ID:0:8}
VER=`date -u +'%Y%m%d'`
VER="${VER}_${COMMIT_ID}"
TAG=${PWD##*/}
DIR=$2
sudo docker-compose up -d --build
echo "BUILD FROM $FILE COMPLETE"
exit 0