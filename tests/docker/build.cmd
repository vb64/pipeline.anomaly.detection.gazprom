rem files to add
cp ../../tests/requirements.txt tests.txt
docker-compose build
rem cleanup
rm tests.txt
