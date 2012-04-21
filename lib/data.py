import pygame
import pygame.image
import pygame.mixer

from xml.etree import ElementTree

import os

from util import *

DATA_PATH = os.path.join(BASE_PATH,'data')

COLOR_KEY = (255,0,255)

imagesLoaded = {}
soundsLoaded = {}

def loadImage(img_path):
    img_path = os.path.relpath(os.path.join(DATA_PATH,'image',img_path))
    
    if img_path not in imagesLoaded:
        imagesLoaded[img_path] = pygame.image.load(img_path).convert()
        imagesLoaded[img_path].set_colorkey(COLOR_KEY)
        
    
    return imagesLoaded[img_path]
    

def loadUnitImages():
    if '_unit' in imagesLoaded:
        return imagesLoaded['_unit']
        
    
    factions = ('blue',)
    units = ('swordsman',)
    
    names = []
    
    for fac in factions:
        for unit in units:
            names.append(fac+'-'+unit)
            
        
    
    src_image = None
    frame_rect = pygame.Rect(0,0,48,32)
    
    images = {}
    
    for name in names:
        src_image = loadImage(os.path.join('unit',(name+'.png')))
        
        
    
    imagesLoaded['_unit'] = images
    return images
    

def loadTerrainTiles():
    if '_terrain' in imagesLoaded:
        return imagesLoaded['_terrain']
        
    
    # Dict containing all of the images
    images = {}
    tiles = []
    
    src_image = loadImage(os.path.join('terrain','tiles.png'))
    tile_rect = pygame.Rect(0,0,12,12)
    
    while tile_rect.bottom <= src_image.get_height():
        
        tile_rect.left = 0
        
        while tile_rect.right <= src_image.get_width():
            tiles.append(src_image.subsurface(tile_rect))
            
            tile_rect.left = tile_rect.right
            
        
        tile_rect.top = tile_rect.bottom
        
    
    images['grass'] = [[]]
    
    for i in range(0,8):
        images['grass'][0].append(tiles[i])
        
    
    images['dirt'] = []
    
    images['dirt'].append([tiles[15],tiles[20],tiles[25]])
    
    images['dirt'].append([tiles[16],tiles[21],tiles[26]])
    images['dirt'].append([tiles[17],tiles[22],tiles[27]])
    images['dirt'].append([tiles[18],tiles[23],tiles[28]])
    images['dirt'].append([tiles[19],tiles[24],tiles[29]])
    
    images['dirt'].append([tiles[31],tiles[36],tiles[41]])
    images['dirt'].append([tiles[32],tiles[37],tiles[42]])
    images['dirt'].append([tiles[33],tiles[38],tiles[43]])
    images['dirt'].append([tiles[34],tiles[39],tiles[44]])
    
    images['dirt'].append([tiles[46],tiles[51],tiles[56]])
    images['dirt'].append([tiles[47],tiles[52],tiles[57]])
    images['dirt'].append([tiles[48],tiles[53],tiles[58]])
    images['dirt'].append([tiles[49],tiles[54],tiles[59]])
    
    images['rock'] = []
    
    images['rock'].append([tiles[60],tiles[65],tiles[70]])
    
    images['rock'].append([tiles[61],tiles[66],tiles[71]])
    images['rock'].append([tiles[62],tiles[67],tiles[72]])
    images['rock'].append([tiles[63],tiles[68],tiles[73]])
    images['rock'].append([tiles[64],tiles[69],tiles[74]])
    
    images['rock'].append([tiles[76],tiles[81],tiles[86]])
    images['rock'].append([tiles[77],tiles[82],tiles[87]])
    images['rock'].append([tiles[78],tiles[83],tiles[88]])
    images['rock'].append([tiles[79],tiles[84],tiles[89]])
    
    images['rock'].append([tiles[91],tiles[96],tiles[101]])
    images['rock'].append([tiles[92],tiles[97],tiles[102]])
    images['rock'].append([tiles[93],tiles[98],tiles[103]])
    images['rock'].append([tiles[94],tiles[99],tiles[104]])
    
    images['border'] = []
    
    images['border'].append([tiles[105],tiles[109],tiles[113]])
    images['border'].append([tiles[106],tiles[110],tiles[114]])
    images['border'].append([tiles[107],tiles[111],tiles[115]])
    images['border'].append([tiles[108],tiles[112],tiles[116]])
    
    images['border'].append([tiles[120],tiles[124],tiles[128]])
    images['border'].append([tiles[121],tiles[125],tiles[129]])
    images['border'].append([tiles[122],tiles[126],tiles[130]])
    images['border'].append([tiles[123],tiles[127],tiles[131]])
    
    return images
    
