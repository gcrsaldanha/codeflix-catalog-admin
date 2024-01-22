Instalar o Django:
```bash
$ python -m pip install Django
```

Criar o projeto "django_project
```bash
$ django-admin startproject django_project src
```

Mover o `manage.py` para a raíz do projeto
```bash
$ mv src/manage.py ./
```

Atualizar o `manage.py`:
```python
sys.path.append("src")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
```

Em `settings.py`, confirmar se as variáveis estão com esses valores:
```python
ROOT_URLCONF = 'django_project.urls'
WSGI_APPLICATION = 'django_project.wsgi.application'
```

E atualizar o `BASE_DIR` (adicionar um `.parent`):
```python
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```

Criar o `category_app` **dentro** de `django_project/`
```bash
$ mkdir -p src/django_project/category_app
$ python manage.py startapp category_app src/django_project/category_app
```

"Instalar" o `category_app` em `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'django_project.category_app',
]
```

Atualizar o `CategoryAppConfig` (category_app/apps.py):
```python
name = 'django_project.category_app'
```

Executar as migrações:
```bash
$ python manage.py migrate
```

Executar o servidor:
```bash
$ python manage.py runserver
```

