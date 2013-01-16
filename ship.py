#!/usr/bin/env python

from vector import Vector3
from spaceobj import *
import math
from mimosrv import MIMOServer
import message
        
import sys

class Ship(SmartObject):
    def __init__(self, osim, osid=0, uniid=0, type="dummy-ship", port=None):
        SmartObject.__init__(self, osim, osid, uniid)
        self.name = "Unkown"
        self.type = type
        self.max_missiles = 10
        self.cur_missiles = self.max_missiles
        self.radius = 20.0 #20m?
        self.mass = 100000.0 #100 Tonnes?
        self.energy = 1000
        
        self.listen_port = port

        
    def do_scan(self):
        pass
    
    def handle_visdata(self, mess):
        #as though there is no way of getting the original string...
        new_mess = "VISDATA\n%d\n%f\n%f\n%f\n%f\n%f\n%f\n%f\n" % (
            mess.phys_id,
            mess.radius,
            mess.position[0], mess.position[1], mess.position[2],
            mess.orientation[0], mess.orientation[1], mess.orientation[2] )
        for client in self.vis_clients:
            client.send(new_mess)
    
    #might need some locking here
    def handle_client(self, client):
        if client not in self.clients:
            self.clients.append(client)
        
        mess = message.Message.get_message(client)[0]

        
        if isinstance(mess, message.VisualDataEnableMsg):
            if mess.enabled == 1:
                if client not in self.vis_clients:
                    self.vis_clients.append(client)
                    print str(len(self.vis_clients))
                if self.vis_enabled ==  False:
                    self.enable_visdata()
                    self.vis_enabled = True
            else:
                #delete from vis_clients
                if client in self.vis_clients:
                    self.vis_clients.remove(client)
                if self.vis_enabled and len(self.vis_clients) < 1:
                    self.disable_visdata()
                    self.vis_enabled = False
                    
        sys.stdout.flush()
        
    #def handle_phys(self, mess):
        #print "Ship collided with something! %d, %d" % (self.uniid, self.osid)
        #pass
        
    def run(self):
        if (self.listen_port != None):
            self.client_net = MIMOServer(self.handle_client, port = self.listen_port)
            self.clients = []
            self.vis_clients = []
            self.vis_enabled = False
            
            self.client_net.start()
            
        SmartObject.run(self)
        
    def fire_laser(self, direction, h_focus=math.pi/6, v_focus=math.pi/6, power=100.0):
        
        laser = WeaponBeam(self.osim)
        
        self.init_beam(laser, power, 299792458.0, direction, h_focus, v_focus)
        
        self.fire_beam(laser)
    
    #fire a dumb-fire missile in a particular direction. thrust_power is a scalar
    def fire_missile(self, direction, thrust_power):
        if (self.cur_missiles > 0):
            missile = Missile(self.osim)

            #set the initial position of the missile some small distance outside the ship
            tmp = direction.ray(Vector3((0.0,0.0,0.0)))
            tmp.scale((self.radius + missile.radius) * -1.1)
            missile.location = self.location + tmp
            
            #should missile have our initial velocity?
            missile.velocity = self.velocity
            
            tmp = direction.ray(Vector3((0.0,0.0,0.0)))
            tmp.scale(thrust_power * -1)                
            missile.thrust = tmp        
            missile.orient = direction
                    
            self.osim.spawn_object(missile)
            
            self.cur_missiles -= 1
            
        
            #shouldn't really return this, but for now, testing, etc
            return missile
        
        return None
        
    def fire_homing(self, direction, thrust_power):
        missile = HomingMissile1(self.osim)

        #set the initial position of the missile some small distance outside the ship
        tmp = direction.ray(Vector3((0.0,0.0,0.0)))
        tmp.scale((self.radius + missile.radius) * -1.1)
        missile.location = self.location + tmp
        
        #should missile have our initial velocity?
        missile.velocity = self.velocity
        
        tmp = direction.unit()
        tmp.scale(thrust_power)                
        missile.thrust = tmp        
        missile.orient = direction
                
        self.osim.spawn_object(missile)
        
        return missile
        #self.cur_missiles -= 1
    