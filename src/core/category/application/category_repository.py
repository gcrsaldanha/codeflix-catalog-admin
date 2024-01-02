from abc import ABC, abstractmethod


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category):
        raise NotImplementedError
