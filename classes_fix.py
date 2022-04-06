import math


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def cross(self, v):
        return Vector(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x
        )
    
    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def scale(self, c):
        return Vector(self.x * c, self.y * c, self.z * c)

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def norm(self):
        return self.scale(1 / self.mag())

    def visual(self):
        return Vector(self.x, -self.y, self.z)

    def round(self):
        return Vector(round(self.x, 20), round(self.y, 20), round(self.z, 20))

    def getComponents(self):
        return (self.x, self.y, self.z)


class Ball:
    def __init__(self, pos_v):
        # mass in slugs
        # diameter in feet
        self.pos = pos_v
        self.MASS = 0.00993566
        self.DIAMETER = 0.25
        self.AREA = math.pi * (self.DIAMETER / 2) ** 2
        # self.SEEM_HEIGHT = 
    
    def positionChangePitch(self, field, pitch, time_int):
        pitch.dx(field, self, time_int)
        pitch.dy(field, self, time_int)
        pitch.dz(field, self, time_int)
        delta = pitch.vel.scale(time_int)
        self.pos = self.pos.add(delta)
        if self.pos.z < 0:
            self.pos.z = 0
    
    def positionChangeHit(self, field, hit, time_int):
        if self.pos.y <= 0:
            self.pos.y = 0
            hit.vel_v.y = 0
            hit.dxGround(self, time_int)
            hit.dzGround(self, time_int)
        else:
            hit.dx(field, self, time_int)
            hit.dy(self, time_int)
            hit.dz(field, self, time_int)
        delta = hit.vel_v.scale(time_int)
        self.pos = self.pos.add(delta)

class Field:
    def __init__(self, fence_dimensions, altitude, temperature):
            self.PITCH_DISTANCE = 60.5
            # change HOME_PLATE to determine best field view
            # self.HOME_PLATE = 
            # self.FIRST_BASE = 
            # self.SECOND_BASE = 
            # self.THIRD_BASE = 
            self.PLATE_WIDTH = 17 / 12
            # altitude might end up being changed with fields, for now 0
            self.altitude = 0
            self.temp = temperature
            self.air_pressure = (2116 * ((59 - 0.00356 * (self.altitude) 
            + 459.7) / 518.6) ** 5.256)
            self.air_density = self.air_pressure / (1718 * (self.temp + 459.7))

class Pitch:
    def __init__(self, vel_v, spin_axis):
        self.vel = vel_v
        self.DRAG_COEFFICIENT = 0.35
        self.spin_axis = spin_axis
        # could add a function that calculates drag coefficient using
        # spin rate and velocity
        self.LIFT_COEFFICIENT = 0.15
    
    # def dragCoefficient(self):

    def dragForce(self, field, ball):
        scale = (-0.5 * self.DRAG_COEFFICIENT * 
                (field.air_density * self.vel.mag() ** 2)
                * ball.AREA)
        norm = self.vel.norm()
        return norm.scale(scale)

    def magnusEffect(self, field, ball):
        scale = (0.5 * self.LIFT_COEFFICIENT * field.air_density * ball.AREA
            * self.vel.mag() ** 2)
        cross = self.vel.cross(self.spin_axis).norm()
        return cross.scale(scale)

    def gravity(self, ball):
        return Vector(0,1,0).scale(-ball.MASS * 32.19)

    def dx(self, field, ball, time):
        fx_mag = self.magnusEffect(field, ball).x
        fx_drag = self.dragForce(field, ball).x
        a = (fx_mag + fx_drag) / ball.MASS
        self.vel.x += a * time
    
    def dy(self, field, ball, time):
        fy_mag = self.magnusEffect(field, ball).y
        fy_g = self.gravity(ball).y
        a = (fy_mag + fy_g) / ball.MASS
        self.vel.y += a * time

    def dz(self, field, ball, time):
        fz_mag = self.magnusEffect(field, ball).z
        fz_drag = self.dragForce(field, ball).z
        a = (fz_mag + fz_drag) / ball.MASS
        self.vel.z += a * time

class Swing:
    def __init__(self, height, z_value):
        self.height = 1.5 + 3.5 * (height)
        self.z = z_value + 8.5 / 12
        self.bat_radius = 1

    def batAngle(self):
        return  2* math.atan(self.z /2)

    def horizLaunchAngle(self):
        return self.batAngle()

    def vertLaunchAngle(self, ball):
        d_vert = ball.pos.y - self.height
        print(f'd_vert = {d_vert}, bat_radius = {self.bat_radius}')
        return math.asin(d_vert / self.bat_radius)

    def launchDirection(self, ball):
        horiz_angle = self.horizLaunchAngle()
        horiz_vector = Vector(-math.sin(horiz_angle), 0, math.cos(horiz_angle))
        vert_angle = self.vertLaunchAngle(ball)
        vert_vector = Vector(0, math.sin(vert_angle), math.cos(vert_angle))
        result_vector = horiz_vector.add(vert_vector).norm()
        return result_vector
    
    def power(self, ball):
        d = abs(self.height - ball.pos.y)
        power = ((self.bat_radius - d) / self.bat_radius)
        return power
    
    def exitVelo(self, ball):
        power = self.power(ball)
        exit_velo = (150 - 80) * power + 80
        return exit_velo

    def velocityVector(self, ball):
        return self.launchDirection(ball).scale(self.exitVelo(ball))

class Hit:
    def __init__(self, swing, ball):
        self.vel_v = swing.velocityVector(ball)
        self.DRAG_COEFFICIENT = 0.3
        self.coefficient_friction = 2

    def dragForce(self, field, ball):
        scale = (-0.5 * self.DRAG_COEFFICIENT * 
                (field.air_density * self.vel_v.mag() ** 2)
                * ball.AREA)
        norm = self.vel_v.norm()
        return norm.scale(scale)

    def gravity(self, ball):
        return Vector(0,1,0).scale(-ball.MASS * 32.19)

    def friction(self, ball):
        normal_force = ball.MASS * 32.19
        friction = normal_force * self.coefficient_friction
        norm = self.vel_v.norm()
        return norm.scale(-friction)

    def dx(self, field, ball, time):
        fx_drag = self.dragForce(field, ball).x
        a = fx_drag / ball.MASS
        self.vel_v.x += a * time
    
    def dy(self, ball, time):
        fy_g = self.gravity(ball).y
        a = fy_g / ball.MASS
        self.vel_v.y += a * time

    def dz(self, field, ball, time):
        fz_drag = self.dragForce(field, ball).z
        a = fz_drag / ball.MASS
        self.vel_v.z += a * time

    def dzGround(self, ball, time):
        fz_friction = self.friction(ball).z
        a = fz_friction / ball.MASS
        self.vel_v.z += a * time

    def dxGround(self, ball, time):
        fx_friction = self.friction(ball).x
        a = fx_friction / ball.MASS
        self.vel_v.x += a * time
     
time = 0
ball = Ball(Vector(0, 4.44, 0))
swing = Swing(0.84, 0)
# input z needs to be based off of the middle of the plate (8.5 in)
hit = Hit(swing, ball)
field = Field([], 0, 70)

# def getHitTrajectory():


def testHit():
    time = 0
    coordinates = []
    while time < 3:
        time += 0.1
        ball.positionChangeHit(field, hit, 0.1)
        #print(f'''coordinates = {ball.pos.getComponents()}, 
        #velocity = {hit.vel_v.getComponents()}''')
        coordinates.append(ball.pos.getComponents())



testHit()



