from myadvancedsite.todolist.models import Item
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def mark_done(request, pk):
    item = Item.objects.get(pk=pk)
    item.done = True
    item.save()
    return HttpResponseRedirect(reverse('admin:todolist_item_changelist'))
