# Desafio: API CastMember

## Objetivo
O objetivo deste desafio é implementar uma aplicação Django que gerencie membros de elenco de filmes ou séries, conhecidos como `CastMembers`.
Você deverá implementar a entidade `CastMember`, os casos de uso associados e as APIs correspondentes.

## Entidade: CastMember

Na camada de domínio, a entidade `CastMember` representa um membro do elenco e possui os seguintes atributos:

- **id**: UUID - Identificador único para cada `CastMember`.
- **name**: String - Nome do membro do elenco.
- **type**: Enum (ACTOR | DIRECTOR) - Tipo do membro do elenco, podendo ser ATOR ou DIRETOR.

**Regras de Negócio:**

- Todos os atributos são obrigatórios.
- O atributo `type` deve aceitar apenas os valores "ACTOR" ou "DIRECTOR". Recomenda-se o uso do `StrEnum` do Python 3.11 para esta finalidade.

## Application Layer: Casos de Uso

Você deve implementar os seguintes casos de uso na camada de aplicação:

1. **Listar `cast_members` cadastrados**
2. **Cadastrar um novo `cast_member`**
  - Deve validar os campos `name` e `type`
3. **Editar um `cast_member` cadastrado** (fornecendo `name` e `type`)
  - Deve validar se o `cast_member` com o `id` fornecido existe
  - Deve validar os campos `name` e `type`
4. **Deletar um `cast_member` cadastrado** (através do `id` - UUID)
  - Deve validar se o `cast_member` com o `id` fornecido existe

## API

A camada de API deve expor endpoints para cada caso de uso descrito acima:

### Listar Cast Members
```
GET /api/cast_members/
HTTP 200
```

Response:
```json
{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "type": "ACTOR"
    },
    {
      "id": "123e4567-e89b-12d3-a456-426614174001",
      "name": "Jane Doe",
      "type": "DIRECTOR"
    }
  ]
}
```

### Cadastrar Cast Member

- Deve validar se os campos `name` e `type` passados são válidos. Caso contrário, retorna HTTP 400.

```
POST /api/cast_members/
HTTP 201
```

Payload:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Jane Doe",
  "type": "ACTOR"
}
```

### Editar Cast Member

- Valida se a entidade com `pk` existe. Se não existir, retorna HTTP 404.
- Valida se os campos `name` e `type` passados são válidos. Caso contrário, retorna HTTP 400.

```
PUT /api/cast_members/123e4567-e89b-12d3-a456-426614174000/
Response HTTP 204
```

### Deletar Cast Member

- Valida se a entidade com `pk` existe. Se não existir, retorna HTTP 404.

```
DELETE /api/cast_members/123e4567-e89b-12d3-a456-426614174000/
Response HTTP 204
```

## Orientações Gerais

- Escreva testes unitários e de integração para a entidade e casos de uso.
- Escreva testes de integração para as APIs.
- Escreva pelo menos um teste end-to-end interagindo com múltiplos endpoints da API.
- Utilize como base a [git branch do Módulo 8](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-8-genre-api)


## Serializando um Enum

Na camada de API, vamos precisar fazer a conversão do `"ACTOR"` para o `enum` que utilizarmos, por exemplo, `CastMemberType.ACTOR`.

Para fazer isso, podemos ou fazer a conversão na `view`, mas o ideal seria utilizarmos os `serializers`, assim como fizemos com o `SetField`.

Aqui está uma sugestão de implementação de um `Field` para serializar o `enum CastMember`:

```python
class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        # Utilizamos o "choices" do DRF, que permite um conjunto de opções limitado para um certo campo.
        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        # Valor vindo da API como "str" é convertido para o StrEnum
        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        # O valor vindo do nosso domínio é convertido para uma string na API
        return str(super().to_representation(value))
```
