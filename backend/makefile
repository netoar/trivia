.PHONY: all

env/bin/activate: requirements.txt
	/usr/local/bin/python3.8 -m venv env
	./env/bin/pip install -r requirements.txt

run: env/bin/activate
	FLASK_APP=flaskr ./env/bin/flask run

freeze: env/bin/pip
	./env/bin/pip freeze > requirements.txt

clean:
	rm -rf __pycache__
	rm -rf ./env