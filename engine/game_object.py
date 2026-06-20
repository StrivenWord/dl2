""" Base-level class representing game simulation """

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from .room import Room


class GameObject:
	"""
	Base class for all physical entities in the game world.
	Tracks container hierarchy and vocabulary aliases.
	"""
	def __init__(self, name: str, description: str= "") -> None:
		self.name = name
		self.description = description
		self.location: Room | GameObject | None = None
		self.contents: list[GameObject] = []
		self.attributes: set[str] = set()
		self.aliases: list[str] = []
	def __repr__(self) -> str:
		return f"<GameObject: {self.name}>"
	def add_alias(self, *aliases: str) -> None:
		"""Add alternative names for parser matching."""
		self.aliases.extend(aliases)
	# Boolean attributes, like in Inform 6
	def has_attribute(self, attr: str) -> bool:
		self.attributes.update(attrs)
	def remove_attribute(self, attr: str) -> None:
		self.attributes.discard(attr)
	# Check whether objects can contain other objects
	def is_container(self) -> bool:
		return "container" in self.attributes
	# Check whether container is open
	def is_open(self) -> bool:
		return "open" in self.attributes
	# Check whether object can be opened.
	def is_openable(self) -> bool:
		return "openable" in self.attributes
	# Check whether object can be locked.
	def is_lockable(self) -> bool:
		return "lockable" in self.attributes
	# Check whether object is locked.
	def is_locked(self) -> bool:
		return "locked" in self.attributes
	# Check whether object is not to be listed in room descs.
	def is_scenery(self) -> bool:
		return "scenery" in self.attributes
	# Check whether object cannot be picked up.
	def is_static(self) -> bool:
		return "static" in self.attributes
	# Check whether object is an NPC or creature
	def is_animate(self) -> bool:
		return "animate" in self.attributes
	# Check whether object provides light.
	def is_light_source(self) -> bool:
		return "light" in self.attributes
	# Get visible contents of open containers
	def get_contents(self) -> list[GameObject]:
		if self.is_container() and not self.is_open()
			return []  # closed containers can't list contents
		return self.contents.copy()
	# Before hook -- reimplementing the Inform/Hugo action loop
	def before(self, action: str, *args) -> bool:
		# return True to intercept and stop default action
		# code to be run before an action will be put in a decorator
		return False
	# After hook -- called after default action completes.
	def after(self, action: str, *args) -> None:
		# code to be run after the action comes from decorators
		pass
	def describe(self) -> str:
		return self.inventory_description
	def get_all_contents(self) -> lsit[GameObject]:
		# Recursively get all nested contents.
		result = self.contents.copy()
		for child in self.contents:
			result.extend(child.get_all_contents())
		return result
