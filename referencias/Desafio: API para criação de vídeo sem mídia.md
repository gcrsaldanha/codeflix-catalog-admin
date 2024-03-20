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
- Se preferir, utilize como referência o Pull Request adicionando o que abordamos nesse módulo: https://github.com/gcrsaldanha/codeflix-catalog-admin/pull/9

Boa sorte e qualquer dúvida, pode perguntar!


## Correção: Uso de ValueObjects no projeto

> O `ValueObject` **não** deve possuir um `id`. Ele é identificado unicamente por seus valores.

Durante a implementaçãm em aula, adicionei um `id` aos nosso `ValueObjects`, comentando que esse `id` seria utilizado para a persistência no banco de dados.

Porém, isso é um erro **clássico** de `DDD` onde nos guiamos pelo nosso **banco de dados** ao invés do **domínio**. Ou seja, eu inverti o fluxo de dependência e fiz meu *domain model* depender do meu *database model*. No pull request acima, isso está corrigido.

Observe que ao contrário de outras entidades, cuja referência é feita por um `UUID`, os nossos `ValueObjects` são referenciaods *diretamente* pela nossa entidade (e.g.: `video.video = AudioVideoMedia(...)`). Isso é uma das características de um `ValueObject` e reforça a importância dele ser **imutável** - tanto por questões de design quanto de performance.
