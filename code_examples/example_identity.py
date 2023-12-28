from src.core.category.domain.category import Category


category_1 = Category(name="Filme", description="Filmes em geral")
category_2 = Category(name="Série", description="Séries em geral")
category_3 = Category(name="Filme", description="Filmes em geral")

print(category_1 == category_2)
print(category_1 == category_3)


# category_1.__eq__(category_2)
