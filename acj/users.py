from flask import Blueprint, jsonify
from bouncer.constants import READ, MANAGE, EDIT
from flask.ext.restful import Resource, Api, fields, marshal_with

from flask_bouncer import requires, ensure
from flask_login import login_required
from werkzeug.exceptions import Unauthorized
from .util import to_dict, pagination

#from general import admin, teacher, commit, hasher
from .models import Users, CoursesAndUsers

users_api = Blueprint('users_api', __name__)

sysrole_fields = {
	'id': fields.Integer,
	'name': fields.String,
}

user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'displayname': fields.String,
	'firstname': fields.String,
	'lastname': fields.String,
	'email': fields.String,
	'fullname': fields.String,
	'created': fields.DateTime,
	'modified': fields.DateTime,
	'lastonline': fields.DateTime,
	'usertypesforsystem_id': fields.Integer,
	'usertypeforsystem': fields.Nested(sysrole_fields),
}


class UserAPI(Resource):
	@login_required
	@marshal_with(user_fields)
	def get(self, id):
		user = Users.query.get_or_404(id)
		# check that the logged in user can read this user
		ensure(READ, user)
		return user


class UserListAPI(Resource):
	@login_required
	@requires(MANAGE, Users)
	@pagination(Users)
	@marshal_with(user_fields)
	def get(self, objects):

		return objects


class UserCourseListAPI(Resource):
	@login_required
	def get(self, id):
		user = Users.query.get_or_404(id)
		# we want to list courses only, so only check the association table
		coursesandusers = []
		for courseanduser in user.coursesandusers:
			ensure(READ, courseanduser)
			coursesandusers.append(courseanduser)

		# sort alphabetically by course name
		coursesandusers.sort(key=lambda courseanduser: courseanduser.course.name)
		# convert to dict
		courses_ret = to_dict(coursesandusers, ["user"])

		# TODO REMOVE COURSES WHERE USER IS DROPPED?
		# TODO REMOVE COURSES WHERE COURSE IS UNAVAILABLE?

		return jsonify({"objects": courses_ret})

api = Api(users_api)
api.add_resource(UserAPI, '/<int:id>')
api.add_resource(UserListAPI, '')
api.add_resource(UserCourseListAPI, '/<int:id>/courses')

# Get user which checks permissions to restrict what information the client gets about other users.
# This provides a measure of anonymity among students, while instructors and above can see real names.
def get_user(id):
	user = Users.query.get_or_404(id)
	# Determine if the logged in user can view full info on the target user
	access_restricted = True
	try:
		ensure(READ, user)  # check that the logged in user can read this user
		access_restricted = False
	except Unauthorized:
		pass
	if access_restricted:
		enrolments = CoursesAndUsers.query.filter_by(users_id = id).all()
		# if the logged in user can edit the target user's enrolments, then we let them see full info
		for enrolment in enrolments:
			try:
				ensure(EDIT, enrolment)
				access_restricted = False
				break
			except Unauthorized:
				pass
	user_ret = to_dict(user, ["coursesandusers"])
	# Insert other information
	user_ret['avatar'] = user.avatar()
	# Delete information that should not be transmitted
	del user_ret['_password'] # having to manually strip passwords is a bit annoying
	if access_restricted:
		del user_ret['username'] # should only need displayname
		del user_ret['fullname']
		del user_ret['firstname']
		del user_ret['lastname']
		del user_ret['email']
		del user_ret['created']
		del user_ret['modified']
	return user_ret

