import os
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

urlpatterns = patterns('',
    # Example:
    url(r'^$', 'life.goals.views.dun_did_it', name="dun_did_it"),
    url(r'^activity/$', 'life.goals.views.recent_didits', name="recent_didits"),
    url(r'^goals/$', 'life.goals.views.add_goal', name="add_goal"),
    url(r'^categories/$', 'life.goals.views.add_category', name="add_category"),
    url(r'^goal/(?P<goal_id>[0-9]+)/delete/$', 'life.goals.views.delete_goal', name="delete_goal"),
    url(r'^category/(?P<category_id>[0-9]+)/delete/$', 'life.goals.views.delete_category', name="delete_category"),

    url(r'^goal/(?P<goal_id>[0-9]+)/public/$', 'life.goals.views.toggle_goal_is_public', name="toggle_goal_is_public"),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(SITE_ROOT, '..', 'static')}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
