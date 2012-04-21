import pygame
import pygame.transform
import pygame.draw

from math import *
from random import *

from constants import *
from data import *
from a_star import *

TEST_TERRAIN_TILES = []

# Top 14 rows
for y in range(14):
    TEST_TERRAIN_TILES.append([])
    
    for x in range(MAP_WIDTH*2):
        TEST_TERRAIN_TILES[-1].append(('grass',0))
        
    

# 4 rows below the top
for y in range(4):
    row_tiles = []
    
    for x in range(12):
        # First 12 tiles
        row_tiles.append(('grass',0))
    
    if y == 0:
        # The top row of this part
        
        # The top-left corner
        row_tiles.append(('rock',5))
        
        for x in range(14):
            # The top part of the rock
            row_tiles.append(('rock',1))
            
        
        # The top-right corner
        row_tiles.append(('rock',6))
        
    elif y in (1,2):
        
        row_tiles.append(('rock',4))
        
        for x in range(14):
            # The middle part of the rock
            row_tiles.append(('rock',0))
            
        
        row_tiles.append(('rock',2))
        
    else:
        # The bottom row of this part
        
        # The bottom-left corner
        row_tiles.append(('rock',8))
        
        for x in range(14):
            # The bottom part of the rock
            row_tiles.append(('rock',3))
            
        
        # The bottom-right corner
        row_tiles.append(('rock',7))
        
    
    for x in range(12):
        # Last 12 tiles
        row_tiles.append(('grass',0))
    
    TEST_TERRAIN_TILES.append(row_tiles)
    

# Bottom 14 rows
for y in range(14):
    TEST_TERRAIN_TILES.append([])
    
    for x in range(MAP_WIDTH*2):
        TEST_TERRAIN_TILES[-1].append(('grass',0))
        
    

class Unit(object):
    
    def __init__(self,pos,speed,health,faction,images):
        super(Unit,self).__init__()
        
        self.faction = str(faction).lower()
        
        if self.faction not in FACTIONS:
            raise ValueError('Invalid faction '+str(faction)+' given (valid values are: '+(', '.join(FACTIONS))+')')
            
        
        self.images = images
        
        self.pos = list(pos)
        self.path = []
        
        self.speed = int(speed)
        self.rotation = 0
        
        self.animNum = 0
        self.animFrame = 0
        self.animFrameTime = 0
        
        self.attackTarget = None
        
        self.world = None
        
        self.health = int(health)
        self.maxHealth = int(health)
        
        self.selectRect = pygame.Rect(0,0,14,14)
        
        self.selected = False
        
    
    def getGridPos(self):
        grid_pos = list(self.pos)
        
        grid_pos[0] = int(round(grid_pos[0]))
        grid_pos[1] = int(round(grid_pos[1]))
        
        return grid_pos
        
    gridPos = property(getGridPos)
    
    def getImage(self):
        return self.images[self.animNum][self.animFrame]
        
    
    def draw(self,dest):
        draw_x,draw_y = self.pos
        
        draw_x = int(round(draw_x))
        draw_y = int(round(draw_y))
        
        draw_x *= TILE_SIZE
        draw_y *= TILE_SIZE
        
        # Add in the size of a tile to allow for
        # the border around the map.
        draw_x += TILE_SIZE
        draw_y += TILE_SIZE
        
        image = self.getImage()
        image = pygame.transform.rotate(image,self.rotation)
        
        draw_x += TILE_SIZE // 2
        draw_y += TILE_SIZE // 2
        
        draw_x -= image.get_width() // 2
        draw_y -= image.get_height() // 2
        
        dest.blit(image,(draw_x,draw_y))
        
        if self.faction == 'blue' and self.selected:
            draw_x,draw_y = self.pos
            
            draw_x = int(round(draw_x))
            draw_y = int(round(draw_y))
            
            draw_x *= TILE_SIZE
            draw_y *= TILE_SIZE
            
            # TODO: Use the select cursor image
            image = None
            
            # TODO: Draw the selection cursor
            
        
        if self.health < self.maxHealth:
            health_bar_rect = [0,0,0,0]
            
            draw_x,draw_y = self.pos
            
            draw_x = int(round(draw_x))
            draw_y = int(round(draw_y))
            
            draw_x *= TILE_SIZE
            draw_y *= TILE_SIZE
            
            health_bar_rect[2] = 20
            health_bar_rect[3] = 4
            
            draw_y += TILE_SIZE
            draw_x += (TILE_SIZE - health_bar_rect[2]) // 2
            
            health_bar_surf = dest.subsurface(health_bar_rect)
            
            health_bar_surf.fill((191,0,0))
            
            green_bar_rect = [0,0,0,health_bar_rect[3]]
            
            green_bar_rect[2] = int( round( (float(self.health) / float(self.maxHealth)) * 20 ) )
            
            health_bar_surf.fill((0,191,0),green_bar_rect)
            
        
    
    def updateAnimation(self,dt):
        if len(self.path) > 0:
            self.animFrameTime += dt
            
            
        
    
    def update(self,dt):
        
        if len(self.path) > 0:
            move_amount = self.speed * dt
            path_part = self.path[0]
            
            move_direction = [0,0]
            
            if path_part[0] < self.pos[0]:
                move_direction[0] = -1
                
            elif path_part[0] > self.pos[0]:
                move_direction[0] = 1
                
            if path_part[1] < self.pos[1]:
                move_direction[1] = -1
                
            elif path_part[1] > self.pos[1]:
                move_direction[1] = 1
                
            
            self.pos[0] += move_direction[0] * move_amount
            self.pos[1] += move_direction[1] * move_amount
            
            if move_direction[0] < 0 and self.pos[0] <= path_part[0]:
                self.pos[0] = path_part[0]
                
            if move_direction[1] < 0 and self.pos[1] <= path_part[1]:
                self.pos[1] = path_part[1]
                
            
            if int(round(self.pos[0])) == path_part[0] and int(round(self.pos[1])) == path_part[1]:
                self.pos = path_part
                self.path = self.path[1:]
                
            
            self.selectRect.centerx = self.pos[0] + TILE_SIZE // 2
            self.selectRect.centery = self.pos[1] + TILE_SIZE // 2
            
        
    

