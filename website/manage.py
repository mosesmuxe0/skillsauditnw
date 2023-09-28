def deploy():
	"""Run deployment tasks."""
	from . import create_app,db
	from flask_migrate import upgrade,Migrate,init,stamp
	from models import User, Note, Personal

	app = create_app()
	app.app_context().push()
	db.create_all()

	# migrate database to latest revision
	init()
	stamp()
	Migrate()
	upgrade()
	
deploy()