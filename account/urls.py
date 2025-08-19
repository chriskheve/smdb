from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api
from .views import CustomLoginView
urlpatterns = [
    path('account/me/', api.me, name='me'),
    path('account/signup/', api.signup, name='signup'),
    # path('account/create_user_with_location/', api.create_user_with_location, name='create_user_with_location'),
    path('account/login/', CustomLoginView.as_view(), name='custom-login'),
    # path('account/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('account/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('account/user/<uuid:user_id>/', api.get_user_by_id, name='get_user_by_id'),
    # path('account/user/zm/', api.get_user_zm, name='get_user_zm'),
    # path('account/role/all/', api.get_roles, name='get_roles'),
    # path('account/role/new/', api.create_role, name='create_role'),
    # path('account/group-user/all/', api.get_group_user, name='get_group_user'),
    # path('account/group-user/new/', api.create_group_user, name='create_group_user'),
    # path('account/position/all/', api.get_positions, name='get_positions'),
    # path('account/position/new/', api.create_positions, name='create_positions'),
    # path('account/user/edit_password/', api.edit_password, name='edit_password'),
    # path('account/user/edit/<uuid:user_id>/', api.edit_user, name='edit_user'),
    # path('account/user/update-password/<uuid:user_id>/', api.update_password_by_user_id, name='update_password_by_user_id'),
    # path('account/user/update/<uuid:user_id>/', api.update_user2, name='update_user2'),
    # path('account/user/activation/<uuid:user_id>/', api.activate_or_deactivate_user, name='activate_or_deactivate_user'),
    # path('account/user/all/', api.get_all_users, name='get_all_users'),
    # path('account/user/pagination/', api.get_users_pagination, name='get_users_pagination'),
]