class Swordsman(Unit):
    
    def __init__(self,pos,speed,health,faction,images):
        super(Swordsman,self).__init__(pos,speed,health,faction,images)
        
    
    def update(self,dt):
        super(Swordsman,self).update(dt)
        
    

class Faction(object):
    
    def __init__(self,units,color):
        super(Faction,self).__init__()
        
        self.units = list(units)
        
        self.color = str(color).lower()
        
        if self.color not in ('red','blue'):
            raise ValueError('Invalid faction color '+str(color)+' given (Valid values are "red" amd "blue", not case-sensitive)')
            
        
        self.selected = None
        
        self.world = None
        
    
    def checkWorlds(self):
        '''
        Check to make sure we are in the same world as
        our units.
        
        This is mainly useful for making sure that
        the faction's self.world AND the self.world
        of all of its units are set.
        '''
        
        if not self.world:
            # Wait a minute...
            # The faction doesn't have a world set!
            # How can we check if we're in the same
            # world if we're not even in a world?
            raise 'Faction does not have self.world set or has it set to None (well, or another false value, I suppose)'
            
        
        worlds = []
        
        for guy in self.units:
            worlds.append(guy.world)
            
        
        # Whether each given world is the same one
        # as the faction's world.
        worlds_are_mine = [his_world is self.world for his_world in worlds]
        
        # Whether each given world is None
        worlds_are_none = [his_world == None for his_world in worlds]
        
        if any(worlds_are_none):
            # At least one of our units' worlds
            # is set to None
            raise 'At least one of the faction\'s units has its self.world unset or set to none'
            
        elif not any(worlds_are_mine):
            # None of our units are in our world.
            # Could be a useful distinction, so we
            # report it separately.
            raise 'None of the faction\'s units are in the same world as the faction'
            
        elif not all(worlds_are_mine):
            # We're not all in the same world here.
            # Well, we need to report an error.
            raise 'Not all of the faction\'s units have the same world as the faction'
            
        
    

