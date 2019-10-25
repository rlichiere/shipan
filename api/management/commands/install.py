# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from tools import constants

from ... import kernel


class Command(BaseCommand):
    help = """
        This command manages the main steps of the project installation:
      
        1. Load the installer configuration
         
            Configuration can be done directly through the command parameters,
                otherwise via a command line wizard. 
      
        2. Compile thesaurus (.mo) from translation files (.po)
            > python manage.py compilemessages
         
        3. Build potential Models migrations
            > python manage.py makemigrations
         
        4. Migrate Models
            > python manage.py migrate

        5. Create the superuser
            > python manage.py createsuperuser

        6. Create the potentially required cache table
            > python manage.py createcachetable

        7. Load the initial data of the models
            > python manage.py populate

        8. Diagnose project
            > python manage.py diagnose

        9. Backup project
            > python manage.py backup
      
        Examples:
        ```
        > python manage.py install
        > python manage.py install --no-confirm
        ```
    """

    def add_arguments(self, parser):
       parser.add_argument('--noinput', help="""
          Skip inputs potentially asked during the installation process.
       """,
                           default=False,
                           action='store_true')

       super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
       _result = kernel.install(**options)

       if _result.has_failed:
           exit(constants.COMMAND_EXIT_CODE.ERROR)
       exit(constants.COMMAND_EXIT_CODE.SUCCESS)
