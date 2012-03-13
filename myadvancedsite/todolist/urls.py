from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('todolist.views',
    url(r'^mark_done/(\d*)/$', 'mark_done'),
)
