"""World - the central game state and main game loop."""

from __future__ import annotations
from typing import Callable
import sys

from .player import Player
from .parser import Parser
from .actions import ActionProcessor

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
		self.score = 0
		self.max_score = 0

	def set_win_condition(self, condition: Callable, message: str = "You have won!") -> None:
		self.win_condition = condition
		self.win_message = message

	def add_daemon(self, daemon_func: Callable) -> None:
		self.active_daemons.append(daemon_func)

	def remove_daemon(self, daemon_func: Callable) -> None:
		if daemon_func in self.active_daemons:
			self.active_daemons.remove(daemon_func)

	def start(self, start_room) -> None:
		self.current_room = start_room
		self.player.place(start_room)
		self.running = True
		self.restart_requested = False
		self.turn_count = 0

	def show_score(self) -> None:
		print(f"You have so far scored {self.score} out of a possible {self.max_score}, in {self.turn_count} turns.", end="")
		if self.score == 0:
			print(" You are lost and confused.")
		elif self.score == self.max_score:
			print(" You have earned the rank of demon-slayer!")
		elif self.score >= self.max_score * 0.75:
			print(" You are becoming innovative.")
		elif self.score >= self.max_score * 0.5:
			print(" You are a competent adventurer.")
		else:
			print(" You are lost and confused.")

	def show_about(self) -> None:
		print("Dreary Lands")
		print("A short work of interactive fiction.")
		print("Copyright 2005 by Paul Lee.")
		print("Python re-creation by Strivenword.")

	def run(self) -> None:
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
			if parsed["action"] == "go" and parsed.get("direction"):
				self.actions._last_direction = parsed["direction"]
			self.actions.process(parsed)
			self.actions._last_direction = None
			for daemon_func in self.active_daemons:
				daemon_func()
			if self.win_condition():
				print(f"\n{self.win_message}")
				break
			if self.restart_requested:
				break

	def debug_tree(self, obj=None, indent: int = 0) -> None:
		if obj is None:
			obj = self.current_room
		print(" " * indent + obj.name)
		for child in obj.contents:
			self.debug_tree(child, indent + 1)

	def debug_scope(self) -> None:
		scope = self.parser.get_scope()
		print("Current scope:")
		for obj in scope:
			print(f" {obj.name} ({type(obj).__name__})")
			if obj.attributes:
				print(f"    attributes: {obj.attributes}")
