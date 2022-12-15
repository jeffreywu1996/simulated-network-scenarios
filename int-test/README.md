# Integration test for sdk
Simulates a client and server both using sdk to interact

## How to run test case
### Local
```
./start.sh # docker mode
./start_single_docker.sh # Single docker (simulate jenkins environment)
```

### Run test file manually
1. `./start.sh`
   after running `start.sh`, it would pull up 2 containers named: 'server' and 'client'

2. `docker logs -f server`
   cat log from server docker

3. Start to another shell
   1. Go to file `./entrypoint.sh`, change this line `python3 -m pytest -vsx client` to `sleep 1000h`, Used to keep the clinet docker process
   2. `docker exec -it client /bin/bash`, exec in client docker
   3. `python3 -m pytest -vsx test_file.py`, run the test file


### Docker compose mode
```
./start.sh  # Will run in docker compose and auto run all tests
DEBUG=true ./start.sh  # Will start docker compose and run in /bin/bash mode
docker exec -it client /bin/bash  # Enter client docker
pytest -m pytest -vsx client/...  # Run tests you want
```

```
# Build cpp tests
./build.sh

# Start client, server, verifier docker
docker-compose up --build

# Start the test
docker exec -it client /bin/bash
 >>python3 -m pytest -vsx client

docker exec -it client python3 -m pytest -vsx client

# Start test script(TODO)
./start.sh
```
