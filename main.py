from math import cos, pi, sin
import time
import turtle

Colors = [
  "#D0E7F5",
  "#D9E7F4",
  "#D6E3F4",
  "#BCDFF5",
  "#B7D9F4",
  "#C3D4F0",
  "#9DC1F3",
  "#9AA9F4",
  "#8D83EF",
  "#AE69F0",
  "#D46FF1",
  "#DB5AE7",
  "#D911DA",
  "#D601CB",
  "#E713BF",
  "#F24CAE",
  "#FB79AB",
  "#FFB6C1",
  "#FED2CF",
  "#FDDFD5",
  "#FEDCD1"      
]

# Supporting functions / class
class Arc:
  def __init__(self, Color, Velocity, LastImpactTime, NextImpactTime):
    self.Color = Color
    self.Velocity = Velocity
    self.LastImpactTime = LastImpactTime
    self.NextImpactTime = NextImpactTime

def CalculateVelocity(index):
  NumOfCycles = MaxCycles - index
  DistPerCycle = 2 * pi
  return (NumOfCycles * DistPerCycle) / Duration

def CalculateNextImpactTime(CurrentImpactTime, Velocity):
  return CurrentImpactTime + (pi / Velocity) * 1000

def CalculateDynamicOpacity(CurrentTime, LastImpactTime, BaseOpacity, MaxOpacity, Duration):
  TimeSinceImpact = CurrentTime - LastImpactTime
  Perc = min(TimeSinceImpact / Duration, 1)
  OpacityDelta = MaxOpacity - BaseOpacity
  return MaxOpacity - (OpacityDelta * Perc)

def DetermineOpacity(CurrentTime, LastImpactTime, BaseOpacity, MaxOpacity, Duration):
  if not PulseEnabled:
    return BaseOpacity
      
  return CalculateDynamicOpacity(CurrentTime, LastImpactTime, BaseOpacity, MaxOpacity, Duration)

def CalculatePositionOnArc(Center, Radius, Angle):
  X = Center[0] + Radius * cos(Angle)
  Y = Center[1] + Radius * sin(Angle)
  return (X, Y)

# Was planning to add music to it
def PlayKey(index):
  pass

def Init():
  Arcs = []
  
  for index, Color in enumerate(Colors):
    Velocity = CalculateVelocity(index)
      
    LastImpactTime = 0
    NextImpactTime = CalculateNextImpactTime(StartTime, Velocity)
      
    arc = Arc(Color, Velocity, LastImpactTime, NextImpactTime)
    Arcs.append(arc)
      
  return Arcs

# Main functions
def DrawArc(X, Y, Radius, Start, End, action="stroke"):
  turtle.penup()
  turtle.goto(X, Y - Radius)
  turtle.pendown()
  turtle.setheading(0)
  turtle.circle(Radius, (End - Start) * 180 / pi)

def DrawPointOnArc(Center, ArcRadius, PointRadius, Angle):
  Position = CalculatePositionOnArc(Center, ArcRadius, Angle)
  X, Y = Position
  
  turtle.penup()
  turtle.goto(X, Y - PointRadius)
  turtle.pendown()
  turtle.setheading(0)
  turtle.circle(PointRadius)

def Draw():
  turtle.clear()
  
  CurrentTime = time.time() * 1000
  ElapsedTime = (CurrentTime - StartTime) / 1000

  Length = min(turtle.window_width(), turtle.window_height()) * 0.9
  Offset = (turtle.window_width() - Length) / 2

  Start = (Offset, turtle.window_height() / 2)
  End = (turtle.window_width() - Offset, turtle.window_height() / 2)
  Center = (0, 0)

  BaseLength = End[0] - Start[0]
  BaseMinAngle = 0
  BaseStartAngle = 0
  BaseMaxAngle = 2 * pi

  BaseInitialRadius = BaseLength * 0.05 # Affects the arcs size
  BaseCircleRadius = BaseLength * 0.006
  BaseClearance = BaseLength * 0.03
  BaseSpacing = (BaseLength - BaseInitialRadius - BaseClearance) / 2 / len(Colors)

  for index, arc in enumerate(Arcs):
    Radius = BaseInitialRadius + (BaseSpacing * index)

    # Draw arcs
    turtle.pensize(BaseLength * 0.002) # Ignore errors
    turtle.pencolor(arc.Color)

    Offset = BaseCircleRadius * (5 / 3) / Radius
    #DrawArc(Center[0], Center[1], Radius, pi + Offset, (2 * pi) / Offset) # Affects the shape of the guide arcs, division makes the arcs circles
    
    
    # Draw impact points
    turtle.fillcolor(arc.Color)
      
    #DrawPointOnArc(Center, Radius, BaseCircleRadius * 0.75, pi)
    #DrawPointOnArc(Center, Radius, BaseCircleRadius * 0.75, 2 * pi)

    # Draw moving circles
    turtle.fillcolor(arc.Color)
      
    if CurrentTime >= arc.NextImpactTime:
      if SoundEnabled:
        PlayKey(index)
        arc.LastImpactTime = arc.NextImpactTime
              
      arc.NextImpactTime = CalculateNextImpactTime(arc.NextImpactTime, arc.Velocity)

    Dist = ElapsedTime * arc.Velocity
    Angle = (pi + Dist) % BaseMaxAngle
    DrawPointOnArc(Center, Radius, BaseCircleRadius, Angle)

  turtle.update()
  turtle.ontimer(Draw, 1)

StartTime = time.time() * 1000
Duration = 900 # Time until orginial position comes back
MaxCycles = max(len(Colors), 100)
SoundEnabled = False
PulseEnabled = True

turtle.hideturtle()
turtle.setup(800, 600)
turtle.title("Polyrhythmic Spiral")
turtle.bgcolor("black")
turtle.tracer(0)

Arcs = Init()
Draw()

turtle.done()
