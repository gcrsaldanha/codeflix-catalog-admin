# Desafio: Paginação e Refatoração

No módulo 10 vimos como adicionar paginação à nossa API de Category.


## Parte 1: Adicionando paginação aos outros domínios

A primeira parte do desafio é implementar a paginação correta para os outros 3 domínios, seguindo o seguinte contrato de API:

Request:
```
GET /categories/?current_page=1
```

Response:
```json
{
    "data": [...],
    "meta": {
        "current_page": 1,
        "per_page": N,
        "total": M
    }
}
```
Onde `N` e `M` são valores que você pode definir.

Como referência, utilize-os seguintes commits:

- [Adiciona serialização à camada de aplicação](https://github.com/gcrsaldanha/codeflix-catalog-admin/commit/c77fc1e224cc8c17c5cf69d3168fbd10fc12617f#diff-fd06040ea71dc7ea28fe4c569704ef7bed2f6154b3ba485590c4cacafada0630)
- [Adiciona serialização da paginação à API](https://github.com/gcrsaldanha/codeflix-catalog-admin/commit/88e5bfa5594cfba7a0bd09f144de088a6d394eb5)


## Parte 2: Refatoração/Abstração

Você deve ter percebido que a **listagem** é uma operação muito parecido entre os diferentes domínios.

Tente abstrair e diminuir a duplicação de código para a listagem de entidades, tanto para a camada de aplicação quanto para a API (Views/Serializers).