class PlayerFaction(Faction):
    
    def __init__(self,units):
        super(PlayerFaction,self).__init__(units,'blue')
        
        self.inputState = {}
        
        self.inputState['select'] = False
        self.inputState['command'] = False
        
    
    def handleInput(self,input_state,cpu_faction):
        if ((input_state['select'] and not self.inputState['select']) or
            (input_state['command'] and not self.inputState['command'])):
            
            grid_mouse_pos = list(input_state['mouse pos'])
            
            # Adjust for the border
            grid_mouse_pos[0] -= TILE_SIZE
            grid_mouse_pos[1] -= TILE_SIZE
            
            # Scale for the grid
            grid_mouse_pos[0] //= TILE_SIZE
            grid_mouse_pos[1] //= TILE_SIZE
            
            if input_state['select']:
                for guy in self.units:
                    if guy.selectRect.collidepoint(grid_mouse_pos):
                        if guy is self.selected:
                            # We've already selected that one
                            break
                            
                        
                        # Deselect the currently selected unit
                        self.selected.selected = False
                        
                        # Switch to the newly selected unit
                        self.selected = guy
                        
                        # Set the unit's selected flag to True
                        self.selected.selected = True
                        
                        # Break from the loop!
                        break
                        
                    
                
            elif input_state['command']:
                # TODO: Check whether we should attack
                
                world = self.selected.world
                
                path = None
                
                try:
                    path = world.pathForUnit(self.selected,end_pos)
                    
                except:
                    # We can't get that path, so we should
                    # just stay put for now. This cancels
                    # all movements, too.
                    self.selected.path = []
                    
                
                # We have the path, so we put it into
                # the unit.
                self.selected.path = path
                
            
        
        self.inputState['selected'] = input_state['selected']
        self.inputState['command'] = input_state['command']
        
    

class CpuFaction(Faction):
    
    def __init__(self,units):
        super(CpuFaction,self).__init__(units,'red')
        
        # The amount of time left before the AI
        # can make another command.
        self.commandTimer = 0.0
        
    
    def update(self,dt):
        self.commandTimer -= dt
        
        if self.commandTimer > 0.0:
            # Can't make another command yet...
            return
            
        
        # Otherwise...
        
    

class UnitLayout(object):
    
    def __init__(self,units):
        super(UnitLayout,self).__init__()
        
        self.units = []
        
        for guy in units:
            unit_type,unit_pos = guy[:2]
            
            self.units.append([unit_type,unit_pos])
            
        
    
    def getUnitsOfType(self,unit_type):
        unit_type = str(unit_type)
        
        if unit_type not in UNIT_TYPES:
            raise ValueError('Invalid unit type '+unit_type+' given (converted to lower-case string) (valid values are '+(', '.join(UNIT_TYPES))+')')
            
        
        units_of_type = []
        
        for guy in self.units:
            # For each of our units...
            
            if guy[0] == unit_type:
                # If the unit's type (the first element) is
                # equal to the requested unit type then we
                # add it to the list of positions
                units_of_type.append(guy)
                
            
        
    
    def getPositionsForType(self,unit_type):
        # Get the units of that type
        units_of_type = getUnitsOfType(unit_type)
        
        # Get the position (the second element) from
        # each unit's data.
        return [unit[1] for unit in units_of_type]
        
    
    def getUnitAtPos(self,pos):
        # We want to check to make sure that
        # the position is valid for the size
        # of a unit layout.
        x,y = pos
        
        if (x < 0 or y < 0 or
            x >= UNIT_LAYOUT_WIDTH or
            y >= UNIT_LAYOUT_HEIGHT):
            
            raise ValueError('Invalid unit position '+str(pos)+' given (coordinates must fit within a unit layout)')
            
        
        for guy in self.units:
            if pos == guy[1]:
                # The given position is equal to the
                # position of the current unit, so
                # we return that unit.
                return guy
                
            
        
        # Otherwise, we don't have a unit at that
        # position.
        
    