#def import_users(list, group=True):
#	schema = {
#			'type': 'object',
#			'properties': {
#				'username': {'type': 'string'},
#				'usertype': {'type': 'string',
#					'enum': ['Admin', 'Student', 'Teacher']},
#				'password': {'type': 'string'},
#				'email': {'type': 'string', 'format': 'email', 'required': False},
#				'firstname': {'type': 'string', 'required': False},
#				'lastname': {'type': 'string', 'required': False},
#				'display': {'type': 'string', 'required': False}
#				}
#			}
#	# query all used usernames and displays
#	query = Users.query.with_entities(Users.username).all()
#	usernames = [item for sublist in query for item in sublist]
#	query = Users.query.with_entities(Users.displayname).all()
#	displays = [item for sublist in query for item in sublist]
#	duplicate = []
#	error = []
#	success = []
#	for user in list:
#
#		try:
#			validictory.validate(user, schema)
#		except ValueError as err:
#			error.append({'user': user, 'msg': str(err), 'validation': True})
#			continue
#
#		# fill in empty values if they don't exist
#		if not 'firstname' in user:
#			user['firstname'] = ''
#		if not 'lastname' in user:
#			user['lastname'] = ''
#		if not 'display' in user:
#			user['display'] = ''
#
#		if user['username'] in duplicate:
#			error.append({'user': user, 'msg': 'Duplicate username in file'})
#			continue
#		if user['username'] in usernames:
#			if not group:
#				error.append({'user': user, 'msg': 'Username already exists'})
#			else:
#				u = Users.query.filter_by( username = user['username'] ).first()
#				if u.userrole.role == 'Student':
#					user = {'id': u.id, 'username': u.username, 'password': 'hidden', 'usertype': 'Student',
#							'email': u.email, 'firstname': u.firstname, 'lastname': u.lastname, 'display': u.display}
#					duplicate.append(user['username'])
#					success.append({'user': user})
#				else :
#					error.append({'user': user, 'msg': 'User is not a student'})
#			continue
#		if user['display'] in displays:
#			if not group:
#				error.append({'user': user, 'msg': 'Display name already exists'})
#				continue
#			integer = random.randrange(1000, 9999)
#			user['display'] = user['display'] + ' ' + str(integer)
#		if 'email' in user:
#			email = user['email']
#			if not re.match(r"[^@]+@[^@]+", email):
#				error.append({'user': user, 'msg': 'Incorrect email format'})
#				continue
#		else:
#			email = ''
#		usertype = UserTypesForSystem.query.filter_by(name = user['usertype']).first().id
#		newUser = Users(
#			username = user['username'],
#			usertypesforsystem = usertype,
#			email = email,
#			firstname = user['firstname'],
#			lastname = user['lastname'],
#			displayname = user['display']
#		)
#		newUser.set_password(user['password'])
#		db_session.add(newUser)
#		status = db_session.commit()
#		if not status:
#			error.append({'user': user, 'msg': 'Error'})
#		else:
#			# if successful append usernames + displays to prevent duplicates
#			duplicate.append(user['username'])
#			displays.append(user['display'])
#			user['id'] = newUser.id
#			success.append({'user': user})
#	return {'error': error, 'success': success}
#
#@teacher.require(http_exception=401)
#def csv_user_parser(filename):
#	reader = csv.reader(open(filename, "rU"))
#	list = []
#	error = []
#	for row in reader:
#		# filter removes trailing empty columns in cases where some rows have more than 4 columns
#		row = filter(None, row)
#		if len(row) != 4:
#			error.append({'user': {'username': 'N/A', 'display': 'N/A'}, 'msg': str(row) + ' is an invalid row'})
#			continue
#		user = {'username': row[0], 'password': password_generator(), 'usertype': 'Student',
#				'email': row[3], 'firstname': row[1], 'lastname': row[2], 'display': row[1] + ' ' + row[2]}
#		list.append(user)
#	return {'list': list, 'error': error}
#
#@teacher.require(http_exception=401)
#def password_generator(size=16, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
#	return ''.join(random.choice(chars) for x in range(size))
#
#@users_api.route('/userimport', methods=['POST'])
#@teacher.require(http_exception=401)
#def user_import():
#	file = request.files['file']
#	if not file or not allowed_file(file.filename):
#		return json.dumps( {"completed": True, "msg": "Please provide a valid file"} )
#	schema = {
#			'type': 'object',
#			'properties': {
#				'course': {'type': 'string'}
#				}
#			}
#	try:
#		validictory.validate(request.form, schema)
#	except ValueError, error:
#		return json.dumps( {"completed": True} )
#	courseId = request.form['course']
#	retval = []
#	ts = time.time()
#	timestamp = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
#	filename = timestamp + '-' + secure_filename(file.filename)
#	file.save(os.path.join(users_api.config['UPLOAD_FOLDER'], filename))
#	content = csv_user_parser(os.path.join(users_api.config['UPLOAD_FOLDER'], filename))
#	result = import_users(content['list'])
#	enrolled = []
#	success = []
#	if len(result['success']):
#		enrolled = enrol_users(result['success'], courseId)
#		success = enrolled['success']
#		enrolled = enrolled['error']
#	error = result['error'] + enrolled + content['error']
#	return json.dumps( {"success": success, "error": error, "completed": True} )
#
#@users_api.route('/user/<id>', methods=['POST'])
#@teacher.require(http_exception=401)
#def create_user(id):
#	result = import_users([request.json], False)
#	return json.dumps(result)
#
#@users_api.route('/user/<id>', methods=['PUT'])
#def edit_user(id):
#	user = ''
#	loggedUser = Users.query.filter_by(username = session['username']).first()
#	if id == '0':
#		user = loggedUser
#	elif id:
#		user = Users.query.filter_by(id = id).first()
#	param = request.json
#	schema = {
#			'type': 'object',
#			'properties': {
#				'email': {'type': 'string', 'format': 'email', 'required': False},
#				'display': {'type': 'string'},
#				'password': {
#					'type': 'object',
#					'properties': {
#						'old': {'type': 'string'},
#						'new': {'type': 'string'},
#						},
#					'required': False
#					},
#				}
#			}
#	try:
#		validictory.validate(param, schema)
#	except ValueError as error:
#		print (str(error))
#		return ''
#	display = param['display']
#	query = Users.query.filter(Users.id != user.id).filter_by(display = display).first()
#	if query:
#		db_session.rollback()
#		return json.dumps( {"flash": 'Display name already exists'} )
#	user.display = display
#	if 'email' in param:
#		email = param['email']
#		if not re.match(r"[^@]+@[^@]+", email):
#			db_session.rollback()
#			return json.dumps( {"flash": 'Incorrect email format'} )
#		user.email = email
#	else:
#		user.email = ''
#	if 'password' in param:
#		if not user.verify_password(param['password']['old']):
#			db_session.rollback()
#			return json.dumps( {"flash": 'Incorrect password'} )
#		user.set_password(param['password']['new'])
#	usertype = user.usertypeforysystem
#	db_session.commit()
#	return json.dumps( {"msg": "PASS", "usertype": usertype} )
#
#@users_api.route('/admin', methods=['POST'])
#def create_admin():
#	print "Here 1"
#	result = import_users([request.json], False)
#	print "Here 2"
#	file = open('tmp/installed.txt', 'w+')
#	print "Here 3"
#	return json.dumps(result)
#
#@users_api.route('/password/<uid>')
#@admin.require(http_exception=401)
#def reset_password(uid):
#	user = User.query.filter_by( id = uid ).first()
#	password = password_generator()
#	user.password = hasher.hash_password( password )
#	commit()
#	return json.dumps( {"resetpassword": password} )
#
