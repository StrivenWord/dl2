"""
Dreary Lands - game content definition.
Based on the Z-code game "Dreary Lands" by Paul Lee (2005).
"""

from engine.game_object import GameObject
from engine.room import Room
from engine.player import Player
from engine.world import World


BUILTIN_KEYS = {"the", "a", "an", "my", "your"}


def _strip_articles(name: str) -> str:
	words = name.split()
	cleaned = [w for w in words if w.lower() not in BUILTIN_KEYS]
	return " ".join(cleaned) if cleaned else name


def _make_name(name: str) -> str:
	return _strip_articles(name)


def build_world() -> World:
	world = World()
	world.max_score = 8

	player = world.player
	player.max_carried = 100

	# ─── ROOMS ────────────────────────────────────────────────

	chamber = Room(
		"In a Small, Cramped Chamber",
		"You are in a small chamber, approximately three feet wide and six tall, allowing you barely any room. Oddly, the walls are a bright blue color, while the ceiling is a colorful shade of orange and the floor a sunny yellow.",
	)
	chamber.aliases = ["chamber"]

	car_interior = Room(
		"In a Wierd Oblong Room",
		"You've just fallen from the room above through the roof of a hot pink-colored convertable. The area is more roomy than before, but not by much.",
	)
	car_interior.aliases = ["oblong room"]

	field = Room(
		"In a Perfectly Silent Field",
		"You only hear a tremendous whine, like the sound of a dolphin magnified infinitely. You only see blackness with shining stars of white. You only feel tremendous pain all over your body. You have crashed. But you're still alive...",
	)

	valley = Room(
		"In a Sunken Valley Before a Marsh",
		"You are in a short depression between two large hills. The ease in which you crossed the field is nonexistent here, for a vast swamp lies northward, extending almost to the end of sight east and west, stopping maybe half a mile to the north, drowning the foot of a hill higher than the one you had to cross to get here, which hides the yonder castle from view.",
	)

	swamp = Room(
		"Standing Waist Deep in a Dark, Putrid Swamp",
		"The swamp encompasses you, the heavy water making your way difficult. The air here is very repugnant, making your lungs heavy and your head dizzy. Insects of all unholy varieties swarm you, biting your flesh. You could retreat back southward, where the swamp shallows and eventually gives way to land, but to make progress you're going to have to brave the northern way, where the far shore is still quite a distance, and the evil water thicker and potentially even deeper.",
	)

	swamp_north = Room(
		"Near the North End of the Swamp",
		"Having traversed the harsh mass of the swamp, the stagnant waters -- now little more than knee-deep -- shallow into a marshy plain a distance northward, which lies in the shadow of the great hill.",
	)

	hill = Room(
		"On the Top of a Tall Hill",
		"Wind rustles around you here at the top of the hill, a barren place of briars and dried grasses. The castle does not stand on this hill; instead it stands on a smaller one a little way south, which begins at the very foot of this one. The briars become dense and impenetrable to the east and the west, but an unkempt stone road slices this area in to north and south sectors and runs through the briars on both sides; to the east the briars have grown and choked out the road, which is soon lost in that direction, but to the west the path is still perhaps usable, and descends a little into scrubland. Far to the south you can see the great wall, extending infinitely horizontally and upwards.",
	)

	gate_room = Room(
		"Before the Castle Gate",
		"A high arching gate of pure white marble rises before you, overlooking squalid vegetation much the same as is found elsewhere in this dreary land. The castle is set back behind an encircling stone wall several yards from the gate, and a small beaten path beside the gate leads eastward into a mud-brick hut.",
	)

	hut = Room(
		"Inside a Small, Mud-brick Hut",
		"This small hut has one encompassing circular wall and is doorless; the exit to the west is just a rectangular space clear of bricks from the dirt floor to the ceiling. Taking up most of this room is a wooden weapons rack. Perhaps this hut is (or was) used as an armory or some such.",
	)

	clearing = Room(
		"In a Hillside Clearing",
		"This little clearing is a rough circle or oval free from the thick thorn bushes which encompass it. Beyond the clearing, which is only about ten yards from side to side, trees begin to rise above the briars, suggesting a forest, the first you've encountered in these wide lands.",
	)

	courtyard = Room(
		"Before the Castle Gate",
		"The great gate now stands open before you, leading into a courtyard.",
	)

	foyer = Room(
		"Inside of the Foyer of a Large Castle",
		"You are in the entranceway of the castle; a stone arch leads south to the courtyard. This room is not sparsely furnished -- it is completely barren. The walls, floor, and ceiling are all of plain, drab granite. A few featureless, pane-less windows let in dismal grey light. Hallways lead in several directions, and a large twisting staircase winds its way upward just north of here. The demeanor of this empty, dreary place chills you; however, and you find yourself somehow uneager to explore the rest of the castle.",
	)

	dark_chamber = Room(
		"In a Dark, Cramped Chamber",
		"You have no recollection of landing, yet you are in a very small area where all is veiled in blackness. This area is very cramped, almost boxlike: your head is propped painfully against a ceiling; your bent knees against a hard floor; your shoulders packed between two walls. You neither know nor care where or what this place is; all you know is that you must get out! MUST GET OUT!!",
	)

	museum = Room(
		"In the Foyer of a Museum",
		"This large room contains some displays placed to put the museum-goer in the mood for ancient artifacts and the like. The floor is of a checkered black-and-white tile pattern, and several corridors of like flooring leave to the rest of the museum. A door to the south will allow you access to the outside world!",
	)

	# ─── EXITS ────────────────────────────────────────────────

	chamber.add_exit("out", car_interior)

	car_interior.add_exit("out", field)

	field.add_exit("n", valley)

	valley.add_exit("n", swamp)
	valley.add_exit("s", field)

	swamp.add_exit("n", swamp_north)
	swamp.add_exit("s", valley)

	swamp_north.add_exit("n", hill)
	swamp_north.add_exit("s", swamp)

	hill.add_exit("n", gate_room)
	hill.add_exit("e", clearing)
	hill.add_exit("s", swamp_north)

	gate_room.add_exit("e", hut)
	gate_room.add_exit("n", foyer)
	gate_room.add_exit("s", hill)

	hut.add_exit("w", gate_room)

	clearing.add_exit("w", hill)

	foyer.add_exit("s", gate_room)
	foyer.add_exit("out", dark_chamber)

	dark_chamber.add_exit("out", museum)

	museum.add_exit("s", None)

	# ─── OBJECTS ──────────────────────────────────────────────

	# Track game state
	world.puzzle_box_pushes = set()
	world.tree_burning = False
	world.gate_open = False
	world.rod_pulled = False
	world.car_crashed = False
	world.branch_fallen = False
	world.arrow_tarred = False
	world.arrow_lit = False
	world.arrow_loaded = False
	world.sword_taken = False
	world.toranuld_dead = False
	world.escaped = False
	world.has_branch = False

	# ─── ROD ───
	rod = GameObject("hot pink-colored rod", "It protrudes straight out of the wall six inches, then turns up another three, making it seem like some kind of handle. Its odd color of hot pink now seems normal amidst this room's brilliance.")
	rod.attributes.update(["turnable", "static"])
	rod.aliases = ["rod", "handle", "pink rod"]

	def on_rod_turn(player):
		if world.rod_pulled:
			print("You've already turned the rod. The floor has fallen out below you!")
			return
		world.rod_pulled = True
		print("You grab the hot pink-colored rod and for a moment are not sure how to work it, but soon discover that by twisting it clockwise you get the mechanical sound of something catching, like a key unlocking a door. Now the handle pulls out a few inches from the wall, clicking all the way.")
		print("")
		print("The floor begins to rumble and shake as a result of your messing with the rod. An engine screeches loudly from within the walls, and (oh dear) the floor falls out from under your feet. You land with a thunk, looking up just in time to see the ceiling of this new room (which presumably was the floor of the first) churn closed on two massive hinges. The sound of the engine stops abruptly.")
		rod.attributes.discard("static")
		rod.attributes.discard("turnable")
		rod.place(car_interior)
		player.place(car_interior)
		world.current_room = car_interior

	rod.on_turn = on_rod_turn

	# ─── CAR INTERIOR OBJECTS ───

	car = GameObject("hot pink-colored convertable", "Hmm... it seems you touched a hot-pink rod and got a hot-pink rod, for this car is truly the same color as the handle. It is an open convertible. You fell through the top on your way down here. It seems a very nice car, but not one to your taste; its shade of pink in both interior and exterior is almost gross in intensity, so that if you gazed at the hood long enough you'd probably get a brain tumor.")
	car.attributes.update(["static", "scenery"])
	car.aliases = ["car", "convertible", "vehicle", "pink car"]

	def car_before(action, player, target, second):
		if action == "start" and target is car:
			if ignition_key.location is not player:
				print("You don't have a key to start the car with.")
				return True
			world.rod_pulled = True
			print("You turn the key in the ignition, hearing the engine whirr like you used to groan when your alarm clock woke you up in the morning. The engine sputters a little bit more, and then with a cough comes to life. Before you have a chance to react; however, the vehicle lurches forward, you cannot do anything to stop it. Following the law of Murphy, the car has exactly enough time to build up a bit of speed before it slams into the cement wall!")
			print("")
			print("You open your eyes. You're alive! Why are you alive? Well, maybe you're not alive, considering that the hot-pink colored car is floating along with the clouds in a perfect blue sky.")
			print("")
			print("You take a look backwards. Hmm... there's a hole far up in an unfathomably high cement wall, and bits of cement debris are falling next to the car, which is not even noticeably scratched! You're beginning to think that this madness isn't so bad; it saved your life didn't it?")
			print("")
			print("You wait for several minutes as you fall, and finally become brave enough to look down. The ground grows closer each second; impact is now only a moment away. You have time for one more thought before your doom: \"Hey, if this car ploughed through a cement wall, maybe it'll survive the fall.\"")
			world.score += 2
			world.car_crashed = True
			player.place(field)
			world.current_room = field
			world.actions.action_look(player)
			print("")
			print("[Your score has just gone up by two points.]")
			return True
		return False

	car.before = car_before

	seats = GameObject("violet bucket seats", "By now you are only vaguely surprised to find that the seats are a radiant violet color. Other than that, they are bucket seats, have their own arm rests, and sit upon metal frames, leaving a little bit of floor space underneath them.")
	seats.attributes.update(["static", "scenery", "supporter"])
	seats.aliases = ["seats", "bucket seats", "seat"]

	rucksack = GameObject("sturdy leather rucksack", "It is an antiquated brown leather carry-all, worn a bit by the passage of time yet sturdy. Its handle is a stout slab of leather, apparently capable of holding all that weight of the many items which one would be able to fit within the large interior.\n\nBeing a humanly plain brown color, the sturdy leather rucksack contrasts the surrounding colorfulness and that of the previous room like aluminum foil touching a filling. It is almost comforting to look upon; while not proving or providing sanity in and of itself, it is a reminder, albeit a scant one, of regularity and order; laws that bind the way the world behaves.")
	rucksack.attributes.update(["container", "open"])
	rucksack.aliases = ["rucksack", "sack", "backpack", "carry-all"]

	glove_compartment = GameObject("glove compartment", "A simple glove compartment built in the dashboard by the passenger seat.")
	glove_compartment.attributes.update(["container", "openable", "static"])
	glove_compartment.aliases = ["glove compartment", "compartment", "dashboard"]

	metal_box = GameObject("six-by-four-inch metal box", "It's a metal box, perhaps of blued steel. It is unadorned save for a very small keyhole and hinges in the back.")
	metal_box.attributes.update(["container", "openable", "lockable", "locked"])
	metal_box.aliases = ["metal box", "steel box", "six-by-four-inch box"]

	small_key = GameObject("small key", "A small brass key, slightly corroded.")
	small_key.attributes.update(["key"])
	small_key.aliases = ["key", "small key", "brass key"]

	maple_box = GameObject("slightly smaller box of maple-wood", "This box is only slightly smaller than the one you found it in, though it is much different in appearance. First off, it is made of wood -- fine maple, you would say. Whereas the metal box is unadorned, this box is quite decorative, having an old cryptic look because of engravings and designs carved into it, although there seems no obvious way to open it.\n\nThree carvings on the top of the box stand out: an intricate square, a fancy broadsword, and an amulet shaped like an hourglass. These seem carved deep into the wood; they look as though they could be depressed like buttons.")
	maple_box.attributes.update(["container", "openable", "pushable"])
	maple_box.aliases = ["maple box", "wooden box", "puzzle box", "maple-wood box", "box of maple-wood", "wood box"]

	square_carving = GameObject("carving of an intricate square", "Amazingly, you can see quite a bit of detail in the wooden carving, and you're rather convinced that it works like a button. The carving is of a square, maybe a box, which has designs not wholly unlike those of the box onto which it is engraved. Yet the carving looks more archaic, and it has spots of masterful engrafted detail that suggest rust, perhaps the square depicted is a likeness of a box that is some ancient relic, with spiritual or ethical significance, though it doesn't really need any explanation of existence to be here, in this place where things just seem to exist without any semblance of reason or belonging.")
	square_carving.attributes.update(["pushable", "static", "scenery"])
	square_carving.aliases = ["square", "carving", "intricate square", "square carving"]

	def on_push_square(player):
		world.puzzle_box_pushes.add("square")
		print("The carving of an intricate square depresses smoothly some inches downward and comes back up without making barely any noise.")

	square_carving.on_push = on_push_square

	broadsword_carving = GameObject("carving of a fancy broadsword", "The stout iron blade and the spectacularly detailed haft and pommel are outlandishly clear in the wooden carving.")
	broadsword_carving.attributes.update(["pushable", "static", "scenery"])
	broadsword_carving.aliases = ["fancy broadsword", "broadsword carving", "sword carving"]

	def on_push_broadsword(player):
		world.puzzle_box_pushes.add("broadsword")
		print("The carving of a fancy broadsword depresses smoothly some inches downward and comes back up without making barely any noise.")

	broadsword_carving.on_push = on_push_broadsword

	amulet_carving = GameObject("carving of an amulet shaped like an hourglass", "Perhaps the most interesting carving of the three, the amulet has been meticulously crafted into the solid maple. A long chain of iron links is connected to the top of the hourglass and is wrapped around the middle section where a grain of sand would fall through were it a real glass, though it seems as if the skilled carver was trying to depict only clear glass.")
	amulet_carving.attributes.update(["pushable", "static", "scenery"])
	amulet_carving.aliases = ["amulet carving", "hourglass carving", "hourglass amulet", "carving"]

	def on_push_amulet(player):
		world.puzzle_box_pushes.add("amulet")
		print("The carving of an amulet shaped like an hourglass depresses smoothly some inches downward and comes back up without making barely any noise.")
		if "square" in world.puzzle_box_pushes and "broadsword" in world.puzzle_box_pushes and "amulet" in world.puzzle_box_pushes:
			if not maple_box.is_open():
				maple_box.attributes.add("open")
				brown_box.place(maple_box)
				print("")
				print("The top of the slightly smaller box of maple-wood springs open, revealing a very small, brown box.")

	amulet_carving.on_push = on_push_amulet

	brown_box = GameObject("very small, brown box", "It is by far the smallest box you've encountered yet -- just a four-by-two-inch brown rectangle. It seems rather un-boxlike; it has neither an obvious way of being opened nor any engravings or designs of any type or form at all. Furthermore, and stranger still, it doesn't look textured in any way that would suggest a solid, tangible material. In fact, it looks to be soft and pliable.\n\nStrange hot rods, strange room, strange boxes -- everything about your life seems strange today. You just hate these days when you wake up in a tiny cramped (and wildly-colored) chamber. No good for mental health.")
	brown_box.aliases = ["brown box", "rectangle", "chocolate"]

	def describe_brown_box():
		if hasattr(brown_box, "_chocolate_eaten") and brown_box._chocolate_eaten:
			return "It's just an empty wrapper now."
		return brown_box.description

	brown_box.describe = describe_brown_box

	def on_touch_brown_box(player):
		if hasattr(brown_box, "_chocolate_eaten") and brown_box._chocolate_eaten:
			print("It's just an empty wrapper.")
			return
		print("It is soft to your touch! Not completely pliable like clay, but your fingernails can easily scratch it, and after you've handled it some dark substance remains on your fingers.")

	brown_box.attributes.update(["touchable"])

	class BrownBox(GameObject):
		def before(self, action, *args):
			if action == "touch":
				on_touch_brown_box(player)
				return True
			return False

	def on_brown_box_smell(player, target):
		if hasattr(brown_box, "_chocolate_eaten"):
			print("It just smells like old cardboard now.")
			return
		print("You sniff at the rectangle, and catch a scent which you somehow recognize, sweet, rich, flavorful... chocolate?")

	# We'll handle the brown box specially in the main flow
	# since its behavior spans multiple actions

	cupholder = GameObject("cupholder", "A filthy mess of slime and dirt is corroded to the bottom and sides of the cupholder. You cannot see anything in it, but it's small and dark therein, and you suppose something could be hiding in the gook.")
	cupholder.attributes.update(["container", "static", "scenery"])
	cupholder.aliases = ["cupholder", "holder"]

	ignition_key = GameObject("ignition key", "A metal key, toothed on both sides, like an ignition key to a vehicle.")
	ignition_key.attributes.update(["key"])
	ignition_key.aliases = ["ignition key", "key", "car key"]

	# ─── PLACE OBJECTS IN CAR INTERIOR ───
	car.place(car_interior)
	seats.place(car_interior)
	rucksack.place(car_interior)
	glove_compartment.place(car_interior)
	cupholder.place(car_interior)

	# Rucksack starts empty
	# Glove compartment contains metal box
	metal_box.place(glove_compartment)
	# Metal box contains maple box
	maple_box.place(metal_box)
	# Carvings are on the exterior of the maple box — visible even when box is closed
	# Place them in the metal box (same container as maple box) so they're in scope
	square_carving.place(metal_box)
	broadsword_carving.place(metal_box)
	amulet_carving.place(metal_box)
	# Cupholder contains small key
	small_key.place(cupholder)

	# ─── SEARCH SEATS → find rucksack ───
	original_search_seats = seats.after if hasattr(seats, 'after') else None

	def seats_after(action, player, target, second):
		if action == "search" and target is seats:
			rucksack.place(seats)
			world.actions.move_object(rucksack, player)
			print("You find and take a sturdy leather rucksack from beneath the driver's seat.")
			return True
		return False

	# Use before/after hooks
	# Actually, since we want to hook into the default search behavior,
	# let's use a different approach: override via the before hook on the seats object

	class SceneryWithSearch(GameObject):
		def before(self, action, player, target, second):
			return False

	# Let's use a simpler approach: register a custom handler

	# ─── FIELD OBJECTS ───

	car_wreck = GameObject("flaming wreck of a hot pink-colored convertable", "It's completely unrecognizable in its flames; your survival was a miracle. You don't need to worry about it blowing up any time soon; it looks as if it has already exploded.")
	car_wreck.attributes.update(["static", "scenery"])
	car_wreck.aliases = ["car", "wreck", "wreckage", "flaming wreck"]

	wall_ruins = GameObject("tremendous cement wall", "The wall extends eternally up, slicing through the sky like a knife in a vat of butter, as well as east and west, as far as the eye can see. Its flat face of drab grey concrete betrays nothing, but presumably you came through it somewhere far up hidden by space. Again you wonder how you could still be alive.")
	wall_ruins.attributes.update(["static", "scenery"])
	wall_ruins.aliases = ["wall", "cement wall", "concrete wall"]

	car_wreck.place(field)
	wall_ruins.place(field)

	# ─── VALLEY OBJECTS ───

	stone = GameObject("single stone", "It's a smooth round stone, about the size of your fist. It would make a good projectile.")
	stone.aliases = ["stone", "rock", "single stone"]

	stone.place(valley)

	# ─── SWAMP OBJECTS ───

	swamp_tree = GameObject("tall, leafless dead tree", "It quite surprises you that this tree is here in this dead place, though if it still is alive it doesn't look it. You cannot tell by glancing what kind of tree it is, but it must be one of the tall varieties, for from the water level it reaches straight up for many feet above the water level, its lowest naked branches stopping a few feet above your reach.")
	swamp_tree.attributes.update(["static", "scenery"])
	swamp_tree.aliases = ["tree", "dead tree", "leafless tree"]

	branch_obj = GameObject("long, sturdy branch", "It looks quite dense and sturdy compared to some of the other branches, and probably could come in handy. It's higher than you can reach, but it seems to be hanging onto the bough at the place where lightning struck very barely. If only you could somehow knock it down.")
	branch_obj.aliases = ["branch", "sturdy branch", "long branch"]

	swamp_tree.place(swamp)

	# ─── HILL / EVIL TREE ───

	evil_tree = GameObject("evil animated tree", "In every physical aspect the same tree you met earlier down to the broken bough -- it is somehow alive, a giant gnarly monster. Its dead and dried appendages hang unnaturally flexible, long limbs prepared to attack you. Some entity looms about the dead wood, a force animating it; and you sense it with the long-existent but never-named sense of supernatural in mankind as a frigid, sickening fear.")
	evil_tree.attributes.update(["static", "animate"])
	evil_tree.aliases = ["tree", "evil tree", "animated tree"]

	evil_tree.place(hill)

	# ─── GATE ───

	gate = GameObject("impenetrable gate", 'Inscribed in large, ornate lettering along the marble curve are the words: "THESE GATES SHALL NOT OPEN -- SAVE BY THE BLADE OF TRUTH."\n\nThe gate is of the double-door variety, and stands an impenetrable bulwark, the heavy doors shut with hardly a crack at their junction. You are on the outside, and if you have any hopes of getting on the inside, you\'ll have to come up with something.')
	gate.attributes.update(["static", "scenery"])
	gate.aliases = ["gate", "marble gate", "impenetrable gate"]

	gate.place(gate_room)

	# ─── HUT OBJECTS ───

	shield = GameObject("round wooden shield", "The brass shield-boss in this otherwise ordinary shield's center is shaped in a simple fish design, the metal stained a deep red. Strange, that.")
	shield.aliases = ["shield", "wooden shield", "round shield"]

	tar_bucket = GameObject("bucket of tar", "A bucket of thick, black tar. It's sticky and viscous.")
	tar_bucket.attributes.update(["container", "open", "static"])
	tar_bucket.aliases = ["tar", "bucket", "bucket of tar"]

	flint1 = GameObject("piece of flint", "A piece of flint, the kind used to start fires.")
	flint1.aliases = ["flint", "piece of flint"]

	flint2 = GameObject("piece of flint", "A piece of flint, the kind used to start fires.")
	flint2.aliases = ["flint", "piece of flint"]

	bow = GameObject("yew bow", "A finely crafted yew bow, unstrung but in good condition.")
	bow.aliases = ["bow", "yew bow", "longbow"]

	arrow = GameObject("long-shafted arrow", "A long-shafted arrow, fletched with gray goose feathers.")
	arrow.attributes.update(["lightable"])
	arrow.aliases = ["arrow", "long-shafted arrow", "shaft"]

	# Multiple arrows in the room (the game mentions several burning ones)
	# We'll just have one arrow that the player can pick up

	shield.place(hut)
	tar_bucket.place(hut)
	flint1.place(hut)
	bow.place(hut)
	arrow.place(hut)

	# ─── CLEARING OBJECTS ───

	pedestal = GameObject("marble pedestal", "A rectangular block of fine marble, it is engraved like a Corinthian pillar; long marbled tresses decorate the otherwise smooth base beside delicate fig leaves.\n\nThe top surface of the pedestal supports a marvelous broadsword. It lies placed perfectly across the center of the square surface; to either side of it runes of an ancient mode have been skillfully incised.")
	pedestal.attributes.update(["static", "scenery"])
	pedestal.aliases = ["pedestal", "marble pedestal", "platform"]

	runes = GameObject("ancient runes", "The letters flow elegantly upon the surface of the platform, presumably describing the magical sword. They are in a very antiquated fashion; trying to read them is a lost cause, but to your eye they look possibly Greek and most certainly Cyrillic. You are fairly sure they are not some kind of old Latin.")
	runes.attributes.update(["static", "scenery"])
	runes.aliases = ["runes", "inscription", "writing"]

	sword = GameObject("ornate broadsword", "The flawless blade protrudes two feet out from the ornate hilt, a deep groove cut into the entire length of the double-edged blade beginning several inches above the hilt and terminating near the top of the blade. The blade does not angle sharply on either side at its top for the two broad sides to meet and form the razor-sharp point; instead, the whole length is shaped like a much-elongated triangle, gradually growing thinner.\n\nThe haft is more than a foot long; its comfortable wooden grip, inlaid with a floral pattern in ivory, is easily long enough for a big man to grab two-handed. Above the grip, the gold-plated crossguards lie long and curved upwards. The pommel attached to the grip is a three-inch diameter circle of precious metals and bearing an emerald of high quality.")
	sword.aliases = ["sword", "broadsword", "ornate broadsword", "blade", "blade of truth"]

	def sword_take_intercept(action, player, target, second):
		if action == "take" and target is sword:
			if not world.sword_taken:
				world.sword_taken = True
				world.score += 2
				print("As your hands grip the hilt, a mysterious sense of power excites you. Even more mysteriously, this sense of power is mingled with a sense of familiarity.")
				print("[Your score has just gone up by two points.]")
				if hasattr(world, 'arrow_lit') and world.arrow_lit:
					arrow.location = None
					print("The small flame has burnt away all the tar and makes its way down the shaft alarmingly quickly. You toss the long-shafted arrow away.")
			return False
		return False

	sword.before = sword_take_intercept

	pedestal.place(clearing)
	runes.place(clearing)
	sword.place(clearing)

	# ─── FOYER OBJECTS ───

	toranuld = GameObject("frightening man", 'The man is taller, imposing more so than you by several feet. He is wrapped securely in some sort of dark robe or cloak, which covers his ankles and his arms with its long, baggy sleeves. In the right hand the man is grasping a long staff, perfectly straight and with a strange pointed head atop it. The hand that grasps the staff is thin and withered with overgrown fingernails.\n\nThe face earns by far most of your attention. It looks, superficially, like the face of any old man, but the eyes (which you confirm to be yellow) are inflamed and baggy. The man\'s forehead is marred by some dark marking or scar of sorts, beneath a head of long, white locks (but the hairline is receding). A large, and somehow crooked nose lies above a small mouth, hidden by mustache and beard, which extend several inches across the chest. Dark lines that suggest a perpetual sneer are visible running along his face. All things considered, the face indeed looks very evil, almost in a deranged, half-psychotic way.')
	toranuld.attributes.update(["animate", "proper", "static"])
	toranuld.aliases = ["man", "toranuld", "demon", "lord", "figure", "entity"]

	toranuld_amulet = GameObject("A small, silver pendant shaped like an hourglass", "It is the same amulet as the one depicted on the puzzle-box. From this real examination you can tell that its features are engraved in pure silver, with delicate grains of sand depicted with gold by some astounding feat of metallurgy.")
	toranuld_amulet.attributes.update(["static"])
	toranuld_amulet.aliases = ["amulet", "pendant", "hourglass", "silver pendant", "Amulet of the Ages"]

	toranuld.place(foyer)
	toranuld_amulet.place(foyer)

	# ─── MUSEUM OBJECTS ───

	museum_box = GameObject("A small, intricate box", "It's the box which was a button on the puzzle-box. And you'll bet it's also the third of the sacred objects!")
	museum_box.aliases = ["box", "intricate box", "small box"]

	museum_box.place(museum)

	# ─── SPECIAL LOGIC ────────────────────────────────────────

	# Search seats → find rucksack
	def seats_before(action, player, target, second):
		if action == "search" and target is seats:
			if rucksack.location is not player:
				world.actions.move_object(rucksack, player)
				print("You find and take a sturdy leather rucksack from beneath the driver's seat.")
				return True
		return False

	seats.before = seats_before

	# Search cupholder → find small key
	def cupholder_before(action, player, target, second):
		if action == "search" and target is cupholder:
			if small_key.location is not player:
				world.actions.move_object(small_key, player)
				print("You put your hand bravely into the slime, and bring out a small key.")
				return True
		return False

	cupholder.before = cupholder_before

	# Brown box special behavior
	def brown_box_before(action, player, target, second):
		if target is not brown_box:
			return False
		if action == "touch":
			on_touch_brown_box(player)
			return True
		if action == "smell":
			if hasattr(brown_box, "_chocolate_eaten"):
				print("It just smells like old cardboard now.")
				return True
			print("You sniff at the rectangle, and catch a scent which you somehow recognize, sweet, rich, flavorful... chocolate?")
			return True
		if action == "taste" or action == "eat":
			return False  # Let default handling work, then we intercept
		return False

	brown_box.before = brown_box_before

	# Override taste for brown box
	def brown_box_after(action, player, target, second):
		if target is brown_box and action == "taste":
			if hasattr(brown_box, "_chocolate_eaten"):
				print("It's already been eaten.")
				return
			brown_box._chocolate_eaten = True
			print("Chocolate it is, and better chocolate than you've ever had in your life. Not that you're an avid chocoholic, but this seems the most creamy, most smooth and luxurious morsel that has ever passed your lips.")
			print("")
			print("As it dissolves in your mouth beautifully slowly, something hard and cold ruins the delicious sensation. You pull out of your mouth a key, toothed on both sides, like an ignition key to a vehicle. You lick it clean of the last remnants of chocolate.")
			if ignition_key.location is not player:
				world.actions.move_object(ignition_key, player)

	brown_box.after = brown_box_after

	# "taste" isn't a standard action that catches "eat"
	# Let's add "eat" as a synonym for taste
	world.actions.register_default_response("eat", "")  # Will be handled by the before hook

	def action_eat(player, target, second):
		if target is brown_box:
			brown_box_after("taste", player, brown_box, None)
			return
		print("That doesn't appeal to you.")

	world.actions.register_action("eat", action_eat)

	# ─── SWAMP TREE LOGIC ───

	# ─── SWAMP CROSSING LOGIC ───

	def swamp_before(action, player, target, second):
		if action == "smell" and target is None:
			print("The bog-odor is repugnant in your nostrils.")
			print("")
			print("Angry dark clouds gather above you where the sky had been clear a moment before. Suddenly, you cringe backwards as a bolt of lightning streaks down, striking one of the tree's greater branches, which is nearly severed from the tree, but hangs onto the main bough by a few weak strands of plant tissue just out of your reach.")
			if not world.branch_fallen and branch_obj.location is None:
				branch_obj.attributes.add("static")
				branch_obj.place(swamp)
			return True
		if action == "throw" and target is stone and second is branch_obj and not world.branch_fallen:
			if branch_obj.location is not None:
				world.branch_fallen = True
				print("Gripping the smooth round stone in your hand, you strain your arm as you hurl it furiously at your target. Your stone hits the break in the bough head-on, and then falls into the swamp, sinking with a splash. The branch, knocked off its thin balance, hangs precariously by its thinner hold for a moment, twisting with momentum. Now its own small weight betrays it, and it drops into the swamp. It goes under and bobs back up, now floating within reach!")
				branch_obj.attributes.discard("static")
				stone.place(None)
				branch_obj.place(swamp)
			return True
		if action == "go":
			direction = getattr(world.actions, '_last_direction', None)
			if direction == "north" and not world.has_branch:
				if world.branch_fallen:
					print("You bravely stride forward, but the water gets darker and deeper as a forceful current runs across this part of the swamp, which you cannot push through. If only you had something to brace yourself with!")
					return True
		return False

	swamp.before = swamp_before

	# Getting the branch gives you the ability to cross
	def branch_take_intercept(action, player, target, second):
		if action == "take" and target is branch_obj:
			if not world.has_branch:
				world.has_branch = True
				world.score += 2
				print("[Your score has just gone up by two points.]")
			return False
		return False

	branch_obj.before = branch_take_intercept

	# ─── EVIL TREE LOGIC ───

	def evil_tree_before(action, player, target, second):
		if action == "go":
			direction = getattr(world.actions, '_last_direction', None)
			if direction == "north" and evil_tree.location is hill:
				print("The tree lunges at you again, but as soon as its roots touch the stone road it instantly brings them back as if it had touched a red-hot burner.")
				return True
		if action == "shoot" and target is evil_tree:
			if not world.arrow_loaded:
				print("You need to load your bow first!")
				return True
			if world.arrow_lit:
				world.tree_burning = True
				print("You pull back the bowstring, and release your arrow. Your shot is good; your enemy is hit!")
				print("")
				print("The flaming arrow hits the tree near the topmost, driest boughs, which begin to ignite almost immediately. The tree churns about, bending with uncanny flexibility as it waves its boughs in raving madness. The wretched thing, writhing in torment, begins to dance across the area madly, and accidentally hits its roots against the stone road in the meantime. In horrendous agony, the tree retreats southward down the hill, perhaps hoping to extinguish itself in the horrid swamp-waters.")
				return True
			else:
				print("Your arrow isn't lit!")
				return True
		return False

	evil_tree.before = evil_tree_before

	# ─── GATE LOGIC ───

	def gate_before(action, player, target, second):
		if action == "hit":
			if second is not None and second is sword:
				if not world.gate_open:
					world.gate_open = True
					print('A bit more than half unsure of yourself, you bring the blade down upon the gate. As soon as metal touches metal by even indescribable proportions, a rumbling sound greets your ears. You remove the sword in a shallow fit of panic as the enormous double-gate begins to swing outward! Even now it settles into an open position; however, it still seems uninviting.')
					print("")
					print('"Hello."')
					print("")
					print("The voice that greets you is stately, calm, slow, and chillingly venomous.")
					print("")
					print("You notice a figure standing by the door to the castle at the opposite end of this courtyard, which is smaller than it appeared from the outside and very unremarkable.")
					print('"Allow me to introduce myself. I am the lord of this humble world you\'ve stumbled into, and you are my new slave..."')
				player.place(foyer)
				world.current_room = foyer
				world.actions.action_look(player)
				return True
			else:
				print("Violence isn't the answer to this one.")
				return True
		return False

	gate.before = gate_before

	# ─── TORANULD LOGIC ───

	toranuld_asked_about = set()

	def toranuld_before(action, player, target, second):
		if action == "ask":
			topic = ""
			if second is not None:
				topic = second.name.lower() if hasattr(second, 'name') else str(second)
			if not topic:
				raw = getattr(world.parser, 'last_command', '')
				parts = raw.lower().replace('?', '').split()
				if 'about' in parts:
					idx = parts.index('about')
					topic = ' '.join(parts[idx+1:]) if idx + 1 < len(parts) else ''
			if topic:
				toranuld_asked_about.add(topic)
				if "man" in topic or "toranuld" in topic:
					print('"Well, for starters, this place you have entered is my dominion. Here I am sovereign..."')
					return True
				if "sword" in topic or "blade" in topic:
					print('"The blade of truth -- one of the three sacred objects that help to keep this world together. It was forged fifteen hundred years ago; the inscription on its blade reads \'By this sword shall a great kingdom fall.\'"')
					return True
				if "object" in topic or "amulet" in topic or "sacred" in topic or "box" in topic:
					print('"The Amulet of the Ages," says the frightening man caressing the pendant in a lithe hand.')
					print('"The Sword you have won in your cleverness; the Amulet I keep, and therefore any thoughts of mutiny or escape you may have are vain. The third object is hidden to you, and I shall not speak more of it."')
					return True
				print('Toranuld glowers at you menacingly.')
				return True
			print("Ask about what?")
			return True
		if action == "kill" or action == "attack":
			if second is not None and second is sword:
				if world.toranuld_dead:
					print("Toranuld is already destroyed.")
					return True
				print("You swing the blade with all the might that you possess...")
				world.toranuld_dead = True
				world.score += 2
				print("[Your score has just gone up by two points.]")
				print("The keen iron of the blade catches the amulet around his neck...")
				print("")
				print("The body crumples for an instant on the floor and then disappears in a puff of thick black mist!")
				toranuld.place(None)
				toranuld_amulet.attributes.discard("static")
				return True
			else:
				print("The keen iron of the blade merely bounces off Toranuld who doesn't so much as blink. Toranuld mocks you with a cruel laugh.")
				return True
		return False

	toranuld.before = toranuld_before

	# ─── TORANULD AMULET LOGIC ───

	def amulet_before(action, player, target, second):
		if action == "hit" and target is toranuld_amulet:
			if second is sword:
				if not world.toranuld_dead:
					print("Toranuld is still in possession of the amulet. Kill him first.")
					return True
				world.escaped = True
				world.score += 2
				print("[Your score has just gone up by two points.]")
				print("You bring the heavy broadsword down on the amulet upon the floor. A great silver flash!"
					"The amulet shatters and the silver links fly apart, skittering along the floor.")
				print("")
				print("A great rumbling comes from the ground below you, and the floor shakes with a sudden violence."
					" A crack opens in the granite floor to the west, spreading wide enough to reveal a dark hole.")
				foyer.add_exit("out", dark_chamber)
				return True
			print("You can't damage the amulet with that.")
			return True
		if action == "take" and target is toranuld_amulet:
			if not world.toranuld_dead:
				print("Toranuld turns his staff toward you, glowering under dark brows. The hand you had raised suddenly writhes in pain, and you feel a force push your body against the stone wall, not entirely gently.")
				return True
			return False
		return False

	toranuld_amulet.before = amulet_before

	# ─── DARK CHAMBER ESCAPE ───

	def dark_chamber_before(action, player, target, second):
		if action == "go":
			direction = getattr(world.actions, '_last_direction', None)
			if direction == "out":
				player.place(museum)
				world.current_room = museum
				print("You push with your body and limbs in agony, trying to leave this dark pit. As you do so, your efforts are rewarded as a hatch in the ceiling pushes open at the upward push of your head and shoulders. Exhausted but thankful, you crawl out of the chamber and find yourself somewhere bright and large...")
				print("")
				world.actions.action_look(player)
				return True
		return False

	dark_chamber.before = dark_chamber_before

	# ─── MUSEUM WIN ───

	def museum_before(action, player, target, second):
		if action == "go":
			direction = getattr(world.actions, '_last_direction', None)
			if direction == "south":
				world.score += 2
				print("You step out of the museum and into the street.")
				print("")
				print("Oh, the city! And the beautifully sweet and smoggy city air!")
				print("")
				world.win_message = f"*** You have won! ***\n\nIn that game you scored {world.score} out of a possible {world.max_score}. You have earned the rank of demon-slayer!"
				world.win_condition = lambda: True
				return True
		return False

	museum.before = museum_before

	# ─── ARROW / BOW / FLINT LOGIC ───

	world.arrow_tarred = False
	world.arrow_lit = False
	world.arrow_loaded = False

	# Handle "put arrow in tar" — intercepted via arrow.before
	# (the tar remains on the arrow, it stays in player's inventory)

	# Handle "light arrow with flint" and "put arrow in tar"
	def arrow_before(action, player, target, second):
		if action == "put" and second is not None:
			if "tar" in second.name.lower() or "bucket" in second.name.lower():
				world.arrow_tarred = True
				print("You secure some tar to the end of the arrow below the arrowhead.")
				return True
		if action == "light":
			if second is not None and "flint" in second.name.lower():
				if not world.arrow_tarred:
					print("The arrow isn't tarred. You need to put it in tar first.")
					return True
				world.arrow_lit = True
				print("The sparks catch the tar on the arrow, and your work is rewarded by a small flame.")
				print("")
				print("The tar on your arrow is burning.")
				return True
		return False

	arrow.before = arrow_before

	# Handle "load arrow in bow"
	def bow_on_load(player, target):
		if target is arrow:
			if not world.arrow_lit:
				print("The arrow isn't lit yet. You need to light it first.")
				return
			world.arrow_loaded = True
			print("You put the long-shafted, burning arrow into the yew bow.")
			print("")
			print("The tar on your arrow is burning.")
	bow.on_load = bow_on_load

	# ─── STARTING STATE ───

	world.start(chamber)
	rod.place(chamber)

	return world
