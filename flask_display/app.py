
from flask import Flask, render_template, request, redirect
import model
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():    
	# choice = request.form['display']
	try:
		display_type = request.form.to_dict()['display']
	except:
		display_type = 'skills'

	if display_type=='skills':
		data = model.getSkills()
	elif display_type == 'people':
		data = model.getPeople()
	else:
		data = model.getCompanys()
	return render_template('index.html', data = data, display_type=display_type)

def run():
	app.run(debug=True)
if __name__ == '__main__':  
    print('starting Flask app', app.name)  
    app.run(debug=True)