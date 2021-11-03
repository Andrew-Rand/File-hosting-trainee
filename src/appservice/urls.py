from django.urls import re_path

from .views.all_files_view import AllFilesView
from .views.change_password_view import ChangePasswordView
from .views.delete_file_view import DeleteFileView
from .views.edit_file_description_view import EditFiledescriptionView
from .views.file_detail_view import FileDetailView
from .views.user_detail_view import UserDetailView

urlpatterns = [
    re_path(r'^files/$', AllFilesView.as_view(), name='all_user_files'),
    re_path(r'^files/(?P<pk>[0-9A-Fa-f-]+)/$', FileDetailView.as_view(), name='file_detail'),
    re_path(r'^files/(?P<pk>[0-9A-Fa-f-]+)/delete/$', DeleteFileView.as_view(), name='delete_file'),
    re_path(r'^files/(?P<pk>[0-9A-Fa-f-]+)/edit/$', EditFiledescriptionView.as_view(), name='edit_description'),
    re_path(r'^user/$', UserDetailView.as_view(), name='user_view_and_update'),
    re_path(r'^user/change_password/$', ChangePasswordView.as_view(), name='change_password'),

]
