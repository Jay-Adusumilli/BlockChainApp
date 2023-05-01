echo "Starting the server"
start cmd /k python server.py
timeout /t 1
echo "Starting the clients"
start cmd /k python client2.py
start cmd /k python client3.py
start cmd /k python client4.py
timeout /t 1
start cmd /k python client1data.py