class Terrain(object):
    
    def __init__(self,tiles,spawns,tile_images,spawn_images):
        super(Terrain,self).__init__()
        
        self.drawRect = pygame.Rect(
            0,0,        # Position
            MAP_WIDTH + MAP_BORDER_X,   # Width
            MAP_HEIGHT + MAP_BORDER_Y   # Height
        )
        
        self.drawRect.width *= TILE_SIZE
        self.drawRect.height *= TILE_SIZE
        
        self.drawSurface = pygame.Surface(self.drawRect.size)
        
        self.drawSurface.fill(COLOR_KEY)
        self.drawSurface.set_colorkey(COLOR_KEY)
        
        # We create this variable here so we aren't
        # allocating and freeing memory constantly
        tile_image = None
        
        # The drawing position, which uses the
        # features of pygame.Rect to iterate
        # easily. That is, we can reposition
        # it very easily.
        draw_rect = pygame.Rect(
            0,0,
            TILE_SIZE // 2, # Width
            TILE_SIZE // 2 # Height
        )
        
        draw_rect.left = MAP_BORDER_WIDTH
        draw_rect.top = MAP_BORDER_HEIGHT
        
        
        for row in tiles:
            for tile_type,tile_index in row:
                tile_image = tile_images[tile_type][tile_index]
                
                tile_image = choice(tile_image)
                
                self.drawSurface.blit(tile_image,draw_rect.topleft)
                
                draw_rect.left = draw_rect.right
                
            
            draw_rect.left = MAP_BORDER_WIDTH
            draw_rect.top = draw_rect.bottom
            
        
        # - Now we draw the spawn points
        #   (or... we will once that's implemented!)
        
        # Put the drawing rectangle back at (0,0)
        # and resize it.
        draw_rect.topleft = 0,0
        draw_rect.size = TILE_SIZE,TILE_SIZE
        
        for pos,color in spawns:
            draw_rect.left = pos[0]*TILE_SIZE
            draw_rect.top = pos[1]*TILE_SIZE
            
            #image = spawn_images[color]
            #self.drawSurface.blit(image,draw_rect.topleft)
            
            break
            
        
    
    def draw(self,dest):
        # Easy drawing because we rendered this earlier
        dest.blit(self.drawSurface,self.drawRect.topleft)
        
    

