from django.db import migrations


def crear_roles_iniciales(apps, schema_editor):
    Roles = apps.get_model("login", "Roles")

    # Definimos los roles que queremos asegurar en la BD
    roles_data = [
        {
            "nombre_rol": "Administrador",
            # Aquí puedes ajustar permisos según tu lógica
            "permisos": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
        },
        {
            "nombre_rol": "Usuario",
            "permisos": [1, 2, 3],  # ejemplo: permisos más básicos
        },
        {
            "nombre_rol": "Jefe Bodega",
            "permisos": [1, 2, 3, 4, 5, 6],  # ejemplo: más permisos que Usuario
        },
    ]

    for data in roles_data:
        Roles.objects.update_or_create(
            nombre_rol=data["nombre_rol"],
            defaults={
                "permisos": data["permisos"],
            },
        )

class Migration(migrations.Migration):

    dependencies = [
        # deja aquí lo que Django te generó automáticamente,
        # normalmente algo como ("login", "0001_initial")
        ("login", "0003_alter_roles_permisos"),
    ]

    operations = [
        migrations.RunPython(crear_roles_iniciales),
    ]
