
import copy
import ctypes
import math


def copy_matrix(matrix):
    return copy.deepcopy(matrix)  # 2d arrays, so need to deepcopy


clean_matrix = [[0.0 for x in range(4)] for x in range(4)]
open_matrix = copy_matrix(clean_matrix)

open_matrix[0][0] = 1.0
open_matrix[1][1] = 1.0
open_matrix[2][2] = 1.0
open_matrix[3][3] = 1.0


def multiply_matrices(x_matrix, y_matrix):
    result_matrix = copy_matrix(clean_matrix)

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
            self.data = copy_matrix(clean_matrix)

    def load_identity(self):
        self.data = copy_matrix(open_matrix)

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
        one_minus_cos = 1.0 - cos_angle

        xx = x * x
        yy = y * y
        zz = z * z

        xy = x * y
        yz = y * z
        zx = z * x

        xs = x * sin_angle
        ys = y * sin_angle
        zs = z * sin_angle

        rotation_matrix = copy_matrix(clean_matrix)

        rotation_matrix[0][0] = (one_minus_cos * xx) + cos_angle
        rotation_matrix[0][1] = (one_minus_cos * xy) - zs
        rotation_matrix[0][2] = (one_minus_cos * zx) + ys

        rotation_matrix[1][0] = (one_minus_cos * xy) + zs
        rotation_matrix[1][1] = (one_minus_cos * yy) + cos_angle
        rotation_matrix[1][2] = (one_minus_cos * yz) - xs

        rotation_matrix[2][0] = (one_minus_cos * zx) - ys
        rotation_matrix[2][1] = (one_minus_cos * yz) + xs
        rotation_matrix[2][2] = (one_minus_cos * zz) + cos_angle

        rotation_matrix[3][3] = 1.0
        self.data = multiply_matrices(self.data, rotation_matrix)

    def rotate_2d(self, x, y):
        self.rotate(x, 0, 1.0, 0)
        self.rotate(-y, math.cos(x), 0, math.sin(x))

    def frustum(self, left, right, bottom, top, near, far):
        dx = right - left
        dy = top - bottom
        dz = far - near

        frustum_matrix = copy_matrix(clean_matrix)

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

        ortho_matrix = copy_matrix(open_matrix)

        ortho_matrix[0][0] = 2.0 / dx
        ortho_matrix[3][0] = -(right + left) / dx

        ortho_matrix[1][1] = 2.0 / dy
        ortho_matrix[3][1] = -(top + bottom) / dy

        ortho_matrix[2][2] = 2.0 / dx
        ortho_matrix[3][2] = -(near + far) / dz

        self.data = multiply_matrices(self.data, ortho_matrix)
