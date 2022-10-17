import math

class Vector2:
    fp_precision = 10**(-13)

    #Overrides

    #Constructors
    def __init__(self, x, y=None):
        """A Tuple/list/iterable can be used as inputs as well"""
        if y == None:
            y = x[1]
            x = x[0]
        self.x = x
        self.y = y
        self.magnitude = self.Magnitude()

    def PolarConstructor(r, t):
        """Constructs a vector with given magnitude and direction(angle in radians)"""
        return Vector2(r*math.cos(t), r*math.sin(t))

    def PolarConstructorDeg(r, t):
        """Constructs a vector with given magnitude and direction(angle in degrees)"""
        t = math.radians(t)
        return Vector2(r*math.cos(t), r*math.sin(t))
    
    def asTuple(self) -> tuple:
        """Returns the vector as a tuple"""
        return (self[0], self[1])


    #Shell representation
    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    #Print function
    def __str__(self):
        return str((self.x, self.y))

    #indexing
    def __getitem__(self, index):
        if index == 0 or index == 'x':
            return self.x
        elif index == 1 or index == 'y':
            return self.y
        else:
            raise IndexError("Enter a valid index (0/x or 1/y)")

    #Writing index
    def __setitem__(self, index, item):
        if index == 0 or index == 'x':
            self.x = item
        elif index == 1 or index == 'y':
            self.y = item
        else:
            raise IndexError("Enter a valid index (0/x or 1/y)")        



    # +
    def __add__(self, other) -> 'Vector2':
        return Vector2(self[0] + other[0], self[1] + other[1])
    # additive inverse
    def __neg__(self) -> 'Vector2':
        return Vector2(-self[0], -self[1])

    # -
    def __sub__(self, other) -> 'Vector2':
        return self + (-Vector2(other))

    # *
    def __mul__(self, scalar) -> 'Vector2':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return Vector2(self[0]*scalar, self[1]*scalar)

    # * but from the left
    def __rmul__(self, scalar) -> 'Vector2':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return Vector2(self[0]*scalar, self[1]*scalar)

    # /
    def __truediv__(self, scalar) -> 'Vector2':
        if type(scalar) != int and type(scalar) != float:
            raise TypeError("scalar has to be an int or a float")
        return self * (1/scalar)

    #compare if 2 floats are as close as to be considered equal
    def PrecisionEquality(a,b):
        return abs(a-b)<Vector2.fp_precision

    # ==
    def __eq__(self, o:'Vector2'):
        if o==None:
            return False
        return Vector2.PrecisionEquality(self[0], o[0]) and Vector2.PrecisionEquality(self[1], o[1])


    #Other operators
    
    def Magnitude(self):
        """Returns the magnitude of the vector"""
        return math.sqrt(self[0]**2 + self[1]**2)

    def Dot(self, b):
        """
        Returns the dot product a.b
        Usage: Dot(a,b) or a.Dot(b)
        """
        return self[0]*b[0] + self[1]*b[1]

    
    def Normalized(self):
        """Returns the unit vector in the direction of the input vector"""
        return self/self.magnitude

    def Cross(self, b:'Vector2'):
        """
        Returns the cross product axb (in this order)
        Usage: Dot(a,b) or a.Dot(b)
        """
        return self[0]*b[1] - self[1]*b[0]

    def Direction(a:'Vector2', b:'Vector2') -> 'Vector2':
        return b-a

    def Angle(self, other:'Vector2' = None):
        """returns the angle in radians between 2 vectors"""
        if other == None:
            return math.atan2(self[1], self[0])
            

        return self.Angle() - Vector2.Angle(other)


    def AngleDeg(self, other:'Vector2' = None):
        """returns the angle in degrees between 2 vectors"""
        return math.degrees(self.Angle(other))

    def Rotate(self, angle):
        """returns a vector rotated by angle in radians"""
        return Vector2.PolarConstructor(self.magnitude, self.Angle()+angle)

    def RotateDeg(self, angle):
        """returns a vector rotated by angle in degrees"""
        angle = math.radians(angle)
        return Vector2.PolarConstructor(self.magnitude, self.Angle()+angle)

    def IntClamp(self):
        """Round the vector to the nearest integer vector"""
        return Vector2(round(self[0]), round(self[1]))


    #Vector operators
    def lerp(start, end, t):
        return start + t*(end-start)

    def slerp(start, end, t : float, omega=90):
        omega = math.radians(omega)

        return ((math.sin((1-t)*omega)/math.sin(omega)) * start) + ((math.sin((t)*omega)/math.sin(omega))*end)


    #global constants
    def UP():
        return Vector2(0, 1)
    def DOWN():
        return Vector2(0, -1)
    def LEFT():
        return Vector2(-1,0)
    def RIGHT():
        return Vector2(1,0)
    def ZERO():
        return Vector2(0,0)
