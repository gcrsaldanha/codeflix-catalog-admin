# Módulo 7 - Genre Domain

## Aula 1: Introdução

### Genre: Atributos
- id
- name
- is_active
- categories: Set[UUID]

> Categoria **tem um gênero**. Gênero **tem várias categorias**. Não vamos nos preocupar com o **banco** agora! Vamos focar no **domínio**.


### Genre: Métodos
- change_name(name: str)
- add_category(category_id: UUID)
- remove_category(category_id: UUID)
- activate()
- deactivate()


### Genre: Casos de uso
- Criar gênero com categorias
  - Se a categoria não existir, retorna um erro
  - Pode criar um Genre **sem** categoria
- Listar gêneros
  - Retorna listagem de generos com ID de categorias associadas
- Remover gênero
- Atualizar gênero (PUT)


## Aula 2 - Implementando o Domain Genre
- Copiar Category domain e atualizar para Genre
  - Gêneros: "Romance", "Drama", "Suspense", etc.
- Atualizar testes (alguns, não todos)
- Escrever os testes para add_category/remove_category
- Exercício: atualizar os outros testes unitários


## Aula 3 - Caso de uso: Criar Gênero
- Unit tests apenas
  - test_when_provided_categories_do_not_exist_then_raise_related_categories_not_found
  - test_when_created_genre_is_invalid_then_raise_invalid_genre
  - test_when_created_genre_is_valid_and_categories_exist_then_save_genre
  - test_create_genre_without_categories
- Spec do repositorio
- UseCase depende de 2 repositórios: Genre e Category
- Utilizar Input/Output como classes internas do CreateGenre


# Aula 4 - InMemoryGenreRepository
- Simplesmente copiar e atualizar os métodos do InMemoryCategoryRepository
- O repositório do Django vai ter algumas peculiaridades


## Aula 5 - Teste de integração: Criar Gênero
- test_create_genre_with_associated_categories
- test_create_genre_with_inexistent_categories_raise_an_error
- Exercício: test_create_genre_without_categories


## Aula 6 - Caso de uso: Listar Gêneros
- test_list_genres_with_associated_categories
  - 2 genres, 1 com categorias, outro sem
- Não precisamos do CategoryRepository para a listagem (apenas para os testes de integração)
- Exercício: escrever os testes unitários
  - Mesmo casos que de integração, mas utilizando o create_autospec
  - Adicionar caso de listagem para quando não tem gêneros cadastrados


## Aula 7 - Caso de uso: Deletar Gênero
- Copiar DeleteCategory use case
- Fazer os testes unitários
- test_delete_genre_from_repository
- test_when_genre_does_not_exist_then_raise_error
- Regex para assertion: `match="Genre with id .* not found"`
- Exercício: escrever testes de integração


## Aula 8 - Desafio - Caso de uso: Atualizar Gênero
Desafio: implementar o caso de uso de atualizar gênero

Os atributos passados devem substituir **totalmente** os atributos da entidade (comportamento similar ao PUT e não ao PATCH).

Casos de teste (pode escolher fazer mais unitários e apenas o "happy path" de integração):
- Atualizar um Genre que não existe deve retornar um GenreNotFound Exception
- Atualizar um Genre passando atributos inválidos deve retonar uma InvalidGenre Exception
- Atualizar um Genre com categorias que não existem deve retornar um RelatedCategoriesNotFound Exception
- Atualizar um Genre com categorias que existem deve atualizar o Genre corretamente
  - Lembrando que vamos atualizar o Genre **totalmente**. Se ele tinha 3 categorias e passamos 2, ele deve ficar com 2 categorias.
  - Incluir atributos como "name" e "is_active" no teste
