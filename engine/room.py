"""
Class for 'rooms' -- locations in the game.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Callable

from .game_object import GameObject

class Room(GameObject):
	"""
	Rooms are instatiations of a subclass. Directional pathways are implemented
	using dictionary mappings, effectively creating a graph of the represented
	game world.
	"""
	def __init__(self, name: str, description: str = "") -> None:
		super().__init__(name, description)
		self.exits: dict[str, Room | Callable[[], Room]] = {}
		self.attributes.add("light")  # Rooms are lit by default.
	def add_exit(self, direction: str, destination: Room | Callable[[], Room]) -> None:
		"""
		Add an exit in a given direction.
		Destination can be a Room or a callable that returns a Room
		(for dynamic exits liike in William Tell chapter 8).
		"""
		d = {"n": "north", "s": "south", "e": "east", "w": "west",
			"ne": "northeast", "nw": "northwest",
			"se": "southeast", "sw": "southwest",
			"u": "up", "d": "down", "i": "in"}.get(direction.lower(), direction.lower())
		self.exits[d] = destination
	# Get the room in a given direction.
	def get_exit(self, direction: str) -> Room | None:
		direction = direction.lower()
		direction = {"n": "north", "s": "south", "e": "east", "w": "west",
			"ne": "northeast", "nw": "northwest",
			"se": "southeast", "sw": "southwest",
			"u": "up", "d": "down", "i": "in"}.get(direction, direction)
		if direction not in self.exits:
			return None
		dest = self.exits[direction]
		if callable(dest):
			return dest()
		return dest
	# Get list of available exit directions.
	def get_exit_directions(self) -> list[str]:
		return list(self.exits.keys())
	def __repr__(self) -> str:
		return f"<Room: {self.name}>"
