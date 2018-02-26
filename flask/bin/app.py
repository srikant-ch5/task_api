from flask import Flask,jsonify,abort,make_response,request

app = Flask(__name__)

tasks = [
	{
	'id':1,
	'title':u'Working out daily',
	'description' : u'Doing strength training',
	'done':False
	},
	{
	'id':2,
	'title':u'Coding',
	'description':u'Coding whatever I want for atleast 2 hours a day',
	'done':False
	}
]

@app.route('/todo/api/v1.0/tasks/<int:task_id>',methods=['GET'])
def get_tasks(task_id):
	task = [ taski for taski in tasks if taski['id'] == task_id]
	
	if(len(task) == 0):
		abort(404)
	return jsonify({'task':tasks[0]})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':'Error message: Page for task does not exist'}),404)

@app.route('/todo/api/v1.0/tasks',methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(404)

	task = {
		'id':tasks[-1]['id'] + 1,
		'title': request.json['title'],
		'description':request.json.get('description',""),
		'done':False
	}

	tasks.append(task)
	return jsonify({'tasks':tasks}) ,201

@app.route('/todo/api/api/v1.0/tasks/<int:task_id>',methods=['PUT'])
def update_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'title' in request.json and type(request.json['title']) != unicode:
		abort(400)
	if 'description' in request.json and type(request.json['description']) != unicode:
		abort(400)
	if 'done' in request.json type(request.json['done']) is not bool:
		abort(400)

	task[0]['title'] = request.json.get('title',task[0]['title'])
	task[0]['description'] =request.json.get('description',task[0]['description'])
	task[0]['done'] = request.json.get('done',task[0]['done'])

	return jsonify({'task':task[0]})

@app.route('/todo/api/v2.0/tasks/<int:task_id>',methods=['DELETE'])
def remove_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]

	if len(task) == 0:
		abort(404)

	tasks.remove(task[0])

	return jsonify({'result':True})

#more to add the added security features

if __name__ == '__main__':
    app.run(debug=True)
