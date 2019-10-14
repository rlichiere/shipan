# Thesaurus

The thesaurus tools allow the customization of Shipan messages.

Use the `makemessages` and `compilemessages` commands in order to **generate** and **reimport** the thesaurus files of the website.
 A `django.po` file corresponds to each language, in which you are invited to **perform the desired customizations**.

* [Commands](#commands)
  * [Export : makemessages](#command_makemessages)
  * [Customize messages](#command_customize)
  * [Reimport : compilemessages](#command_compilemessages)
* [Samples](#samples)
  * [All languages](#sample_all_languages)
  * [A specific language](#sample_specific_language)

## Commands
<a name='commands'></a>

### Export messages: `makemessages`
<a name='command_makemessages'></a>
Export messages of a specific language to a file : `locale/[LANGAGE_TO_EXPORT]/LC_MESSAGES/django.po`
```
python manage.py makemessages -l [LANGAGE_TO_EXPORT]
```

Export messages of all languages
```
python manage.py makemessages -l [LANGAGE_TO_EXPORT]
```

### Customize messages: `vi`
<a name='command_customize'></a>
Customize the the desired `django.po` file with you favorite editor, then [recompile](#compilemessages) the thesaurus.

### Reimport messages: `compilemessages`
<a name='command_compilemessages'></a>

After having customized somme messages, you must reimport the thesaurus files in order so see changes in the site.
```
python manage.py compilemessages -l [LANGAGE_TO_COMPILE]
```

Recompile all languages thesaurus
```
python manage.py compilemessages
```
<div class="float-right"><a href=#top>Top</a></div>

## Samples
<a name='samples'></a>

### All languages
<a name='sample_all_languages'></a>
For example, export and reimport the English thesaurus:
```
python manage.py makemessages
python manage.py compilemessages
```

### A specific language
<a name='sample_specific_language'></a>
For example, export and reimport the English thesaurus:
```
python manage.py makemessages -l en
python manage.py compilemessages -l en
```
