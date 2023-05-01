echo "Starting the server"
start cmd /k python server.py
timeout /t 3
echo "Starting the clients"
start cmd /k python client1.py
timeout /t 1
start cmd /k python client2.py
timeout /t 1
start cmd /k python client3.py
timeout /t 1
start cmd /k python client4.py
