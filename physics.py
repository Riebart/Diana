#!/usr/bin/env python

import sys
from math import sin, cos, pi, sqrt
from mimosrv import MIMOServer
from message import Message
from message import HelloMsg, PhysicalPropertiesMsg, VisualPropertiesMsg
from message import VisualDataEnableMsg, VisualMetaDataEnableMsg
from message import BeamMsg

class Vector3:
    def __init__(self, v, y=None, z=None):
        if y==None:
            self.x = v[0]
            self.y = v[1]
            self.z = v[2]
        else:
            self.x = v
            self.y = y
            self.z = z

    #def __init__(self, x, y, z):
        #self.x = x
        #self.y = y
        #self.z = z

    def length(self):
        r = self.x * self.x + self.y * self.y + self.z * self.z
        return sqrt(r)

    def length2(self):
        r = self.x * self.x + self.y * self.y + self.z * self.z
        return r

    def dist(self, v):
        x = v.x - self.x
        y = v.y - self.y
        z = v.z - self.z
        return sqrt(x * x + y * y + z * z)

    def dist2(self, v):
        x = v.x - self.x
        y = v.y - self.y
        z = v.z - self.z
        return x * x + y * y + z * z

    # Returns a unit vector that originates at v and goes to this vector.
    def ray(self, v):
        x = v.x - self.x
        y = v.y - self.y
        z = v.z - self.z
        m = sqrt(x * x + y * y + z * z)
        return Vector3([x / m, y / m, z / m])

    # In this case, self is the first vector in the cross product, because order
    # matters here
    def cross(self, v):
        rx = self.y * v.z - self.z * v.y
        ry = self.z * v.x - self.x * v.z
        rz = self.x * v.y - self.y * v.x
        return Vector3([rx, ry, rz])

    @staticmethod
    # Combines a linear combination of a bunch of vectors
    def combine(vecs):
        rx = 0.0
        ry = 0.0
        rz = 0.0
        
        for v in vecs:
            rx += v[0] * v[1].x
            ry += v[0] * v[1].y
            rz += v[0] * v[1].z

        return Vector3([rx, ry, rz])

    def normalize(self):
        l = self.length()
        self.x /= l
        self.y /= l
        self.z /= l

    def scale(self, c):
        self.x *= c
        self.y *= c
        self.z *= c

    # Adds v to self.
    def add(self, v, s = 1):
        self.x += s * v.x
        self.y += s * v.y
        self.z += s * v.z

    #override +
    def __add__(self, other):
        return Vector3([self.x+other.x, self.y+other.y, self.z+other.z])

    def sub(self, v):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z

    #override -
    def __sub__(self, other):
        return Vector3([self.x-other.x, self.y-other.y, self.z-other.z])

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    #overrid []
    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z

        raise IndexError('Vector3 has only 3 dimensions')

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise IndexError('Vector3 has only 3 dimensions')

