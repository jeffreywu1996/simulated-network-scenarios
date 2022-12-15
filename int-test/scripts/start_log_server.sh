echo "Starting log-server and ping-pong server"

if [[ -z "${TEST_HASH}" ]]; then
  echo "TEST_HASH not set. exiting"
  exit 1
fi

(cd server && python3 log-server/main.py &)
(cd server && python3 server_ping_pong.py &)
