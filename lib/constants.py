import pygame

# - Window size
WIN_WIDTH = 576
WIN_HEIGHT = 480

WIN_SIZE = WIN_WIDTH,WIN_HEIGHT

# - Base drawing rectangle
DRAW_RECT = pygame.Rect((0,0),WIN_SIZE)

# - Target frame rate
FRAME_RATE = 60

# - Map tile size
TILE_SIZE = 24

# - Map size
MAP_WIDTH   = 20
MAP_HEIGHT  = 16
MAP_SIZE    = MAP_WIDTH,MAP_HEIGHT

# - Map border size
MAP_BORDER_X = 2
MAP_BORDER_Y = 1

MAP_BORDER_WIDTH = MAP_BORDER_X * TILE_SIZE
MAP_BORDER_HEIGHT = MAP_BORDER_Y * TILE_SIZE

# - Map drawing size
MAP_DRAW_WIDTH = (MAP_WIDTH*TILE_SIZE) + (MAP_BORDER_WIDTH*2)
MAP_DRAW_HEIGHT = (MAP_HEIGHT*TILE_SIZE) + (MAP_BORDER_HEIGHT*2)

MAP_DRAW_SIZE    = MAP_DRAW_WIDTH,MAP_DRAW_HEIGHT

# - Map drawing rectangle
MAP_DRAW_RECT = pygame.Rect((0,0),MAP_DRAW_SIZE)

# (Set the map drawing rectangle's position,
#  just in case of weirdness)
MAP_DRAW_RECT.top = DRAW_RECT.top
MAP_DRAW_RECT.centerx = DRAW_RECT.centerx

# - Hud drawing size
HUD_DRAW_WIDTH  = WIN_WIDTH
HUD_DRAW_HEIGHT = 120

HUD_DRAW_SIZE = HUD_DRAW_WIDTH,HUD_DRAW_HEIGHT

# - Hud drawing rectangle
HUD_DRAW_RECT = pygame.Rect((0,0),HUD_DRAW_SIZE)

# (Align the hud drawing rectangle with the
#  drawing surface rectangle)
HUD_DRAW_RECT.bottom    = DRAW_RECT.bottom
HUD_DRAW_RECT.centerx   = DRAW_RECT.centerx

# - Factions
#   (Red is the AI, blue is the player)
FACTIONS = 'red','blue'

# - Unit types
UNIT_TYPES = 'swordsman','archer','wizard'

# - Unit layout size
UNIT_LAYOUT_WIDTH   = 3
UNIT_LAYOUT_HEIGHT  = 3

UNIT_LAYOUT_SIZE = UNIT_LAYOUT_WIDTH,UNIT_LAYOUT_HEIGHT

# - Terrain types
TERRAIN_TYPES = 'grass','dirt','spawn','rocks'

# - Star start and end X coordinates
#   (this is for the parallax star effect in
#    the background of the levels)
STAR_START_X = -20
STAR_END_X = MAP_DRAW_WIDTH + 20

# - Minimum time between AI faction commands
CPU_COMMAND_DELAY = 0.5

# - Maximum number of units
MAX_UNITS = 6
