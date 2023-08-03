import ctypes
import pyglet.gl as gl
import pyglet
import shader

pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

vertex_positions = [  # 3d coordinates for each vertex
    -0.5,  0.5, 1.0,
    -0.5, -0.5, 1.0,
    0.5, -0.5, 1.0,
    0.5,  0.5, 1.0,
]

indices = [
    0, 1, 2,
    0, 2, 3,
]


class Window(pyglet.window.Window):
    def __init__(self, **args):
        super(Window, self).__init__(**args)

        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        self.vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        gl.glBufferData(gl.GL_ARRAY_BUFFER,
                        ctypes.sizeof(gl.GLfloat * len(vertex_positions)),
                        (gl.GLfloat * len(vertex_positions))(*vertex_positions),
                        gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)

        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER,
                        ctypes.sizeof(gl.GLuint * len(indices)),
                        (gl.GLuint * len(indices))(*indices),
                        gl.GL_STATIC_DRAW)

        self.shader = shader.Shader("vert.glsl", "frag.glsl")
        self.shader.use()

    def on_draw(self):
        gl.glClearColor(1.0, 0.5, 1.0, 1.0)
        self.clear()

        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(indices),
            gl.GL_UNSIGNED_INT,
            None
        )

    def on_resize(self, width, height):
        print(f"resize {width} * {height}")
        gl.glViewport(0, 0, width, height)


class Game:
    def __init__(self):
        self.config = gl.Config(major_version=3)
        self.window = Window(config=self.config, width=800, height=600,
                             caption="Minecraft: Python Edition", resizable=True, vsync=False)

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = Game()
    game.run()
