import numpy as np


def radec2xyz(ra, dec):
    """
    Convert right ascension and declination to cartesian coordinates

    Parameters
    ----------
    ra : float
        Right ascension in degrees
    dec : float
        Declination in degrees

    Returns
    -------
    np.array
        Cartesian coordinates of the given right ascension and declination
    """
    ra = np.deg2rad(ra)
    dec = np.deg2rad(dec)
    cosdec = np.cos(dec)
    return np.array([np.cos(ra) * cosdec, np.sin(ra) * cosdec, np.sin(dec)])


def xyz2radec(x, y, z):
    """
    Convert cartesian coordinates to right ascension and declination

    Parameters
    ----------
    x : float
        x-coordinate
    y : float
        y-coordinate
    z : float
        z-coordinate

    Returns
    -------
    tuple
        Tuple containing the right ascension and declination in degrees
    """
    ra = np.degrees(np.arctan2(y, x))
    dec = np.degrees(np.arcsin(z))
    ra = np.where(ra < 0., ra + 360., ra)

    return ra, dec


class Triangle:
    def __init__(self, e0= np.zeros(3), e1= np.zeros(3), e2= np.zeros(3)):
        if len(e0) != 3 or len(e1) != 3 or len(e2) != 3:
            raise ValueError("e0, e1, e2 must be 3D vectors")
        self.e0 = e0
        self.e1 = e1
        self.e2 = e2
        self._north = np.array([0, 0, 1])

    # set what get printed when you print the object
    def __str__(self):
        return f"e0: {self.e0}, e1: {self.e1}, e2: {self.e2}"
    
    @property
    def x(self):
        return np.array([self.e0[0], self.e1[0], self.e2[0]])
    
    @property
    def y(self):
        return np.array([self.e0[1], self.e1[1], self.e2[1]])
    
    @property
    def z(self):
        return np.array([self.e0[2], self.e1[2], self.e2[2]])

    @property
    def center(self):
        center = self.e0 + self.e1 + self.e2
        return center / np.linalg.norm(center)
    
    @property
    def axis0(self):
        axis0 = np.cross(self._north, self.center)
        return axis0 / np.linalg.norm(axis0)
    
    @property
    def axis1(self):
        return np.cross(self.center, self.axis0)
    
    @property
    def scale(self):
        scale = 0.
        for c in [self.e0, self.e1, self.e2]:
            mu0 = np.dot(c - self.center, self.axis0)
            mu1 = np.dot(c - self.center, self.axis1)
            f = 1.0 / np.sqrt(1.0 - mu0 * mu0 - mu1 * mu1)
            h = np.abs(mu0) * f
            if scale < h:
                scale = h
            h = np.abs(mu1) * f
            if scale < h:
                scale = h
        return scale

    def radec_to_x0x1(self, ra, dec):
        v = radec2xyz(ra, dec)
        mu0 = (v - self.center) @ self.axis0
        mu1 = (v - self.center) @ self.axis1
        d = 1.0 - mu0*mu0 - mu1*mu1
        sd = np.sqrt(d)
        x0 = mu0 / (sd * self.scale)
        x1 = mu1 / (sd * self.scale)
        # the factor of 59.5 is found empirically, I dunno where it comes from
        return x0 / (0.0001 / 3600. / 59.5), x1 / (0.0001 / 3600. / 59.5)

    # write a function to reverse x0, x1 to ra, dec
    def x0x1_to_radec(self, x0, x1):
        x0 = np.array(x0).astype(np.float64)
        x1 = np.array(x1).astype(np.float64)
        # the factor of 59.5 is found empirically, I dunno where it comes from
        x0 *= (0.0001 / 3600. / 59.5) * self.scale
        x1 *= (0.0001 / 3600. / 59.5) * self.scale
        pos = self.axis0 * x0 + self.center + self.axis1 * x1
        pos /= np.linalg.norm(pos)
        return xyz2radec(*pos)


class HalfSpace:
    def __init__(self, n, d):
        self.n = n  # Normal vector
        self.d = d  # Distance parameter

    def inside(self, x):
        # Check if point x is inside the half-space
        return x * self.n >= self.d


