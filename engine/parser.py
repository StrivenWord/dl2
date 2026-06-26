"""
The parser
Draws heavily from the example of structured pattern matching in PEP 636:
	https://peps.python.org/pep-0636/
"""

from __future__ import annotations
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from .game_object import GameObject
	from .player import Player
	from .room import Room

class Parser:
	ARTICLES = {"the", "a", "an", "my", "your"}
	VERB_SYNONYMS = {
		# mapping all the movement commands to "GO"
		"go": "go", "walk": "go", "run": "go", "move": "go", "head": "go",
		# -- directions are included here and then expanded later
		"north": "go", "south": "go", "east": "go", "west": "go",
		"northeast": "go", "southeast": "go", "southwest": "go",
		"ne": "go", "nw": "go", "se": "go", "sw": "go",
		"up": "go", "down": "go", "u": "go", "d": "go",
		"n": "go", "s": "go", "e": "go", "w": "go",
		"enter": "enter", "exit": "exit", "leave": "exit", "out": "exit",
		"take": "take", "get": "take", "pick": "take", "grab": "take",
		"drop": "drop",
		"put": "put", "place": "put", "insert": "put",
		"give": "give", "offer": "give", "feed": "give",
		"open": "open", "close": "close",
		"unlock": "unlock", "lock": "lock",
		"look": "look", "examine": "examine", "x": "examine", "read": "examine",
		"search": "search",
		"listen": "listen", "smell": "smell", "taste": "taste", "touch": "touch",
		"change": "change", "transform": "change",
		"swim": "swim",
		"fly": "fly",
		"pray": "pray",
		"shoot": "shoot", "fire": "shoot", "aim": "shoot",
		"inventory": "inventory", "i": "inventory", "inv": "inventory",
		"quit": "quit", "q": "quit", "restart": "restart",
		"save": "save", "restore": "restore",
		"help": "help", "hint": "hint",
		"turn": "turn",
		"push": "push", "press": "push", "depress": "push",
		"start": "start",
		"throw": "throw", "hurl": "throw", "toss": "throw",
		"light": "light",
		"load": "load",
		"hit": "hit", "strike": "hit", "attack": "hit",
		"ask": "ask",
		"kill": "kill", "slay": "kill",
		"about": "about",
		"score": "score",
		"smell": "smell",
		"salute": "salute",
		"sing": "sing",
	}
	DIRECTIONS = {
		"north": "north", "n": "north",
		"south": "south", "s": "south",
		"east": "east", "e": "east",
		"west": "west", "w": "west",
		"northeast": "northeast", "ne": "northeast",
		"northwest": "northwest", "nw": "northwest",
		"southeast": "southeast", "se": "southeast",
		"southwest": "southwest", "sw": "southwest",
		"up": "up", "u": "up",
		"down": "down", "d": "down",
		"in": "in", "out": "out",
	}
	def __init__(self, player: Player) -> None:
		self.player = player
		self.last_command: str = ""
		self.last_noun: GameObject | None = None
	def parse(self, command_string: str) -> dict | None:
		if not command_string or not command_string.strip():
			return None
		self.last_command = command_string.strip()
		original = self.last_command
		raw = command_string.lower().strip()
		tokens = re.split(r"\s+", raw)
		tokens = [w for w in tokens if w]
		if not tokens:
			return None
		cleaned = [w for w in tokens if w not in self.ARTICLES]
		if not cleaned:
			return None
		if len(cleaned) == 1 and cleaned[0] in self.DIRECTIONS:
			return {
				"action": "go",
				"direction": self.DIRECTIONS[cleaned[0]],
				"noun": None, "second": None,
				"preposition": None, "raw": original,
			}
		raw_verb = cleaned[0]
		verb = self.VERB_SYNONYMS.get(raw_verb, raw_verb)
		rest = cleaned[1:]
		match [verb, *rest]:
			case ["quit"]:
				return { "action": "quit",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["save"]:
				return { "action": "save",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["restore"]:
				return { "action": "restore",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["restart"]:
				return { "action": "restart",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["help"] | ["hint"]:
				return { "action": "help",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["look"]:
				return { "action": "look",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["inventory"]:
				return { "action": "inventory",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["exit"]:
				return { "action": "exit",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["about"]:
				return { "action": "about",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["score"]:
				return { "action": "score",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["smell"]:
				return { "action": "smell",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["listen"]:
				return { "action": "listen",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["taste"]:
				return { "action": "taste",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["touch"]:
				return { "action": "touch",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["salute"]:
				return { "action": "salute",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["sing"]:
				return { "action": "sing",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["pray"]:
				return { "action": "pray",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["swim"]:
				return { "action": "swim",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["fly"]:
				return { "action": "fly",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["change"]:
				return { "action": "change",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["go", direction] if direction in self.DIRECTIONS:
				return { "action": "go",
					"direction": self.DIRECTIONS[direction],
					"noun": None, "second": None,
					"preposition": None, "raw": original }
			case ["go"]:
				return { "action": "go",
					"direction": None,
					"noun": None, "second": None,
					"preposition": None, "raw": original }
			case ["examine", noun]:
				return { "action": "examine",
					"noun": noun, "second": None,
					"direction": None, "preposition": None,
					"raw": original }
			case ["examine"]:
				return { "action": "examine",
					"noun": None, "second": None,
					"direction": None, "preposition": None,
					"raw": original }
			case ["take", noun]:
				return { "action": "take",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["take", "up", noun]:
				return { "action": "take",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["take", noun, "up"]:
				return { "action": "take",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["drop", noun]:
				return { "action": "drop",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["drop", *objects]:
				return { "action": "drop",
					"noun": " ".join(objects) if objects else None,
					"second": None, "preposition": None,
					"direction": None, "raw": original }
			case ["open", noun]:
				return { "action": "open",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["close", noun]:
				return { "action": "close",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["lock", noun, "with", second]:
				return { "action": "lock",
					"noun": noun, "second": second,
					"preposition": "with", "direction": None,
					"raw": original }
			case ["lock", noun]:
				return { "action": "lock",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["unlock", noun, "with", second]:
				return { "action": "unlock",
					"noun": noun, "second": second,
					"preposition": "with", "direction": None,
					"raw": original }
			case ["unlock", noun]:
				return { "action": "unlock",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["put", noun, ("in" | "into" | "on" | "onto") as prep, second]:
				return { "action": "put",
					"noun": noun, "second": second,
					"preposition": prep, "direction": None,
					"raw": original }
			case ["put", noun]:
				return { "action": "put",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["give", noun, "to", second]:
				return { "action": "give",
					"noun": noun, "second": second,
					"preposition": "to", "direction": None,
					"raw": original }
			case ["give", noun]:
				return { "action": "give",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["shoot", noun, "with", second]:
				return { "action": "shoot",
					"noun": noun, "second": second,
					"preposition": "with", "direction": None,
					"raw": original }
			case ["shoot", noun]:
				return { "action": "shoot",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["enter", noun]:
				return { "action": "enter",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["search", noun]:
				return { "action": "search",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["listen", noun]:
				return { "action": "listen",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["smell", noun]:
				return { "action": "smell",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["taste", noun]:
				return { "action": "taste",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["touch", noun]:
				return { "action": "touch",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["turn", noun]:
				return { "action": "turn",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["push", noun]:
				return { "action": "push",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["start", noun]:
				return { "action": "start",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["start"]:
				return { "action": "start",
					"noun": None, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["throw", noun, ("at" | "on") as prep, second]:
				return { "action": "throw",
					"noun": noun, "second": second,
					"preposition": prep, "direction": None,
					"raw": original }
			case ["throw", noun]:
				return { "action": "throw",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["light", noun, "with", second]:
				return { "action": "light",
					"noun": noun, "second": second,
					"preposition": "with", "direction": None,
					"raw": original }
			case ["light", noun]:
				return { "action": "light",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["load", noun, ("in" | "into" | "on") as prep, second]:
				return { "action": "load",
					"noun": noun, "second": second,
					"preposition": prep, "direction": None,
					"raw": original }
			case ["load", noun]:
				return { "action": "load",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["hit", noun, "with", second]:
				return { "action": "hit",
					"noun": noun, "second": second,
					"preposition": "with", "direction": None,
					"raw": original }
			case ["hit", noun]:
				return { "action": "hit",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["ask", noun, "about", second]:
				return { "action": "ask",
					"noun": noun, "second": second,
					"preposition": "about", "direction": None,
					"raw": original }
			case ["ask", noun]:
				return { "action": "ask",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case ["kill", noun, "with", second]:
				return { "action": "kill",
					"noun": noun, "second": second,
					"preposition": "with", "direction": None,
					"raw": original }
			case ["kill", noun]:
				return { "action": "kill",
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case [action, ("at" | "to" | "on" | "in" | "with" | "into" | "onto" | "for" | "about") as preposition, noun]:
				return { "action": action,
					"noun": noun, "second": None,
					"preposition": preposition, "direction": None,
					"raw": original }
			case [action, noun, preposition, second]:
				return { "action": action,
					"noun": noun, "second": second,
					"preposition": preposition, "direction": None,
					"raw": original }
			case [action, noun]:
				return { "action": action,
					"noun": noun, "second": None,
					"preposition": None, "direction": None,
					"raw": original }
			case [action, *rest_words]:
				return { "action": action,
					"noun": " ".join(rest_words) if rest_words else None,
					"second": None, "preposition": None,
					"direction": None, "raw": original }
			case _:
				return None
	def resolve_noun(self, noun_string: str, scope: list[GameObject]) -> GameObject | str | None:
		if not noun_string:
			return None
		noun_lower = noun_string.lower()
		if noun_lower in ("it", "him", "her", "them"):
			if self.last_noun:
				return self.last_noun
			print("You can't refer to something that isn't here.")
			return None
		matches: list[tuple[GameObject, int]] = []
		for obj in scope:
			if noun_lower == obj.name.lower():
				matches.append((obj, 2))
			elif any(noun_lower == alias.lower() for alias in obj.aliases):
				matches.append((obj, 2))
			elif any(noun_lower in alias.lower() for alias in obj.aliases):
				matches.append((obj, 1))
			elif noun_lower in obj.name.lower():
				matches.append((obj, 1))
		if not matches:
			return None
		matches.sort(key=lambda x: x[1], reverse=True)
		if len(matches) > 1 and matches[0][1] == matches[1][1]:
			names = ", ".join(f"the {m[0].name}" for m in matches[:3])
			return "AMBIGUOUS"
		self.last_noun = matches[0][0]
		return matches[0][0]
	def _collect_scope_recursive(self, obj: GameObject, scope: list[GameObject]) -> None:
		for child in obj.contents:
			scope.append(child)
			if child.is_container() and child.is_open():
				self._collect_scope_recursive(child, scope)
	def get_scope(self) -> list[GameObject]:
		scope = []
		if self.player.location:
			scope.append(self.player.location)
			self._collect_scope_recursive(self.player.location, scope)
			scope.extend(self.player.contents)
			for item in self.player.contents:
				if item.is_container() and item.is_open():
					self._collect_scope_recursive(item, scope)
		return scope
