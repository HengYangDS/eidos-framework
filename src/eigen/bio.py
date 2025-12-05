from .core import Operator
from typing import Any, Callable, Type

class Genome(Operator):
    """
    The fundamental unit of biological information.
    """
    def mutate(self):
        pass

class PetriDish(Operator):
    """
    An environment for evolution.
    """
    def __init__(self, species: Type[Genome], fitness: Callable[[Any], float]):
        self.species = species
        self.fitness = fitness
        
    async def evolve(self, generations: int = 100) -> Any:
        # Mock evolution
        best = self.species()
        return best

    async def __call__(self, input: Any) -> Any:
        return await self.evolve()
