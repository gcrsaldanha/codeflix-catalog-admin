# codeflix-catalog-admin
Administração de Catálogo – Codeflix - Python

## Running

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
python manage.py startconsumer
python manage.py runserver
```

## Git Branch para cada módulo
- [Módulo 2: Entidade Category](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-2-category)
- [Módulo 3: Casos de uso Category](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-3-category-use-cases)
- [Módulo 4: casos de uso Category - pt 2](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-4-category-use-cases-part-2)
- [Módulo 5: Implementando nossa API](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-5-django-api)
- [Módulo 6: Implementando nossa API - pt 2](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-6-django-api-parte-2)
- [Módulo 7: Domain Genre](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-7-genre-domain)
- [Módulo 8: API Genre](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-8-genre-api)
- [Módulo 9: API CastMember](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-9-cast-member)
    - [Desafio: Implementar Domain e API CastMember](https://github.com/gcrsaldanha/codeflix-catalog-admin/blob/main/referencias/Desafio%3A%20API%20CastMember.md)
- [Módulo 10: Refatoração](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-10-refatoracao)
    - [Desafio: Paginação e Refatoração](https://github.com/gcrsaldanha/codeflix-catalog-admin/blob/main/referencias/Desafio%3A%20Pagina%C3%A7%C3%A3o%20e%20Refatora%C3%A7%C3%A3o.md)
- [Módulo 11: Domain Video](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-11-domain-video-completo)
  - [Pull Request](https://github.com/gcrsaldanha/codeflix-catalog-admin/pull/9)
  - [Desafio: Implementar API Video](https://github.com/gcrsaldanha/codeflix-catalog-admin/blob/main/referencias/Desafio%3A%20API%20para%20cria%C3%A7%C3%A3o%20de%20v%C3%ADdeo%20sem%20m%C3%ADdia.md)
- [Módulo 12: Upload de Vídeo](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-12-upload-de-video)
  - [Pull Request](https://github.com/gcrsaldanha/codeflix-catalog-admin/pull/11)
- [Módulo 13: Eventos](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-13-domain-events)
  - [Pull Request](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-13-domain-events)
  - [Desafio: Teste End-to-End](./referencias/Desafio:%20Teste%20end-to-end%20para%20eventos.md)
- [Módulo 14: Autenticação](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-14-keycloak)
  - [Pull Request](https://github.com/gcrsaldanha/codeflix-catalog-admin/pull/14)
  - [Desafio: Gerando token JWT](./referencias/Desafio:%20Gerando%20token%20JWT.md)