class GeodesicGrid:
    def __init__(self, level: int, max_level: int = 8):
        """
        GeodesicGrid constructor 

        Parameters
        ----------
        level : int
            The level of the grid
        max_level : int
            The maximum level allowed of the GeodesicGrid
        """
        self.max_level = max_level
        self.level = level
        if self.level > self.max_level:
            raise ValueError("level must be less than or equal to max_level")
        elif self.level < 0:
            raise ValueError("level must be greater than or equal to 0")

        self.icosahedron_G = 0.5 * (1.0 + np.sqrt(5.0))
        self.icosahedron_b = 1.0 / np.sqrt(
            1.0 + self.icosahedron_G * self.icosahedron_G
        )
        self.icosahedron_a = self.icosahedron_b * self.icosahedron_G

        self.icosahedron_corners = np.array(
            [
                [self.icosahedron_a, -self.icosahedron_b, 0.0],
                [self.icosahedron_a, self.icosahedron_b, 0.0],
                [-self.icosahedron_a, self.icosahedron_b, 0.0],
                [-self.icosahedron_a, -self.icosahedron_b, 0.0],
                [0.0, self.icosahedron_a, -self.icosahedron_b],
                [0.0, self.icosahedron_a, self.icosahedron_b],
                [0.0, -self.icosahedron_a, self.icosahedron_b],
                [0.0, -self.icosahedron_a, -self.icosahedron_b],
                [-self.icosahedron_b, 0.0, self.icosahedron_a],
                [self.icosahedron_b, 0.0, self.icosahedron_a],
                [self.icosahedron_b, 0.0, -self.icosahedron_a],
                [-self.icosahedron_b, 0.0, -self.icosahedron_a],
            ]
        )

        self.icosahedron_triangles = np.array(
            [
                [1, 0, 10],  #  1
                [0, 1, 9],  #  0
                [0, 9, 6],  # 12
                [9, 8, 6],  #  9
                [0, 7, 10],  # 16
                [6, 7, 0],  #  6
                [7, 6, 3],  #  7
                [6, 8, 3],  # 14
                [11, 10, 7],  # 11
                [7, 3, 11],  # 18
                [3, 2, 11],  #  3
                [2, 3, 8],  #  2
                [10, 11, 4],  # 10
                [2, 4, 11],  # 19
                [5, 4, 2],  #  5
                [2, 8, 5],  # 15
                [4, 1, 10],  # 17
                [4, 5, 1],  # 4
                [5, 9, 1],  # 13
                [8, 9, 5],  #  8
            ]
        )

        self.triangles = []  # should be nested list of Triangle objects, first level is the level
        self.vertices = [self.icosahedron_corners]  # should be nested list of vertices, first level is the level
        self.faces = [self.icosahedron_triangles]  # should be nested list of faces, first level is the level
        self._init_triangles()

    @property
    def num_zones(self):
        """
        Get the number of zones in the grid at the current level
        """
        return self.level_nzones(self.level)
    
    def level_nzones(self, level):
        """
        Calculate the number of zones at a given level
        """
        return 20 * (4**level)
    
    def _init_triangles(self):
        # initialize level 0 triangles
        temp_triangles = []
        for i in range(20):
            temp_triangles.append(Triangle(*self.icosahedron_corners[self.icosahedron_triangles[i]]))
        self.triangles.append(temp_triangles)

        for level in range(1, self.level+1):
            temp_triangles = []
            temp_vertices = []
            temp_faces = []
            counter = 0
            for i in range(self.level_nzones(level) // 4):
                t = self.triangles[level-1][i]
                c0, c1, c2 = t.e0, t.e1, t.e2
                e0 = c1 + c2
                e0 = e0 / np.linalg.norm(e0)
                e1 = c2 + c0
                e1 = e1 / np.linalg.norm(e1)
                e2 = c0 + c1
                e2 = e2 / np.linalg.norm(e2)
                temp_triangles.append(Triangle(c0, e2, e1))
                temp_triangles.append(Triangle(e2, c1, e0))
                temp_triangles.append(Triangle(e1, e0, c2))
                temp_triangles.append(Triangle(e0, e1, e2))
                temp_vertices.extend([c0, c1, c2, e0, e1, e2])
                temp_faces.append(np.array([[0, 5, 4], [5, 1, 3], [4, 3, 2], [3, 4, 5]]) + counter)
                counter += 6
            self.triangles.append(temp_triangles)
            self.vertices.append(temp_vertices)
            self.faces.append(temp_faces)

    def search_zone(self, v):  # TODO: vectorize this function
        """
        Search for the zone that contains the vector v

        Parameters
        ----------
        v : np.array
            The 3D vector to search for in geodesic grid (Not RA/DEC)
            If you want to search for a point in RA/DEC, use radec2xyz to convert it to a vector
        """
        v = np.atleast_2d(v)  # make sure at least 2D array

        result = np.ones(len(v), dtype=int) * -1  # initialize result with -1
        # always need to search level 0 anyway
        for i in range(self.level_nzones(0)):
            t = self.triangles[0][i]
            c0, c1, c2 = t.e0, t.e1, t.e2
            mask = (
                (np.dot(np.cross(c0, c1), v.T) >= 0) &
                (np.dot(np.cross(c1, c2), v.T) >= 0) &
                (np.dot(np.cross(c2, c0), v.T) >= 0)
            )
            result[mask] = i
        
        v = v.T
        # vectorized version
        if self.level > 0:
            for level in range(1, 1 + self.level):
                result *= 4
                for j in range(self.level_nzones(level) // 4):
                    calc_idx = np.where(result // 4  == j)[0]
                    temp_v = v[:, calc_idx]
                    if len(calc_idx) == 0:
                        continue
                    for k in range(4):
                        t = self.triangles[level][j * 4 + k]
                        c0, c1, c2 = t.e0, t.e1, t.e2
                        mask = (
                            (np.dot(np.cross(c0, c1), temp_v) >= 0) &
                            (np.dot(np.cross(c1, c2), temp_v) >= 0) &
                            (np.dot(np.cross(c2, c0), temp_v) >= 0)
                        )
                        result[calc_idx[mask]] += k
        return result
