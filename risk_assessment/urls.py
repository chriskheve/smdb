from django.urls import path

from . import api

urlpatterns = [
    path('create/', api.create_risk_assement, name='create_risk_assement'),
    # path('<uuid:vendor_id>/', api.get_vendor_by_id, name='get_vendor_by_id'),
    # path('all/', api.get_all_vendor, name='get_all_vendor'),
    # path('pagination/', api.get_vendor_pagination, name='get_vendor_pagination'),
    # path('update/<uuid:vendor_id>/', api.update_vendor, name='update_vendor'),
    # path('all/v2/', api.get_vendors_by_user_department, name='get_vendors_by_user_department'),
    # path('upload/', api.upload_data, name='upload_data'),
    
]