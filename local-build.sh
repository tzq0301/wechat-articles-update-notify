user=tzq0301
service=waun
tag=$user/$service

docker build -t $tag . --platform=linux/amd64
docker push $tag
