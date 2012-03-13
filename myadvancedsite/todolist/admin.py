from myadvancedsite.todolist.models import Item
from myadvancedsite.todolist.models import DateTime
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import escape, escapejs
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority', 'difficulty', 'created', 'mark_done', 'done']
    search_fields = ['name']
    
class ItemInline(admin.TabularInline):
    model = Item
    extra = 3
    
class DateAdmin(admin.ModelAdmin):
    list_display = ['datetime']
    inlines = [ItemInline]
    
    def response_add(self, request, obj, post_url_continue='../%s/'):
        """ Determines the HttpResponse for the add_view stage. """
        opts = obj._meta
        pk_value = obj._get_pk_val()

        msg = "Item(s) were added successfully."
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if "_popup" in request.POST:
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if "_popup" in request.POST:
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % \
                # escape() calls force_unicode.
                (escape(pk_value), escapejs(obj)))
        elif "_addanother" in request.POST:
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)

            # Figure out where to redirect. If the user has change permission,
            # redirect to the change-list page for this object. Otherwise,
            # redirect to the admin index.
            if self.has_change_permission(request, None):
                post_url = '../'
            else:
                post_url = '../../../'
            return HttpResponseRedirect(reverse('admin:todolist_item_changelist'))
    
admin.site.register(Item, ItemAdmin)
admin.site.register(DateTime, DateAdmin)