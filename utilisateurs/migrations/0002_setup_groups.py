from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    prof_group, created = Group.objects.get_or_create(name='Professeurs')
    
    # On définit précisément quelle permission de quelle application on veut
    # Format : (nom_application, codename)
    permissions_to_add = [
        ('evaluation', 'add_note'),
        ('evaluation', 'change_note'),
        ('evaluation', 'view_note'),
        ('evaluation', 'add_absence'),
        ('evaluation', 'change_absence'),
        ('evaluation', 'view_absence'),
        ('etudiants', 'view_etudiant'),
        ('cours', 'view_module'),
    ]
    
    for app_label, codename in permissions_to_add:
        try:
            # On cherche la permission spécifique à l'application
            perm = Permission.objects.get(
                codename=codename,
                content_type__app_label=app_label
            )
            prof_group.permissions.add(perm)
        except Permission.DoesNotExist:
            print(f"Attention: Permission {codename} introuvable pour {app_label}")
        except Exception as e:
            print(f"Erreur sur {codename}: {e}")

class Migration(migrations.Migration):
    dependencies = [
        ('utilisateurs', '0001_initial'),
        ('etudiants', '0001_initial'),
        ('evaluation', '0001_initial'),
        ('cours', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'), # Important pour accéder aux ContentTypes
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]