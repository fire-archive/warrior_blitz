#!/usr/bin/env python

from xml.etree import ElementTree

import os

from util import *

LEVEL_PATH = os.path.join(DEVDATA_PATH,'level')

TILESETS = ('floor','walls')
TILESET_PATHS = [os.path.join(LEVEL_PATH,name) for name in TILESETS]

def mungeLevelFile(lvl_path):
    print 'Munging level file at '+lvl_path
    
    in_file = ElementTree.parse(lvl_path)
    out_file_path = lvl_path.replace('.tmx','.xml')
    
    print 'Output path is '+out_file_path
    
    level_num = 0
    music_path = ''
    
    player_start = [0,0]
    lift_pos = [0,0]
    level_size = [0,0]
    baddies = []
    items = []
    doors = []
    terminals = []
    
    floor_tiles = []
    wall_tiles = []
    
    floor_tiles_str = ''
    wall_tiles_str = ''
    
    floor_gid_offset = 0
    wall_gid_offset = 0
    
    for prop_tag in in_file.find('properties').findall('property'):
        prop_name = prop_tag.get('name')
        prop_value = prop_tag.get('value')
        
        if prop_name.lower() == 'levelnum':
            level_num = int(prop_value)
            
        elif prop_name.lower() == 'music':
            music_path = prop_value
            
        
    
    print 'Level number is '+str(level_num)
    print 'Level uses music track '+music_path
    
    level_size[0] = int(in_file.getroot().get('width'))
    level_size[1] = int(in_file.getroot().get('height'))
    
    print 'Level size is '+str(level_size[0])+' by '+str(level_size[1])
    
    # TODO: Get the tileset gid offsets
    
    for layer_tag in in_file.findall('layer'):
        layer_name = layer_tag.get('name')
        
        to_add_to = None
        
        if layer_name.lower() == 'floor':
            print 'Parsing terrain tiles for the floor layer'
            
            to_add_to = floor_tiles
            
        elif layer_name.lower() == 'wall':
            print 'Parsing terrain tiles for the wall layer'
            
            to_add_to = wall_tiles
            
        else:
            continue
            
        
        rows = layer_tag.find('data').text.split('\n')
        tiles = None
        
        for row in rows:
            if len(row) == 0:
                # Empty row created by blindly using str.split()
                continue
                
            
            tiles = row.split(',')
            
            to_add_to.append([])
            
            for gid in tiles:
                if len(gid) == 0:
                    # Empty gid created the same was as empty rows above
                    continue
                    
                
                gid = int(gid)
                
                if to_add_to is floor_tiles:
                    gid -= floor_gid_offset
                    
                if to_add_to is wall_tiles:
                    gid -= wall_gid_offset
                    
                
                if gid < 0:
                    gid = 0
                
                to_add_to[-1].append(gid)
                
            
        
    
    print 'Converting lists of tile gids to CSV strings'
    
    floor_tiles_str = ';'.join(
        [','.join(
            [str(tile_gid) for tile_gid in floor_tiles]
        )]
    )
    
    wall_tiles_str = ';'.join(
        [','.join(
            [str(tile_gid) for tile_gid in wall_tiles]
        )]
    )
    
    for group_tag in in_file.findall('objectgroup'):
        grp_name = group_tag.get('name')
        
        print 'Parsing object group named '+grp_name
        
        # TODO: Get the entities
        
    
    print 'Building output document'
    
    out_file_xml = ElementTree.ElementTree()
    
    out_root = out_file_xml.getroot()
    
    out_root.tag = 'levelFile'
    
    print 'Creating terrain container tag'
    
    terrain_tag = ElementTree.SubElement(out_root,'terrain')
    
    floor_tag = ElementTree.SubElement(terrain_tag,'floor')
    wall_tag = ElementTree.SubElement(terrain_tag,'wall')
    
    floor_tag.text = floor_tiles_str
    wall_tag.text = wall_tiles_str
    
    print 'Creating player start tag with player starting at ' + str(player_pos)
    
    player_start_tag = ElementTree.SubElement(out_root,'playerStart')
    
    x_tag = ElementTree.SubElement(player_start_tag,'x')
    y_tag = ElementTree.SubElement(player_start_tag,'y')
    
    x_tag.text = str(player_start[0])
    y_tag.text = str(player_start[1])
    
    print 'Creating baddie container tag'
    
    baddies_tag = ElementTree.SubElement(out_root,'baddies')
    
    for bad_guy in baddies:
        break
        
    
    print 'Creating item container tag'
    
    items_tag = ElementTree.SubElement(out_root,'items')
    
    for item in items:
        break
        
    
    print 'Creating door container tag'
    
    doors_tag = ElementTree.SubElement(out_root,'doors')
    
    for door in doors:
        break
        
    
    print 'Creating terminal container tag'
    
    terminals_tag = ElementTree.SubElement(out_root,'terminals')
    
    for terminal in terminals:
        break
        
    
    print 'Creating lift position tag with lift at ' + str(lift_pos)
    
    lift_pos_tag = ElementTree.SubElement(out_root,'liftPos')
    
    x_tag = ElementTree.SubElement(lift_pos_tag,'x')
    y_tag = ElementTree.SubElement(lift_pos_tag,'y')
    
    x_tag.text = str(lift_pos[0])
    y_tag.text = str(lift_pos[1])
    
    print 'Opening output file at '+out_file_path
    
    out_file = open(out_file_path,'w')
    
    print 'Writing output file'
    
    out_file.write(ElementTree.tostring(out_file_xml))
    out_file.write('\n')
    
    out_file.close()
    
    print 'Done munging level file at '+lvl_path
    

def mungeTilesetFile(ts_path):
    print 'Munging tileset file at '+ts_path
    
    out_file_path = ts_path.replace('.tsx','.xml')
    
    in_file = ElementTree.parse(ts_path)
    
    out_file_xml = ElementTree.ElementTree()
    
    out_root = out_file_xml.getroot()
    
    out_root.tag = 'tilesetFile'
    
    # TODO: Write the tileset data
    
    out_file = open(out_file_path,'w')
    
    out_file.write(ElementTree.tostring(out_file_xml))
    out_file.write('\n')
    
    out_file.close()
    

def getLevelFiles():
    level_filenames = []
    
    for dirpath,dirnames,filenames in os.walk(LEVEL_PATH):
        
        for name in filenames:
            if name.endswith('.tmx'):# and 'template' not in name:
                print 'Found level file at '+os.path.relpath(os.path.join(dirpath,name))
                level_filenames.append(os.path.relpath(os.path.join(dirpath,name)))
                
            
        
    
    return level_filenames
    

def getTilesetFiles():
    tileset_filenames = []
    
    for dirpath,dirnames,filenames in os.walk(LEVEL_PATH):
        
        for name in filenames:
            if name.endswith('.tsx'):
                print 'Found tileset file at '+os.path.relpath(os.path.join(dirpath,name))
                tileset_filenames.append(os.path.relpath(os.path.join(dirpath,name)))
                
            
        
    
    return tileset_filenames
    

if __name__.lower() == '__main__':
    level_filenames = getLevelFiles()
    tileset_filenames = getTilesetFiles()
    
    for file_path in level_filenames:
        mungeLevelFile(file_path)
        
    
    for file_path in tileset_filenames:
        mungeTilesetFile(file_path)
        
    

