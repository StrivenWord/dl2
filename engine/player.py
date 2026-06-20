"""
Player class
the player character object
"""

from .game_object import GameObject
from .room import Room

class Player(GameObject):
	def __init__(self, name: str = "yourself", description: str = "As good-looking as ever.") -> None:
		super().__init__(name, description)
		self.attributes.update(["animate", "proper"])
		self.location: Room | None = None
		self.max_carried: int = 100  # This is the inventory limit.
	# Check whether player can carry more items.
	def can_carry(self, obj: GameObject) -> bool:
		return len(self.contents) < self.max_carried
	# Recursively format inventory with nested container objects
	def _format_inventory_recursive(self, obj: GameObject, indent: int = 0) -> list[str]:
		lines = []
		for item in obj.contents:
			prefix = " " * (indent + 1)
			lines.append(f"{prefix}{item.name}")
			if item.is_container() and item.is_open() and item.contents:
				lines.extend(self._format_inventory_recursive(item, indent + 1))
		return lines
	# Generate inventory listing with recursive nested contents.
	def inventory_description(self) -> str:
		if not self.contents:
			return "You are empty-handed."
		lines = ["You are carrying:"]
		lines.extend(self._format_inventory_recursive(self))
		return "\n".join(lines)