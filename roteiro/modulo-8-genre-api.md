# Módulo 8: Genre API

## Aula 1: Corrigindo o import path

- Os imports estão inconsistentes para módulos do projeto Django e do Core
- Renomear apps para src.django_project.*
    - settings.py
    - AppConfig (apps.py)
    - Isso vai fazer com que os imports fiquem mais consistents
    - Procurar por todos imports de "django_project." e trocar para "src.django_project."
    - Verificar o commit



## Aula N: Configurando django shell plus

```bash
pip install django-extensions
pip install ipython
```

```python
INSTALLED_APPS = (
    ...
    "django_extensions",
)
```
