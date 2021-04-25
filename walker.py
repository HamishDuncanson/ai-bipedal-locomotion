import math
import random
import numpy as np

newmeans = np.array([-50.535300023391464, 55.92153702803219, 9.065537584044561, -0.7238773753320015, 8.568810649931123, 48.439194338668024, 4.25041782116836, -12.688433565428664, -0.234947636907883, 20.905880714144722, -76.72538451979965, -52.35712147806885, -151.43306786382882, -100.6212193301801, -80.74741734129047, -52.582302465721256, -151.32331547915092, -101.41309404889196, 0.3475042024165834, 0.23705920717736786, 0.333290704654285, 0.3278044625535973, 0.2350166184219108, 0.3247712870198122, 0.3897355606166046, 0.3076537150264171, 0.17957191237366704, 0.3089198495114038, -5.7554027563512955, -5.813646488819407, -5.714640991990096, -5.738803596767667, -5.78588582238552, -5.7475590629693505, -5.510425777958458, -5.62155183086436, -5.697281426419088, -5.530125444598072, 95.7836596835933, 50.94629990480663, 93.71267884089221, 52.04940037134359, 0., 0., 200., 200., 200., 200., 200., 200., 200., 200., 200., 200., 200., 200., 0., 0., 0., 0.])
newsds = np.array([4.698658542703221, 26.512992715572327, 17.27048639799284, 51.21964714712653, 34.00311168152651, 29.90181356501305, 18.48096374074994, 53.87938771432319, 36.53966946817321, 8.327632627647839, 18.75228161125278, 3.6414885984610006, 9.481061587243921, 8.699638165765851, 17.360689175145602, 3.9242295347058325, 11.23157840118195, 8.072289588182073, 0.9725552741139192, 1.8502855451953293, 2.638749666839243, 0.9955055750265137, 1.4723672013497666, 1.4898155173075047, 2.7954399821996705, 0.9714346738060731, 1.8211821666738834, 1.5492953407817556, 2.318289724116721, 2.564053708803567, 4.350340293155056, 3.2602045916518243, 6.954146500866168, 5.325304686872696, 4.941022376161215, 3.5158352310379315, 7.449785308598848, 5.760642199721098, 8.28696515233257, 7.554006682817093, 8.452585809247191, 6.395646836363941, 1., 1., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 100., 1., 1., 1., 1.])

