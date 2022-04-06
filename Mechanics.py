from classes_fix import*

time = 0
ball = Ball(Vector(0, 6, 60.5))
swing = Swing(0.71, 0)
# input z needs to be based off of the middle of the plate (8.5 in)

field = Field([], 0, 70)
timerDelay = 30
pitch = Pitch(Vector(0, 2, -130), Vector(-1, 0, 0).norm())

def getPitchTrajectory(ball, pitch, timerDelay):
    time = 0
    pitch_track = []
    ball_coord = []
    while  ball.pos.z > 0:
        time_int = timerDelay / 1000
        time += time_int
        ball.positionChangePitch(field, pitch, time_int)
        pitch_track.append(ball)
        ball_coord.append(ball.pos.getComponents())
    return ball_coord

ball_tuple = getPitchTrajectory(ball, pitch, timerDelay)[-1]
x, y, z = ball_tuple
hit_ball = Ball(Vector(x, y, z))

# def getHitTrajectory(hit_ball, hit, pitch, timerDelay):
#     if (hit_ball.pos.y - swing.height) > swing.bat_radius:
#         return 'missed'
#     else:
#         pitch = getPitchTrajectory(ball, pitch, timerDelay)
#         time = 0
#         hit_track = []
#         ball_coord = []
#         while  time < 10:
#             time_int = timerDelay / 1000
#             time += time_int
#             hit_ball.positionChangeHit(field, hit, time_int)
#             hit_track.append(hit_ball)
#             ball_coord.append(hit_ball.pos.getComponents())
#         return ball_coord


time = 0
swing = Swing(0.84, 0)
# ball = Ball(0,4,5)
# input z needs to be based off of the middle of the plate (8.5 in)
hit = Hit(swing, hit_ball)
field = Field([], 0, 70)

def getHitTrajectory(field, hit, hit_ball, timerDelay):
    time = 0
    coordinates = []
    while time < 5:
        time_int = timerDelay/1000
        time += time_int
        hit_ball.positionChangeHit(field, hit, time_int)
        #print(f'''coordinates = {hit_ball.pos.getComponents()}, 
        #velocity = {hit.vel_v.getComponents()}''')
        coordinates.append(hit_ball.pos.getComponents())
    return coordinates