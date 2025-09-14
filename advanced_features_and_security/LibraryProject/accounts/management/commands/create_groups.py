from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create default groups and assign permissions'

    def handle(self, *args, **kwargs):
        librarians, created = Group.objects.get_or_create(name='Librarians')
        members, created = Group.objects.get_or_create(name='Members')

        content_type = ContentType.objects.get_for_model(Book)

        can_add = Permission.objects.get(codename='add_book', content_type=content_type)
        can_change = Permission.objects.get(codename='change_book', content_type=content_type)
        can_delete = Permission.objects.get(codename='delete_book', content_type=content_type)
        can_view = Permission.objects.get(codename='view_book', content_type=content_type)

        librarians.permissions.set([can_add, can_change, can_delete, can_view])
        members.permissions.set([can_view])

        self.stdout.write(self.style.SUCCESS('Groups and permissions created successfully.'))