class Walker():
    def __init__(self, fps = False):
        self.ticks = 0
        self.grav = [0,-0.45]
        self.iters = 25
        self._max_episode_steps = 1000
        self.angles = np.linspace(100, 210, 12)
        self.readings = np.zeros(len(self.angles))
        self.moving_links = [1, 5, 9, 13]
        self.vels = np.zeros(4)
        self.sensors = [0, 0]
        self.max_lidar = 400
        self.power = 0.55
        self.pfric = 0.9
        if fps:
            self.display = Display(fps)
        else:
            self.display = False

    def scale(self, state):
        return (state-newmeans)/newsds
            
    def reset(self):
        self.ticks = 0
        self.nodes = []
        self.links = []
        self.spawn()
        if self.display:
            self.display.reset()
        self.heightmap = [np.array([100000]), np.array([6])]
        return self.state()

    def spawn(self):
        self.addnode(200.000000, 190.000000, 5, 1)
        self.addnode(144.098301, 190.000000, 1, 0)
        self.addnode(270.710678, 119.289322, 1, 1)
        self.addnode(217.677670, 136.966991, 1, 1)
        self.addnode(200.000000,  48.578644, 1, 2)
        self.addnode(217.677670, 101.611652, 1, 1)
        self.addnode(270.710678, 119.289322, 1, 1)
        self.addnode(217.677670, 136.966991, 1, 1)
        self.addnode(200.000000,  48.578644, 1, 2)
        self.addnode(217.677670, 101.611652, 1, 1)
        for node in self.nodes:
            node['lastx'] += np.random.uniform(-1, 1)
            node['lasty'] += np.random.uniform(-1, 1)
        self.addlink(0, 1)
        self.addlink(3, 1)
        self.addlink(0, 2)
        self.addlink(0, 3)
        self.addlink(2, 3)
        self.addlink(5, 3)
        self.addlink(4, 2)
        self.addlink(4, 5)
        self.addlink(2, 5)
        self.addlink(7, 1)
        self.addlink(0, 6)
        self.addlink(0, 7)
        self.addlink(6, 7)
        self.addlink(9, 7)
        self.addlink(8, 6)
        self.addlink(8, 9)
        self.addlink(6, 9)
    
    def close(self):
        if self.display:
                self.display.close()

    def distance(self, a, b):
        return ((a['x']-b['x'])**2+(a['y']-b['y'])**2)**0.5

    def addnode(self, x, y, m, c):
        self.nodes.append({'x':x, 'y':y, 'lastx':x, 'lasty':y, 'mass':m, 'collision':c})

    def addlink(self, a, b):
        d = self.distance(self.nodes[a], self.nodes[b])
        self.links.append({'a':a, 'b':b, 'dist':d})

    def verlet(self):
        self.sensors = [0, 0]
        for i in range(len(self.nodes)):
            xv=self.nodes[i]['x']-self.nodes[i]['lastx']
            yv=self.nodes[i]['y']-self.nodes[i]['lasty']
            if i != 1:
                index = 0
                trav = self.heightmap[0][0]
                while self.nodes[i]['x'] > trav:
                    index += 1
                    trav += self.heightmap[0][index]
                
                if self.nodes[i]['y'] < self.heightmap[1][index]: 
                    if i != 4 and i != 8:
                        return True
                    else:
                        lastindex = 0
                        lasttrav = self.heightmap[0][0]
                        while self.nodes[i]['lastx'] > lasttrav:
                            lastindex += 1
                            lasttrav += self.heightmap[0][lastindex]
                        if lastindex == index:
                            pass
                        elif lastindex + 1 == index:
                            border = lasttrav 
                            ratio = (border - self.nodes[i]['lastx']) / (self.nodes[i]['x'] - self.nodes[i]['lastx'])
                            check_height = ratio * self.nodes[i]['y'] + (1 - ratio) * self.nodes[i]['lasty']
                            if check_height < self.heightmap[1][index]:
                                return True
                        elif lastindex - 1 == index:
                            border = trav
                            ratio = (border - self.nodes[i]['lastx']) / (self.nodes[i]['x'] - self.nodes[i]['lastx'])
                            check_height = ratio * self.nodes[i]['y'] + (1 - ratio) * self.nodes[i]['lasty']
                            if check_height < self.heightmap[1][index]:
                                return True
                        overlap = self.heightmap[1][index] - self.nodes[i]['y']
                        xv = 0
                        self.nodes[i]['y'] = self.heightmap[1][index]
                        if yv < 0:
                             yv = 0
                        if i == 4:
                            self.sensors[0] = 1
                        else:
                            self.sensors[1] = 1                 
            self.nodes[i]['lastx']=self.nodes[i]['x']
            self.nodes[i]['lasty']=self.nodes[i]['y']
            self.nodes[i]['x']=self.nodes[i]['x']+xv+self.grav[0]
            self.nodes[i]['y']=self.nodes[i]['y']+yv+self.grav[1]
        return False

    def solve(self, link):
        a = self.nodes[link['a']]
        b = self.nodes[link['b']]
        dx = a['x'] - b['x']
        dy = a['y'] - b['y']
        d = (dx**2 + dy**2)**0.5
        difference = (link['dist'] - d) / d
        im_a = 1 / a['mass']
        im_b = 1 / b['mass']
        scalar_a = im_a / (im_a + im_b)
        scalar_b = 1 - scalar_a
        a['x'] += scalar_a * difference * dx
        a['y'] += scalar_a * difference * dy
        b['x'] -= scalar_b * difference * dx
        b['y'] -= scalar_b * difference * dy

    def exper(self, action):
        self.vels *= self.pfric
        self.vels += np.clip(action, -1, 1) * self.power
        for i in range(4):
            link = self.links[self.moving_links[i]]
            link['dist'] = np.clip(link['dist'] + self.vels[i], 0, 140)
            self.vels[i] *= 1 - (link['dist'] in [0, 140])

    def recursive_lidar(self, x, y, angle, ind, max_len):
        if y < self.heightmap[1][ind]:
            return 0
        if angle > math.pi:
            angle -= math.pi
            down = x/math.tan(angle)
            if down > y - self.heightmap[1][ind]:
                return min(max_len, (y - self.heightmap[1][ind])/math.cos(angle))
            else:
                d = (x**2+down**2)**0.5
                if d > max_len:
                    return max_len
                else:
                    return d + self.recursive_lidar(self.heightmap[0][ind-1], y-down, angle+math.pi, ind-1, max_len - d)
        else:
            angle = math.pi-angle
            down = (self.heightmap[0][ind]-x)/math.tan(angle)
            if down > y - self.heightmap[1][ind]:
                return min(max_len, (y - self.heightmap[1][ind])/math.cos(angle))
            else:
                d = ((self.heightmap[0][ind]-x)**2+down**2)**0.5
                if d > max_len:
                    return max_len
                else:
                    return d + self.recursive_lidar(0, y-down, math.pi-angle, ind+1, max_len - d)

    def lidar(self):        
        index = 0
        trav = self.heightmap[0][0]
        while self.nodes[0]['x'] > trav:
            index += 1
            trav += self.heightmap[0][index]
        for i in range(len(self.angles)):
            ang = self.angles[i]
            if ang == 180:
                self.readings[i] = np.clip(self.nodes[0]['y'] - self.heightmap[1][index], 0, 400)
            else:
                self.readings[i] = self.recursive_lidar(self.nodes[0]['x'] - trav + self.heightmap[0][index], self.nodes[0]['y'], ang * math.pi / 180, index, 400)

    def state(self):
        state = [self.nodes[i]['x']-self.nodes[0]['x'] for i in range(1, len(self.nodes))]
        state += [self.nodes[i]['y']-self.nodes[0]['y'] for i in range(1, len(self.nodes))]
        state += [n['lasty'] - n['y'] for n in self.nodes]
        state += [n['lastx'] - n['x'] for n in self.nodes]
        state += [self.links[i]['dist'] for i in [1, 5, 9, 13]]
        state += self.sensors
        self.lidar()
        return self.scale(np.concatenate([np.array(state), self.readings, self.vels]))

    def consolidate_heightmap(self):
        while self.nodes[0]['x']-325 > self.heightmap[0][0]:
            if len(self.heightmap[0])==1:
                break
            self.heightmap[0][1] += self.heightmap[0][0]
            self.heightmap[0] = self.heightmap[0][1:]
            self.heightmap[1] = self.heightmap[1][1:]

    def step(self, action):
        self.consolidate_heightmap()
        progress = self.nodes[0]['x']
        if self.display:
            self.display.render(self)
        self.exper(action)
        for i in range(self.iters):
            for k in range(len(self.links)):
                self.solve(self.links[k])
        self.ticks += 1
        dead = self.verlet()
        reward = (self.nodes[0]['x'] - progress)/5
        return self.state(), reward, self.ticks == self._max_episode_steps or dead
