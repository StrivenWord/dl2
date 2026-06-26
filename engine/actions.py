"""
Action processing system.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Callable

from .game_object import GameObject
from .player import Player

if TYPE_CHECKING:
	from .room import Room
	from .world import World

class ActionProcessor:
	"""
	Central action dispatch system.
	Before/after hooks
	"""
	def __init__(self, world: World) -> None:
		self.world = world
		self.standard_actions: dict[str, Callable] = {}
		self.default_responses: dict[str, str] = {}
		self._register_actions()

	def _register_actions(self) -> None:
		self.standard_actions = {
			"look": self.action_look,
			"examine": self.action_examine,
			"take": self.action_take,
			"drop": self.action_drop,
			"go": self.action_go,
			"enter": self.action_enter,
			"exit": self.action_exit,
			"inventory": self.action_inventory,
			"open": self.action_open,
			"close": self.action_close,
			"search": self.action_search,
			"listen": self.action_listen,
			"smell": self.action_smell,
			"taste": self.action_taste,
			"touch": self.action_touch,
			"put": self.action_put,
			"give": self.action_give,
			"unlock": self.action_unlock,
			"lock": self.action_lock,
			"help": self.action_help,
			"quit": self.action_quit,
			"restart": self.action_quit,
			"salute": self.action_salute,
			"turn": self.action_turn,
			"push": self.action_push,
			"start": self.action_start,
			"throw": self.action_throw,
			"light": self.action_light,
			"load": self.action_load,
			"shoot": self.action_shoot,
			"hit": self.action_hit,
			"ask": self.action_ask,
			"kill": self.action_kill,
			"about": self.action_about,
			"score": self.action_score,
		}
		self.default_responses = {
			"sing": "You sing.",
			"pray": "You pray.",
			"swim": "You can't swim here.",
			"fly": "You can't fly here.",
			"change": "You are changed.",
		}

	def register_action(self, verb: str, handler: Callable) -> None:
		self.standard_actions[verb] = handler

	def register_default_response(self, verb: str, response: str) -> None:
		self.default_responses[verb] = response

	def process(self, parsed: dict) -> None:
		action = parsed["action"]
		noun = parsed.get("noun")
		second = parsed.get("second")
		direction = parsed.get("direction")
		preposition = parsed.get("preposition")
		player = self.world.player
		target = None
		second_target = None
		if noun:
			scope = self.world.parser.get_scope()
			target = self.world.parser.resolve_noun(noun, scope)
			if target == "AMBIGUOUS":
				print("I don't understand which object you mean.")
				return
		if second:
			scope = self.world.parser.get_scope()
			second_target = self.world.parser.resolve_noun(second, scope)
			if second_target == "AMBIGUOUS":
				print("I don't understand which objects you mean.")
				return
			if target is not None and second_target is not None and not isinstance(target, str) and not isinstance(second_target, str):
				self.world.parser.last_noun = target
		if target and hasattr(target, "before") and target is not player:
			try:
				result = target.before(action, player, target, second_target)
				if result:
					return
			except TypeError:
				result = target.before(action)
				if result:
					return
		room = player.location
		if room and hasattr(room, "before"):
			try:
				result = room.before(action, player, target, second_target)
				if result:
					return
			except TypeError:
				result = room.before(action)
				if result:
					return
		if action in self.standard_actions:
			self.standard_actions[action](player, target, second_target)
		else:
			self.default_fallback(action)
			return
		if target and hasattr(target, "after") and target is not player:
			try:
				target.after(action, player, target, second_target)
			except TypeError:
				target.after(action)
		if room and hasattr(room, "after"):
			try:
				room.after(action, player, target, second_target)
			except TypeError:
				room.after(action)

	def default_fallback(self, action: str) -> None:
		if action in self.default_responses:
			print(self.default_responses[action])
		else:
			print("That's not something you need to do.")

	def move_object(self, obj: GameObject, new_parent: GameObject | None) -> None:
		if obj.location:
			obj.location.contents.remove(obj)
		obj.location = new_parent
		if new_parent:
			new_parent.contents.append(obj)

	def _has_light_recursive(self, obj: GameObject) -> bool:
		if "light" in obj.attributes:
			return True
		for child in obj.contents:
			if child.is_container() and not child.is_open():
				continue
			if self._has_light_recursive(child):
				return True
		return False

	def action_look(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		room = player.location
		if not room:
			print("You are in a void.")
			return
		has_light = self._has_light_recursive(room)
		if not has_light:
			print("It is pitch dark, and you can't see a thing.")
			return
		print("")
		print(room.name)
		print(room.description)
		exits = room.get_exit_directions()
		if exits:
			print(f"Visible exits: {', '.join(sorted(exits, key=lambda d: d.lower()))}")
		for obj in room.contents:
			if obj is not player and "scenery" not in obj.attributes:
				if "animate" in obj.attributes and "proper" in obj.attributes:
					print(f"{obj.name} is here.")
				else:
					print(f"There is {obj.name} here.")

	def action_examine(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to examine?")
			return
		if target == player:
			print(player.description)
		else:
			print(target.describe())

	def action_take(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to take?")
			return
		if "static" in target.attributes:
			print(f"The {target.name} is too heavy to move.")
			return
		if not player.can_carry(target):
			print("You can't carry any more.")
			return
		self.move_object(target, player)
		print("Taken.")

	def action_drop(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to drop?")
			return
		if target.location is not player and target not in player.contents:
			print(f"You don't have the {target.name}.")
			return
		self.move_object(target, player.location)
		print("Dropped.")

	def action_go(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		room = player.location
		if not room:
			return
		direction = getattr(self, '_last_direction', None)
		if not direction:
			print("Which direction?")
			return
		dest = room.get_exit(direction)
		if dest is None:
			if direction in room.exits:
				return
			print("You can't go that way.")
			return
		player.place(dest)
		self.world.current_room = dest
		self.action_look(player)

	def action_enter(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("You can't enter that.")

	def action_exit(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		room = player.location
		if room and "out" in room.exits:
			dest = room.get_exit("out")
			if dest:
				player.place(dest)
				self.world.current_room = dest
				self.action_look(player)
				return
		print("You can't go that way.")

	def action_inventory(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print(player.inventory_description())

	def action_open(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to open?")
			return
		if "openable" not in target.attributes:
			print(f"You can't open the {target.name}.")
			return
		if "open" in target.attributes:
			print(f"The {target.name} is already open.")
			return
		if "locked" in target.attributes:
			print(f"The {target.name} is locked.")
			return
		target.attributes.add("open")
		print(f"You open the {target.name}.")

	def action_close(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to close?")
			return
		if "openable" not in target.attributes:
			print(f"You can't close the {target.name}.")
			return
		if "open" not in target.attributes:
			print(f"The {target.name} is already closed.")
			return
		target.attributes.discard("open")
		print(f"You close the {target.name}.")

	def _search_recursive(self, obj: GameObject, indent: int = 0) -> list[str]:
		lines = []
		for item in obj.contents:
			prefix = " " * (indent + 1)
			lines.append(f"{prefix}{item.name}")
			if item.is_container() and item.is_open() and item.contents:
				lines.extend(self._search_recursive(item, indent + 1))
		return lines

	def action_search(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to search?")
			return
		if "container" not in target.attributes and "supporter" not in target.attributes:
			print(f"Searching the {target.name} reveals nothing unusual.")
			return
		contents = self._search_recursive(target)
		if not contents:
			print(f"The {target.name} contains nothing.")
		else:
			print(f"The {target.name} contains:")
			for line in contents:
				print(line)

	def action_listen(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if target:
			print(f"You hear nothing unexpected from the {target.name}.")
		else:
			print("You hear nothing unexpected.")

	def action_smell(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("You smell nothing out of the ordinary.")

	def action_taste(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("That doesn't appeal to you.")

	def action_touch(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("You feel nothing remarkable.")

	def action_put(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to put?")
			return
		if not second:
			print("Where do you want to put it?")
			return
		if target.location is not player:
			print(f"You don't have the {target.name}.")
			return
		if "container" not in second.attributes and "supporter" not in second.attributes:
			print(f"You can't put things on {second.name}.")
			return
		if "container" in second.attributes and "open" not in second.attributes:
			print(f"The {second.name} is closed.")
			return
		self.move_object(target, second)
		print(f"You put the {target.name} in the {second.name}.")

	def action_give(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to give?")
			return
		if not second:
			print("To whom?")
			return
		print(f"You offer the {target.name} to {second.name}, but they show no interest.")

	def action_unlock(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to unlock?")
			return
		if "lockable" not in target.attributes:
			print(f"You can't unlock the {target.name}.")
			return
		if "locked" not in target.attributes:
			print(f"The {target.name} is not locked.")
			return
		if second and "key" in second.attributes:
			target.attributes.discard("locked")
			print(f"You unlock the {target.name} with the {second.name}.")
		elif second:
			print(f"You can't unlock the {target.name} with that.")
		else:
			print(f"The {target.name} seems to require a key.")

	def action_lock(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to lock?")
			return
		if "lockable" not in target.attributes:
			print(f"You can't lock the {target.name}.")
			return
		if "locked" in target.attributes:
			print(f"The {target.name} is already locked.")
			return
		if second and "key" in second.attributes:
			target.attributes.add("locked")
			print(f"You lock the {target.name} with the {second.name}.")
		elif second:
			print(f"You can't lock the {target.name} with that.")
		else:
			print(f"The {target.name} seems to require a key.")

	def action_help(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("Interactive Fiction Commands:")
		print("  Movement: north/south/east/west/up/down or n/s/e/w/u/d")
		print("  Objects: take/drop/examine/open/close")
		print("  General: look/inventory/help/quit")

	def action_quit(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("Quitting...")
		self.world.running = False

	def action_restart(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("Restarting...")
		self.world.running = False
		self.world.restart_requested = True

	def action_salute(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("You salute.")

	def action_turn(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to turn?")
			return
		if "turnable" in target.attributes:
			if hasattr(target, "on_turn"):
				target.on_turn(player)
				return
		print(f"You try to turn the {target.name}, but nothing happens.")

	def action_push(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to push?")
			return
		if "pushable" in target.attributes:
			if hasattr(target, "on_push"):
				target.on_push(player)
				return
		print(f"You push the {target.name}, but nothing happens.")

	def action_start(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if target and hasattr(target, "on_start"):
			target.on_start(player)
			return
		print("You can't start that.")

	def action_throw(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to throw?")
			return
		if target.location is not player:
			print(f"You don't have the {target.name}.")
			return
		if hasattr(target, "on_throw"):
			target.on_throw(player, second)
			return
		print(f"You throw the {target.name}, but it just falls to the ground.")

	def action_light(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to light?")
			return
		if target.location is not player:
			print(f"You don't have the {target.name}.")
			return
		if hasattr(target, "on_light"):
			target.on_light(player, second)
			return
		print(f"You can't light the {target.name}.")

	def action_load(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to load?")
			return
		if not second:
			print("What do you want to load it into?")
			return
		if hasattr(second, "on_load"):
			second.on_load(player, target)
			return
		print(f"You can't load the {target.name} into the {second.name}.")

	def action_shoot(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to shoot?")
			return
		if hasattr(target, "on_shoot"):
			target.on_shoot(player, second)
			return
		print(f"You can't shoot the {target.name}.")

	def action_hit(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to hit?")
			return
		if hasattr(target, "on_hit"):
			target.on_hit(player, second)
			return
		print(f"You hit the {target.name}, but nothing happens.")

	def action_ask(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("Who do you want to ask?")
			return
		if hasattr(target, "on_ask"):
			target.on_ask(player, second)
			return
		print(f"You ask {target.name}, but get no response.")

	def action_kill(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		if not target:
			print("What do you want to kill?")
			return
		if hasattr(target, "on_kill"):
			target.on_kill(player, second)
			return
		print(f"You can't kill the {target.name}.")

	def action_about(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		self.world.show_about()

	def action_score(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		self.world.show_score()

	def action_save(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("Save is not implemented yet.")

	def action_restore(self, player: Player, target: GameObject | None = None, second: GameObject | None = None) -> None:
		print("Restore is not implemented yet.")
