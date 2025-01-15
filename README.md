To run it you need:

- clone this source code to your PC. 
- create any Python virtual environment you like, naming it whatever you like. 
- activate the virtual environment. 
- in the terminal go to the root folder of the project, to realize that you are there, type the `ls` command, in the list you should see the `requirements.txt` file. 
- install all dependencies using the `pip install -r requirements.txt` command 
- Run `./manage.py migrate`. `Not mandatory, just to get rid of terminal warning`
- run the project with the command `./manage.py runserver` 
- open http://127.0.0.1:8000/jsonrpc-call/ in your browser.
- in the `Method` input field, type `auth.check` for example, and click `Submit`, it should return you `green result` with data.
