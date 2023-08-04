import copy
import ctypes
import math


def copy_matrix(matrix):
    return copy.deepcopy(matrix)  # using 2d arrays so deepcopy is needed


open_matrix = [[0.0 for x in range(4)] for x in range(4)]
iden_matrix = copy_matrix(open_matrix)

iden_matrix[0][0] = 1.0
iden_matrix[1][1] = 1.0
iden_matrix[2][2] = 1.0
iden_matrix[3][3] = 1.0


def multiply_matrices(x_matrix, y_matrix):
    result_matrix = copy_matrix(open_matrix)

    for i in range(4):
        for j in range(4):
            result_matrix[i][j] = \
                (x_matrix[0][j] * y_matrix[i][0]) + \
                (x_matrix[1][j] * y_matrix[i][1]) + \
                (x_matrix[2][j] * y_matrix[i][2]) + \
                (x_matrix[3][j] * y_matrix[i][3])

    return result_matrix


class Matrix:
    def __init__(self, base=None):
        if type(base) == Matrix:
            self.data = copy_matrix(base.data)
        elif type(base) == list:
            self.data = copy_matrix(base)
        else:
            self.data = copy_matrix(open_matrix)

    def load_identity(self):
        self.data = copy_matrix(iden_matrix)

    def __mul__(self, matrix):
        return Matrix(multiply_matrices(self.data, matrix.data))

    def __imul__(self, matrix):
        self.data = multiply_matrices(self.data, matrix.data)

    def scale(self, x, y, z):
        for i in range(4):
            self.data[0][i] *= x
        for i in range(4):
            self.data[1][i] *= y
        for i in range(4):
            self.data[2][i] *= z

    def translate(self, x, y, z):
        for i in range(4):
            self.data[3][i] = self.data[3][i] + \
                (self.data[0][i] * x + self.data[1]
                 [i] * y + self.data[2][i] * z)

    def rotate(self, angle, x, y, z):
        magnitude = math.sqrt(x * x + y * y + z * z)

        x /= -magnitude
        y /= -magnitude
        z /= -magnitude

        sin_angle = math.sin(angle)
        cos_angle = math.cos(angle)
        cos_complement = 1.0 - cos_angle

        xx = x * x
        yy = y * y
        zz = z * z

        xy = x * y
        yz = y * z
        zx = z * x

        xs = x * sin_angle
        ys = y * sin_angle
        zs = z * sin_angle

        rotation_matrix = copy_matrix(open_matrix)

        rotation_matrix[0][0] = (cos_complement * xx) + cos_angle
        rotation_matrix[0][1] = (cos_complement * xy) - zs
        rotation_matrix[0][2] = (cos_complement * zx) + ys

        rotation_matrix[1][0] = (cos_complement * xy) + zs
        rotation_matrix[1][1] = (cos_complement * yy) + cos_angle
        rotation_matrix[1][2] = (cos_complement * yz) - xs

        rotation_matrix[2][0] = (cos_complement * zx) - ys
        rotation_matrix[2][1] = (cos_complement * yz) + xs
        rotation_matrix[2][2] = (cos_complement * zz) + cos_angle

        rotation_matrix[3][3] = 1.0
        self.data = multiply_matrices(self.data, rotation_matrix)

    def rotate_2d(self, x, y):
        self.rotate(x, 0, 1.0, 0)
        self.rotate(-y, math.cos(x), 0, math.sin(x))

    def frustum(self, left, right, bottom, top, near, far):
        dx = right - left
        dy = top - bottom
        dz = far - near

        frustum_matrix = copy_matrix(open_matrix)

        frustum_matrix[0][0] = 2 * near / dx
        frustum_matrix[1][1] = 2 * near / dy

        frustum_matrix[2][0] = (right + left) / dx
        frustum_matrix[2][1] = (top + bottom) / dy
        frustum_matrix[2][2] = -(near + far) / dz

        frustum_matrix[2][3] = -1.0
        frustum_matrix[3][2] = -2 * near * far / dz

        self.data = multiply_matrices(self.data, frustum_matrix)

    def perspective(self, fovy, aspect, near, far):
        frustum_y = math.tan(math.radians(fovy) / 2)
        frustum_x = frustum_y * aspect

        self.frustum(-frustum_x * near, frustum_x * near, -
                     frustum_y * near, frustum_y * near, near, far)

    def orthographic(self, left, right, bottom, top, near, far):
        dx = right - left
        dy = top - bottom
        dz = far - near

        orthographic_matrix = copy_matrix(iden_matrix)

        orthographic_matrix[0][0] = 2.0 / dx
        orthographic_matrix[3][0] = -(right + left) / dx

        orthographic_matrix[1][1] = 2.0 / dy
        orthographic_matrix[3][1] = -(top + bottom) / dy

        orthographic_matrix[2][2] = 2.0 / dx
        orthographic_matrix[3][2] = -(near + far) / dz

        self.data = multiply_matrices(self.data, orthographic_matrix)


# help me i have no idea what im doing lol