# ### TODO ### implement grids, this ties into physics, but the properties
#  need to be added here.
class PhysicsObject:
    @staticmethod
    def is_big_enough(mass, min_distance):
        if mass == None or min_distance == None:
            return 0

        f = 6.67384e-11 * mass / min_distance

        # ### PARAMETER ### GRAVITY CUTOFF
        if f >= 0.01:
            return 1
        else:
            return 0
            
    def __init__(self, universe,
                    position = [ 0.0, 0.0, 0 ],
                    velocity = [ 0.0, 0.0, 0 ],
                    orientation = [ 0.0, 0.0, 0.0 ],
                    mass = 10.0,
                    radius = 1.0,
                    thrust = [0.0, 0.0, 0.0]):
        self.phys_id = universe.get_id()
        self.position = Vector3(position)
        self.velocity = Vector3(velocity)
        self.orientation = Vector3(orientation)
        self.mass = mass
        self.radius = radius
        self.thrust = Vector3(thrust)
        self.art_id = None
        self.emits_gravity = PhysicsObject.is_big_enough(self.mass, self.radius)

    @staticmethod
    def collide(obj1, obj2, dt):
        # ### TODO ### Properly handle forces here.

        # Currently we treat dt and forces as small enough that they can be neglected,
        # and assume that they won't change teh trajectory appreciably over the course
        # of dt

        # What we do is get the line segments that each object will trace outside
        # if they followed their current velocity for dt seconds.

        # We then find the minimum distance between those two line segments, and
        # compare that with the sum of the radii (the minimum distance the objects
        # need to be away from each other in order to not collide).

        # Because the parameters for the parameterizations of the line segments
        # will be in [0,1], we'll need to scale the velocity by dt. If we
        # get around to handling force application we need to scale the acceleration
        # vector by 0.5*dt^2, and then apply a parameter of t^2 to that term.

        # FYI: Mathematica comes back with about 20,000 arithmetic operations per
        # parameter... I don't think I'm going to bother. If errors start to get
        # too high (as in, noticed in gameplay), then forcibly slow down time to
        # keep the physics ticks fast enough to keep collision error in check.

        # Parameters for force-less trajectories are found for object 1 and 2 (t and v)
        # thanks to some partial differentiation of parameterizations of the trajectories
        # using a parameter for each object. Note that this will find the global minimum
        # and the parameters that come back likely won't be in the [0,1] range.

        # If eiher of the parameters are outside of the range, you should check
        # the endpoints for the minimum in the applicable range. If both parameters
        # are in [0,1], then you can skip endpoing checking. Yay!

        # Notes on shorthand here. v1 = (x, y, z), and v2 = (a, b, c). '.' means
        # dot product, and 'x' means cross product.

        # t = ((o1.v1-o2.v1) (v2.v2)-(o1.v2-o2.v2)(v1.v2))
        #     --------------------------------------------
        #              ((v1.v2)^2-(v1.v1) (v2.v2))
        
        # v = (o1-o2).(c{-x z,-y z,x^2+y^2}+b{-x y,x^2+z^2,-y z}+a{y^2+z^2,-x y,-x z})
        #     ------------------------------------------------------------------------
        #                          (v2 x v1).(v2 x v1)
        
        pass

    def collision(self, obj, dt):
        pass

class SmartPhysicsObject(PhysicsObject):
    def __init__(self, universe, client,
                    position = [ 0.0, 0.0, 0 ],
                    velocity = [ 0.0, 0.0, 0 ],
                    orientation = [ 0.0, 0.0, 0.0 ],
                    mass = 10.0,
                    radius = 1.0,
                    thrust = [0.0, 0.0, 0.0]):
        PhysicsObject.__init__(self, universe, position, velocity, orientation, mass, radius, thrust)
        self.client = client
        self.universe = universe
        self.sim_id = None
        self.vis_data = 0
        self.vis_meta_data = 0

    def handle(self, client):
        msg = Message.get_message(client)

        if isinstance(msg, HelloMsg):
            if msg.endpoint_id == None:
                return

            self.sim_id = msg.endpoint_id
            HelloMsg.send(client, self.phys_id)

        # If we don't have a sim_id by this point, we can't accept any of the
        # following in good conscience...
        if self.sim_id == None:
            return

        if isinstance(msg, PhysicalPropertiesMsg):
            if msg.mass:
                self.mass = msg.mass

            if msg.position:
                self.position = Vector3(msg.position)

            if msg.velocity:
                self.velocity = Vector3(msg.velocity)

            if msg.orientation:
                self.orientation = Vector3(msg.orientation)

            if msg.thrust:
                self.thrust = Vector3(msg.thrust)

            if msg.radius:
                self.radius = msg.radius

            new_emits = PhysicsObject.is_big_enough(self.mass, self.radius)
            diff = self.emits_gravity - new_emits

            if diff != 0:
                self.universe.update_attractor(self)

            #PhysicalPropertiesMsg.send(f, [self.mass, self.position.x, self.position.y, self.position.z, self.velocity.x, self.velocity.y, self.velocity.z, self.orientation.x, self.orientation.y, self.orientation.z, self.thrust.x, self.thrust.y, self.thrust.z, self.radius ])

        elif isinstance(msg, VisualPropertiesMsg):
            if self.art_id == None:
                self.art_id = self.universe.curator.register_art(msg.mesh, msg.texture)
            else:
                self.universe.curator.update_art(self.art_id, msg.mesh, msg.texture)
                self.universe.curator.attach_art_asset(self.art_id, self.phys_id)

        elif isinstance(msg, VisualDataEnableMsg):
            changed = msg.enabled - self.vis_data
            self.vis_data = msg.enabled

            if changed != 0:
                self.universe.register_for_vis_data(self, self.vis_data)

        elif isinstance(msg, VisualMetaDataEnableMsg):
            changed = msg.enabled - self.vis_meta_data
            self.vis_meta_data = msg.enabled

            if changed != 0:
                self.universe.curator.register_client(self, self.vis_meta_data)

        elif isinstance(msg, BeamMsg):
            beam = Beam.build(msg, self.universe)
            self.universe.add_beam(beam)

