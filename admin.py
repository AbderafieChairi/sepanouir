from models import *
from flask_admin import Admin,AdminIndexView,expose
from flask_admin.contrib.sqla import ModelView
from flask import session

# admin = Admin(url="/hhh")
# class MyHomeView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         arg1 = 'Hello'
#         return self.render('admin/index.html', arg1='admin' in session)

# admin = Admin(index_view=MyHomeView())
admin = Admin()
class Admin_required(ModelView):
	column_exclude_list = ['users','comments','activities_attend','particpants','msgs','activities','public_id','time']
	form_excluded_columns = column_exclude_list
	def is_accessible(self):
		# print(session)
		# return 'admin' in session
		return True


admin.add_view(Admin_required(Activity, db.session))
admin.add_view(Admin_required(User, db.session))
admin.add_view(Admin_required(Partenaire, db.session))
admin.add_view(Admin_required(Partenaire_user, db.session))
admin.add_view(Admin_required(Sport, db.session))
admin.add_view(Admin_required(Alimentation, db.session))
admin.add_view(Admin_required(Sponsor, db.session))
admin.add_view(Admin_required(became_Partenaire, db.session))
admin.add_view(Admin_required(Options, db.session))
admin.add_view(Admin_required(activite_user_attend, db.session))
admin.add_view(Admin_required(Participants, db.session))
admin.add_view(Admin_required(Room, db.session))
admin.add_view(Admin_required(Message, db.session))

