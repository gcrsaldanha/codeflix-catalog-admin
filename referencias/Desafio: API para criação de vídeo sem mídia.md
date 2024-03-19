# Desafio: Video API

## Objetivo

Implementar a camada de API para o use case `CreateVideoWithoutMedia`.

## Exemplo de Request / Response

Request:

```bash
curl --location 'http://localhost:8000/api/videos' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "title": "title",
    "description": "description",
    "year_launched": 2019,
    "opened": true,
    "rating": "L",
    "duration": 1,
    "categories_id": [
        "1b9d317f-d2e9-4299-9aa8-bfa4ee2ed220"
    ],
    "genres_id": [
        "1d9c7d47-0aac-4dab-a183-2c256ffcae32"
    ],
    "cast_members_id": [
        "aba29a82-2eb7-4638-b65c-06b14ec07299"
    ]
}'
```

Response:

```json
{
    "id": "e7b98989-9a21-4cab-9fd7-bbf0f98924ce"  // ID do video criado
}
```

## Instruções

- Escrever pelo menos 2 testes **end-to-end**
  - Um para o caso de sucesso - video persistido.
  - Um para o caso de falha - qualquer erro (ou múltiplos erros).
- Escrever testes unitários para o *usecase* `CreateVideoWithoutMedia` (caso ainda não o tenha feito)
- Se preferir, utilize como referência o código que implementamos durante a aula: https://github.com/gcrsaldanha/codeflix-catalog-admin/pull/10

Boa sorte e qualquer dúvida, pode perguntar!
