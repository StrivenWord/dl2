"""World - the central game state and main game loop."""

from __future__ import annotations
from typing import Callable
import sys

class World:
	"""Universal state object."""
	def __init__(self, player: Player | None = None) -> None:
		self.player = player or Player()
		self.current_room = None
		self.parser = Parser(self.player)
		self.actions = ActionProcessor(self)
		self.running = True
		self.restart_requested = False
		self.active_daemons: list[Callable] = []
		self.win_condition = lambda: False
		self.win_message = "*** You have won! ***"
		self.turn_count = 0
	def set_win_condition(self, condition: Callable, message: str = "You have win_condition") -> None:
		self.win_condition = condition
		self.win_message = message
	def add_daemon(self, daemon_func: Callable) -> None:
		self.active_daemons.append(daemon_func)
	def remove_daemon(self, daemon_func: Callable) -> None:
		if daemon_func in self.active_daemons:
			self.active_daemons.remove(daemon_func)
	def start(self, start_room) -> None:
		self.current_room = start_room
		self.player.location = start_room
		self.running = True
		self.restart_requested = False
		self.turn_count = 0
	def run(self) -> None:  # Main game loop
		self.actions.action_look(self.player)
		while self.running:
			self.turn_count += 1
			try:
				raw = input("\n> ")
			except (EOFError, KeyboardInterrupt):
				print("")
				break
			if not raw.strip():
				continue
			parsed = self.parser.parse(raw)
			if parsed is None:
				continue
			# GO action
			if parsed["action"] == "go" and parsed.get("direction"):
				self.actions._last_direction = parsed["direction"]
			# Process the action
			self.actions.process(parsed)
			# Clear last direction
			self.actions._last_direction = None
			# Execute daemons after player action
			for daemon_func in self.active_daemons:
				daemon_func()
			# Check win condition
			if self.win_condition():
				print(f"\n{self.win_message}")
				break
			# Check for restart
			if self.restart_requested
				break
	# debugger
	# replicating Inform's TREE debugging verb
	def debug_tree(self, obj=None, indent: int=0) -> None:
		if obj is None:
			obj = self.current_room
		print(" " * indent + obj.name)
		for child in obj.contents:
			self.debug_tree(child, indent + 1)
	# list all objects in scope
	def debug_scope(self) -> None:
		score = self.parser.get_scope()
		print("Current scope:")
		for obj in scope:
			print(f" {obj.name} ({type(obj).__name__})")
			if obj.attributes:
				print(f"    attributes: {obj.attributes}")