import math
import matrix


class Camera:
    def __init__(self, shader, width, height):
        self.width = width
        self.height = height

        self.mv_matrix = matrix.Matrix()
        self.p_matrix = matrix.Matrix()

        self.shader = shader
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")

        self.input = [0, 0, 0]

        self.position = [0, 0, -3]
        self.rotation = [math.tau / 4, 0]

    def update_camera(self, dt):
        speed = 7
        multiplier = speed * dt

        self.position[1] += self.input[1] * multiplier

        if self.input[0] or self.input[2]:
            angle = self.rotation[0] + \
                math.atan2(self.input[2], self.input[0]) - math.tau / 4

            self.position[0] += math.cos(angle) * multiplier
            self.position[2] += math.sin(angle) * multiplier

    def update_matrices(self):

        self.p_matrix.load_identity()
        self.p_matrix.perspective(
            90, float(self.width) / self.height, 0.1, 500)

        self.mv_matrix.load_identity()
        self.mv_matrix.rotate_2d(-(self.rotation[0] -
                                 math.tau / 4), self.rotation[1])
        self.mv_matrix.translate(-self.position[0], -
                                 self.position[1], self.position[2])

        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)
