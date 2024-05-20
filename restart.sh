docker stop reportbro
docker remove reportbro
docker run --name reportbro -p 5012:5012 reportbro:latest
