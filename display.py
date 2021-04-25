import pygame, sys
from pygame import *
from pygame import gfxdraw
import math

class Display():
    def __init__(self, fps):        
        self.windowSurface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('pretty')
        self.open = True
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.xoffset = 0
        self.scrolling = False

    def close(self):
        self.open = False
        pygame.quit()


    def render(self, w):
        if self.open:
            if self.fps:
                self.clock.tick_busy_loop(self.fps)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.open = False
                    pygame.quit()
                    return

            def adjusty(y):
                return int(720-y-self.yoffset)

            def adjustx(x):
                return int(x + self.xoffset)

            def thick(x0, y0, angle, length):
                x1 = x0 + math.sin(angle) * length
                y1 = y0 + math.cos(angle) * length

            heightmap = [w.heightmap[0].astype(int), w.heightmap[1].astype(int)]
            self.yoffset = 120
            max_height = self.yoffset + max(heightmap[1])

            if w.nodes[0]['x'] == 200: # reset
                 self.xoffset = 0
                 self.scrolling = False
            
            if w.nodes[0]['x'] + self.xoffset > 300:
                self.scrolling = True

            if self.scrolling:
                self.xoffset -= (w.nodes[0]['x'] + self.xoffset - 180)/15

            if w.nodes[0]['x'] + self.xoffset < 200:
                self.scrolling = False

            self.windowSurface.fill((44,59,90), pygame.Rect(0,720-max_height,1280, max_height))
                        
            move = self.xoffset % 102.4 - 102.4
            for i in range(0,36,2):
                pygame.gfxdraw.aapolygon(self.windowSurface, [(int(move + 51.2*(i+1)),720), (int(move + 51.2*(i+2)),720), (int(move + 51.2*(i+2)-max_height),720-max_height), (int(move + 51.2*(i+1)-max_height),720-max_height)], (53,71,109))
                pygame.gfxdraw.filled_polygon(self.windowSurface, [(int(move + 51.2*(i+1)),720), (int(move + 51.2*(i+2)),720), (int(move + 51.2*(i+2)-max_height),720-max_height), (int(move + 51.2*(i+1)-max_height),720-max_height)], (53,71,109))   

            x = int(self.xoffset)
            for i in range(len(heightmap[0])):
                self.windowSurface.fill((0,0,14), pygame.Rect(max(0,x),0,heightmap[0][i]+x-max(0,x), 720 - heightmap[1][i] - self.yoffset))
                x += heightmap[0][i]
                if x > 1280:
                    break
            
            x = int(self.xoffset)
            for i in range(len(heightmap[0])):
                if i != 0:
                    if heightmap[1][i-1] < heightmap[1][i]:
                        self.windowSurface.fill((53,71,109), pygame.Rect(max(0,x),720 - heightmap[1][i] - self.yoffset,14+x-max(0,x), heightmap[1][i] - heightmap[1][i-1]+14))
                    else:
                        self.windowSurface.fill((53,71,109), pygame.Rect(max(0,x-14),720 - heightmap[1][i-1] - self.yoffset,x-max(0,x-14), heightmap[1][i-1] - heightmap[1][i]+14))                    
                self.windowSurface.fill((53,71,109), pygame.Rect(max(0,x),720 - heightmap[1][i] - self.yoffset,heightmap[0][i]+x-max(0,x), 14))
                x += heightmap[0][i]
                if x > 1280:
                    break
            
            for i in range(len(w.angles)):
                thick(w.nodes[0]['x'], w.nodes[0]['y'], w.angles[i]*math.pi/180, w.readings[i])
          
            pygame.gfxdraw.aatrigon(self.windowSurface, adjustx(w.nodes[0]['x']),adjusty(w.nodes[0]['y']),adjustx(w.nodes[6]['x']),adjusty(w.nodes[6]['y']),adjustx(w.nodes[7]['x']),adjusty(w.nodes[7]['y']),(116,125,184))
            pygame.gfxdraw.filled_trigon(self.windowSurface, adjustx(w.nodes[0]['x']),adjusty(w.nodes[0]['y']),adjustx(w.nodes[6]['x']),adjusty(w.nodes[6]['y']),adjustx(w.nodes[7]['x']),adjusty(w.nodes[7]['y']),(116,125,184))

            pygame.gfxdraw.aatrigon(self.windowSurface, adjustx(w.nodes[9]['x']),adjusty(w.nodes[9]['y']),adjustx(w.nodes[8]['x']),adjusty(w.nodes[8]['y']),adjustx(w.nodes[6]['x']),adjusty(w.nodes[6]['y']),(116,125,184))
            pygame.gfxdraw.filled_trigon(self.windowSurface, adjustx(w.nodes[9]['x']),adjusty(w.nodes[9]['y']),adjustx(w.nodes[8]['x']),adjusty(w.nodes[8]['y']),adjustx(w.nodes[6]['x']),adjusty(w.nodes[6]['y']),(116,125,184))
                
            pygame.gfxdraw.aatrigon(self.windowSurface, adjustx(w.nodes[0]['x']),adjusty(w.nodes[0]['y']),adjustx(w.nodes[2]['x']),adjusty(w.nodes[2]['y']),adjustx(w.nodes[3]['x']),adjusty(w.nodes[3]['y']),(194,203,255))
            pygame.gfxdraw.filled_trigon(self.windowSurface, adjustx(w.nodes[0]['x']),adjusty(w.nodes[0]['y']),adjustx(w.nodes[2]['x']),adjusty(w.nodes[2]['y']),adjustx(w.nodes[3]['x']),adjusty(w.nodes[3]['y']),(194,203,255))

            pygame.gfxdraw.aatrigon(self.windowSurface, adjustx(w.nodes[5]['x']),adjusty(w.nodes[5]['y']),adjustx(w.nodes[4]['x']),adjusty(w.nodes[4]['y']),adjustx(w.nodes[2]['x']),adjusty(w.nodes[2]['y']),(194,203,255))
            pygame.gfxdraw.filled_trigon(self.windowSurface, adjustx(w.nodes[5]['x']),adjusty(w.nodes[5]['y']),adjustx(w.nodes[4]['x']),adjusty(w.nodes[4]['y']),adjustx(w.nodes[2]['x']),adjusty(w.nodes[2]['y']),(194,203,255))

            pygame.display.flip()
        else:
            print("don't render a closed window..")
