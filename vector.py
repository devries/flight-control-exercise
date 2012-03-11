"""3-D vector library. This library is designed to make working with
vectors as easy as working with regular numbers. The main class is the Threevec
class which stores the vectors in recangular coordinates and allows
standard operations. There are generator functions to return vectors defined
in rectangular coordinates, cylindrical coordinates, and spherical coordinates.
This is an extension of a vector library in C which I started developing in
1993 and was later ported to Java and now Python.

Copyright 2012 Christopher De Vries"""
import math
import numbers

class Threevec(numbers.Number):
    def __init__(self,x=0,y=0,z=0):
        self.x=x
        self.y=y
        self.z=z
        
    def __str__(self):
        return "(%g,%g,%g)"%(self.x,self.y,self.z)

    def __repr__(self):
        return "Threevec(%g,%g,%g)"%(self.x,self.y,self.z)
    
    def __add__(self,other):
        """Vector addition."""
        result = Threevec()
        
        if isinstance(other,Threevec):
            result.x=self.x+other.x
            result.y=self.y+other.y
            result.z=self.z+other.z
            
            return result
        else:
            raise TypeError("A Threevec can only be added to another Threevec")
        
    def __mul__(self,other):
        """Dot product between vectors or vector, scalar multiplication."""
        if isinstance(other,Threevec):
            result = self.x*other.x+self.y*other.y+self.z*other.z
            return result
        elif isinstance(other,numbers.Real):
            result = Threevec(other*self.x,other*self.y,other*self.z)
            return result
        else:
            raise TypeError("A Threevec can only be multiplied by a Threevec or real number")
        
    def __rmul__(self,other):
        """Multiplication of a scalar by a vector."""
        return self*other
    
    def __mod__(self,other):
        """The % operator is used to calculate a cross-product."""
        result = Threevec()
        
        if isinstance(other,Threevec):
            result.x=self.y*other.z-self.z*other.y
            result.y=self.z*other.x-self.x*other.z
            result.z=self.x*other.y-self.y*other.x
            
            return result
        else:
            raise TypeError("A cross product can only be calculated between two Threevecs")

    def __div__(self,other):
        """Division of a vector by a scalar."""
        if isinstance(other,numbers.Real):
            result = self*(1.0/other)
            return result
        else:
            raise TypeError("A Threevec can only be divided by a real number.")

    def __neg__(self):
        """Inversion of a vector is done by the - sign."""
        result = Threevec(-self.x,-self.y,-self.z)
        return result
    
    def __sub__(self,other):
        """Subtraction of a vector from a vector. Equivalent to addition of
        a vector and its inverse."""
        return self+(-other)

    def __abs__(self):
        """The magnitude of a vector is obtained using the abs() operator."""
        return math.sqrt(self.x**2+self.y**2+self.z**2)

    def __eq__(self,other):
        """Vectors are defined as equal if all their elements are equal."""
        return self.x==other.x and self.y==other.y and self.z==other.z

    def __ne__(self,other):
        """Vectors are defined as unequal if any of the elements are not equal."""
        return self.x!=other.x or self.y!=other.y or self.z!=other.z

    def __len__(self):
        """We can treat a Threevec as a sequence of length 3."""
        length = 3
        return length

    def __contains__(self,item):
        """The expression "n in vector" will return True if n is one of the
        components of the vector."""
        return self.x==item or self.y==item or self.z==item

    def __getitem__(self,key):
        """Vectors also act as three element typles. Element 0 is the x
        component, Element 1 is the y component, and Element 2 is the z
        component."""
        if isinstance(key,int):
            if key==0:
                return self.x
            elif key==1:
                return self.y
            elif key==2:
                return self.z
            else:
                raise IndexError("Only elements 0, 1, and 2 are defined in a Threevec")
        else:
            raise TypeError("The keys of a Threevec must be integers")

    def __iter__(self):
        """As an iterator, the vector returns the elements x, y, and z in that
        order."""
        yield self.x
        yield self.y
        yield self.z
    
    @property
    def rho(self):
        """The cylindrical radius component. Equal to the square root of the
        x component squared and the y component squared."""
        return math.sqrt(self.x**2+self.y**2)

    @property
    def phi(self):
        """The spherical phi component, which is the angle between the
        projection of the vector on the x-y plane and the x-axis. 
        This ranges from -pi to pi."""
        return math.atan2(self.y,self.x)

    @property
    def theta(self):
        """The spherical theta component, which is the angle between the vector
        and the z axis."""
        return math.acos(self.z/abs(self))

    def unit(self):
        """Return a new vector in the same direction as this vector, but with unit length."""
        result = self/abs(self)

        return result

    def rotate(self,axis,angle):
        """Return a vector which has been rotated around the axis vector by
        an angle in the right-handed sense."""
        ea = axis.unit()
        eb = (axis%self).unit()
        ec = eb%ea

        ea_mag = self*ea
        eb_mag = math.sin(angle)*self*ec
        ec_mag = math.cos(angle)*self*ec

        result = ea_mag*ea+eb_mag*eb+ec_mag*ec
        return result

        
i = Threevec(1,0,0)
j = Threevec(0,1,0)
k = Threevec(0,0,1)

def recvec(x,y,z):
    """A function which returns a vector defined by x, y, and z in
    rectangular coordinates."""
    return Threevec(x,y,z)

def cylvec(rho,phi,z):
    """A function which returns a vector defined by rho, phi, z in
    cylindrical coordinates."""
    x = rho*math.cos(phi)
    y = rho*math.sin(phi)
    return Threevec(x,y,z)

def sphvec(r,theta,phi):
    """A function which returns a vector defined by r, theta, phi in
    spherical coordinates."""
    x = r*math.sin(theta)*math.cos(phi)
    y = r*math.sin(theta)*math.sin(phi)
    z = r*math.cos(theta)
    return Threevec(x,y,z)

