# import os

# import os
# from os.path import join, dirname
# from dotenv import load_dotenv
# is_prod = os.environ.get('IS_SERVER', None)
# if not is_prod:
# 	dotenv_path = join(dirname(__file__), '.env')
# 	load_dotenv(dotenv_path, verbose=True)
# 	env=True
# else:
# 	env=False
# #     /**these settings will load up only when we are in a server environment*/
# #     APP_ENV = os.environ.get('APP_ENV')
# #     DEBUG = os.environ.get('DEBUG')






class Config(object):
	DEBUG = True
	TESTING = False
	CSRF_ENABLED = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SESSION_COOKIE_SECURE = True
	SESSION_COOKIE_HTTPONLY = True
	SESSION_COOKIE_SAMESITE = 'None'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True 




# class ProductionConfig(Config):
# 	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
# 	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
# 	SECRET_KEY = os.environ.get("SECRET_KEY")	
# 	SQLALCHEMY_DATABASE_URI = os.environ.get("NEW_DATABASE_URL")

# class DeveloppementConfig(Config):
# 	MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
# 	MAIL_USERNAME = os.getenv("MAIL_USERNAME")
# 	SECRET_KEY = os.getenv("SECRET_KEY")	
# 	SQLALCHEMY_DATABASE_URI = os.getenv("NEW_DATABASE_URL")	


class ProductionConfig(Config):
	MAIL_PASSWORD = 'devpro2022'
	MAIL_USERNAME = 'sepanouir.amdin@gmail.com'
	SECRET_KEY = 'kjsgjgfdskhgfdskhgfksgkfqgkfq'	
	# SQLALCHEMY_DATABASE_URI = 'postgresql://tgmczdwjvwuacl:a1938326006507ed76dd9c882cd4cf73188652e0bb0466836f41269d9db77e3b@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/det00nsjnk0hv4'	
	SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"