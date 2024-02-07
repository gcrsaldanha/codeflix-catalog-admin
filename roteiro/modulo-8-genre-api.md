# Módulo 8: Genre API

## Aula 1: Corrigindo o import path

- Os imports estão inconsistentes para módulos do projeto Django e do Core
- Renomear apps para src.django_project.*
    - settings.py
    - AppConfig (apps.py)
    - Isso vai fazer com que os imports fiquem mais consistents
    - Procurar por todos imports de "django_project." e trocar para "src.django_project."
- Commit: https://github.com/gcrsaldanha/codeflix-catalog-admin/commit/77517848b94d39212f63e5d8984b4be83ff432d8


## Aula 2: Criar GenreApp e Genre Model

- Criar o app genre_app
- Genre model com app_label (copiar Category)
- Atualizar AppConfig
- Gerar e executar migrações
- Utilizar o shell_plus para criar gêneros
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


## Aula 3: Implementando Django GenreRepository
- Falar sobre o `.categories`
    - `.categories.add`
    - `.categories.set`


## Aula 4: List API
- Problema de ordenação: vamos resolver isso futuramente


## Aula 5: Create API
- Dois erros: `InvalidGenre` e `RelatedCategoriesNotFound`: HTTP_400


## Aula 6: Delete API
- GenreNotFound: 404


## Desafio: Update API

Implementar API de Update (PUT) com os seguintes testes:

- test_when_request_data_is_valid_then_update_genre
- test_when_request_data_is_invalid_then_return_400
- test_when_related_categories_do_not_exist_then_return_400
- test_when_genre_does_not_exist_then_return_404


Faça um checkout para o commit `7253cf059f1509215f730e196e2e825e5087a791`

```bash
git checkout 7253cf059f1509215f730e196e2e825e5087a791
```

> Os testes já estão implementados em `genre_app/tests/test_views.py`

Se preferir, pode escrever seus próprios testes. Lembre-se que o método PUT assume que todos os valores do payload serão passados.
