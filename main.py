"""
Dreary Lands - Python re-creation of a Z-code IFComp entry from 2005.
"""

import sys
from dreary_lands import build_world


def main():
	world = build_world()
	world.run()


if __name__ == "__main__":
	main()
