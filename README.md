# Pychat

## What is it
  A IRC chat like implementation written in python with sockets and kivy.

## Usage

  Inside the folder, open a   `pipenv shell` and install the dependencies with `pipenv install`.
  If you don't have pipenv installed, install it with `pip`.

  First, you need to run the server with `python server.py`.
  Then, open as many clients you want with `python cliente.py`

  Commands available:
  - **MSG**: sends a message to every client connected
  - **PRIVATE**:  **\<nick>:\<msg>** sends a message to one client
  - **NICK**: **\<nick>** changes nickname
  - **EXIT**: closes connection