class Beam:
    def __init__(self, universe,
                    origin, normals,
                    direction, velocity,
                    energy):
        self.universe = universe
        self.origin = origin
        self.front_position = origin
        self.normals = normals
        self.direction = direction
        self.velocity = velocity
        self.energy = energy

    @staticmethod
    def collide(b, obj, dt):
        # ### TODO ### Properly handle forces here for the physical object

        # To detect a collition, we grab the normals from the beam, and translate
        # the object's position to 'beam-space' by subtracting the beam's origin
        # from the object's position.

        # We dot the resulting vector with each of the beam's normal vectors
        # and examine the results. Sicne the normals are unit-vectors, the result
        # is the length of the vector along each normal to the object's position.

        # Since the object could be positioned outside of the beam's frustrum,
        # but still extend into the beam based on its radius, we check that each
        # of the dot procuts is >= -obj.radius. If that is satisfied for all
        # of the dot products, then the object extends (at least partially)
        # into the beam.

        # Now we need to check that it is actually in the portion of space that
        # the beam will be carving out during dt. To do this we take the beam's
        # front_position, or the centre of the wave-front at the start of the tick
        # and verify that the object's position is between front_position and
        # front_position + dt * beam velocity. Do this by grabbing a unit vector
        # along velocity (direction), dotting the (object's position - front_position)
        # with it, and then comparing the result with dt * beam's speed. The dot
        # product should be in [-obj.radius, dt * beam_speed + obj.radius]
        # (the closed interval)

        # If both of the above conditions are met, then we have an object-beam
        # collision

        # computing the amount of suface area is another topic for another day!
        # ### TODO ### Collision surface area
        
        pass

    def collision(self, obj, dt):
        pass

    def tick(self, dt):
        self.front_position.add(self.velocity, dt)

    @staticmethod
    def build(msg, universe):
        direction = Vector3(msg.velocity)
        direction.scale(direction.length())
        up = Vector3(msg.up)
        up.scale(up.length())
        normals = []

        # Ok, so now we need to convert the direction, up, and spread angles
        # into plane normals. Yay!

        # First we cross the direction and up to get a vector pointing 'horizontally'.
        # this vector points 'right', or clockwise, when looking down the up vector.
        # The order of the cross product here doesn't really matter, but it
        # helps to follow some reasoning.
        right = direction.cross(up)

        # Once we have right, we can find vectors inside of the planes, thanks
        # to some basic trig. Here, cosine is along the direction, and sine
        # is along the right vector.

        sh = sin(msg.spread_h)
        ch = cos(msg.spread_h)
        sv = sin(msg.spread_v)
        cv = cos(msg.spread_v)

        # The vertical planes (those on the right and left boundaries of the beam)
        # are obtained by combining the direction and horizontal vector.
        # That gets us a vector inside the plane
        plane_r = Vector3.combine([[ch, direction], [sh, right]])
        plane_l = Vector3.combine([[ch, direction], [-sh, right]])

        # Similarly, the up vector gets us the top and bottom in-plane vectors
        plane_t = Vector3.combine([[ch, direction], [sh, up]])
        plane_b = Vector3.combine([[ch, direction], [-sh, up]])

        # We can get the normal vectors through another cross product, this time
        # between the in-plane vectors, and the right/up vectors.

        # The order of vectors in the cross product is important here. Reversing the
        # order reverses the direction of the resulting vector, pointing outside of
        # bounded volume, instead of inside.

        # Following the right-hand rule, point your index finger along the first
        # vector, middle finger along the second, and the result is your thumb

        # This means that we need the in-plane vectors first. For the left and right
        # planes, the up vector should be in them, so we can cross them to
        # get a normal. Similarly, the right vector is in the top and bottom planes.

        normals.append(plane_r.cross(up))
        normals.append(plane_l.cross(up))
        normals.append(plane_b.cross(right))
        normals.append(plane_t.cross(right))

        # Now we have enough information to build our beam object.

        return Beam(universe, Vector3(msg.origin), normals, direction, Vector3(msg.velocity), msg.energy)