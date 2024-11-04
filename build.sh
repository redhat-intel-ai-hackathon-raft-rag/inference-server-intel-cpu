export $(cat .env | xargs)
docker build -t flask-app .
docker tag flask-app eichiuehara/redhat-intel-hackathon:latest
docker push eichiuehara/redhat-intel-hackathon:latest