class GameWorld(object):
    
    def __init__(self,units,terrain,trees,path_grid):
        super(GameWorld,self).__init__()
        
        self.pathGrid = path_grid
        
        self.terrain = terrain
        self.units = {'red':[],'blue':[]}
        
        self.trees = trees
        
        for guy in units['red']:
            self.units['red'].append(guy)
            guy.world = self
            
        
        for guy in units['blue']:
            self.units['blue'].append(guy)
            guy.world = self
            
        
        # List containing all of them so that we
        # can alternate during updates
        self.units['all'] = []
        
        for i in range(6):
            
            if i < len(self.units['red']):
                # Add the red unit
                self.units['all'].append(self.units['red'][i])
                
            if i < len(self.units['blue']):
                # Add the blue unit
                self.units['all'].append(self.units['blue'][i])
                
            
        
        # Stars for the background effect
        self.stars = []
        
    
    def coordsToNodeIndex(self,coords):
        x,y = coords
        i = 0
        
        x = int(round(x))
        y = int(round(y))
        
        if (x < 0 or y < 0 or
            x >= MAP_SIZE[0] or
            y >= MAP_SIZE[y]):
            
            raise ValueError('Invalid map coordinates '+str(coords)+' given (coordinates must be within the map')
            
        
    
    def refreshUnitBlocks(self):
        for node in self.pathGrid.nodes.values():
            node.blocked = False
            
        
        for guy in self.units['all']:
            grid_pos = tuple(guy.gridPos)
            
            # Law of Demeter? Screw that! This is easier!
            self.pathGrid.nodes[grid_pos].blocked = True
            
        
    
    def pathForUnit(self,unit,dest):
        # Unpack the coordinates
        dest_x,dest_y = dest
        
        # Round them and make them integers
        dest_x = int(round(dest_x))
        dest_y = int(round(dest_y))
        
        if (dest_x < 0 or dest_y < 0 or
            dest_x >= MAP_WIDTH or
            dest_y >= MAP_HEIGHT):
            
            # The coordinates are outside of the map
            raise ValueError('Invalid map coordinates '+str(dest)+' given (must be within the map\'s boundaries')
            
        
        # Pack the converted coordinates back into
        # the destination
        dest = dest_x,dest_y
        
        # Unpack the unit's position
        start_x, start_y = unit.pos
        
        # Round and convert the coordinates to integers
        start_x = int(round(start_x))
        start_y = int(round(start_y))
        
        # Pack the coordinates into the starting position
        start_pos = (start_x,start_y)
        
        start_node_index = self.coordsToNodeIndex(start_pos)
        end_node_index = self.coordsToNodeIndex(dest)
        
        start_node = self.pathGrid.nodes[start_node_index]
        end_node = self.pathGrid.nodes[end_node_index]
        
        path_nodes = []
        path = []
        
        return path
        
    
    def draw(self,dest):
        map_draw_surf = dest.subsurface(MAP_DRAW_RECT)
        hud_draw_surf = dest.subsurface(HUD_DRAW_RECT)
        
        hud_draw_surf.fill((96,48,0))
        map_draw_surf.fill((0,0,0))
        
        self.terrain.draw(map_draw_surf)
        
    
    def update(self,dt,input_state):
        # TODO: Handle input
        
        if input_state['select'] or input_state['command']:
            mouse_grid_pos = list(input_state['mouse pos'])
            
        
        for guy in self.units['all']:
            guy.update(dt)
            
        
        for star in self.stars:
            star.update(dt)
            
            if star.rect[0] > STAR_END_X:
                self.stars.remove(star)
                
            
        
    
    class Star(object):
        
        def __init__(self,pos,speed,brightness):
            super(Star,self).__init__()
            
            # We store the rectangle as a list of
            # four elements, which Pygame can use
            # as a Rect. This takes less memory.
            self.rect = list(pos)
            self.rect += [2,2]
            
            self.speed = speed
            
            # The color is the brightness three times.
            self.color = [brightness]*3
            
        
        def draw(self,dest):
            dest.fill(self.color,self.rect)
            
        
        def update(self,dt):
            self.rect[0] += int(round(self.speed*dt))
            
        
    

class GameFactory(object):
    
    def __init__(self):
        super(GameFactory,self).__init__()
        
    
    def makeUnit(self,pos,unit_type,faction):
        unit_type = str(unit_type).lower()
        
        unit_class = None
        
        if unit_type == 'swordsman':
            unit_class = Swordsman
            
        elif unit_type == 'archer':
            raise NotImplementedError('GameFactory.makeUnit() does not make archers yet')
            
        elif unit_type == 'wizard':
            raise NotImplementedError('GameFactory.makeUnit() does not make wizards yet')
            
        else:
            raise ValueError('Invalid unit type '+unit_type+' given (converted to lower-case string) (valid values are '+(', '.join(UNIT_TYPES))+')')
            
        
        images = loadUnitImages()[str(faction).lower()][unit_type]
        
        speed = 300
        health = 100
        
        new_unit = unit_class(pos,speed,health,faction,images)
        
        return new_unit
        
    
    def makeGameWorld(self,units,terrain):
        new_world = GameWorld(units,terrain)
        
        return new_world
        
    
    def makeTestWorld(self):
        new_world = None
        new_units = {'red':[],'blue':[]}
        
        new_terrain = Terrain(TEST_TERRAIN_TILES,[],loadTerrainTiles(),{'red':None,'blue':None})
        
        path_grid = PathGrid()
        
        # TODO: Build the path grid's nodes from the terrain
        
        new_world = GameWorld(new_units,new_terrain,[],path_grid)
        
        return new_world
        
    
