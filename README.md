# Org Chart

Org Chart is a minimal Django application that fetches a simplified view of an employee list
and renders a hierarchy list in a HTML list object.

## Usage

First create a virtual environment and install the required dependencies

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then start the server using 

```shell
python server.py runserver 8000
```

Finally start a static files server to render de UI

```shell
python -m http.server 8080
```

