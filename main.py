import blocktype as block_type
import texturemanager as texture_manager
import shader
import matrix
import pyglet.gl as gl
import math
import ctypes
import pyglet

pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False


class Window(pyglet.window.Window):
    def __init__(self, **args):
        super().__init__(**args)

        self.texture_manager = texture_manager.TextureManager(16, 16, 256)

        self.cobblestone = block_type.BlockType(
            self.texture_manager, "cobblestone", {"all": "cobblestone"})
        self.grass = block_type.BlockType(self.texture_manager, "grass", {
            "top": "grass", "bottom": "dirt", "sides": "grass_side"})
        self.dirt = block_type.BlockType(
            self.texture_manager, "dirt", {"all": "dirt"})
        self.stone = block_type.BlockType(
            self.texture_manager, "stone", {"all": "stone"})
        self.sand = block_type.BlockType(
            self.texture_manager, "sand", {"all": "sand"})
        self.planks = block_type.BlockType(
            self.texture_manager, "planks", {"all": "planks"})
        self.log = block_type.BlockType(self.texture_manager, "log", {
            "top": "log_top", "bottom": "log_top", "sides": "log_side"})

        self.texture_manager.generate_mipmaps()

        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)

        self.vertex_position_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.vertex_position_vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vertex_position_vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLfloat * len(self.grass.vertex_positions)),
            (gl.GLfloat * len(self.grass.vertex_positions)
             )(*self.grass.vertex_positions),
            gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)

        self.tex_coord_vbo = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.byref(self.tex_coord_vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.tex_coord_vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLfloat * len(self.grass.tex_coords)),
            (gl.GLfloat * len(self.grass.tex_coords))(*self.grass.tex_coords),
            gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(1)

        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLuint * len(self.grass.indices)),
            (gl.GLuint * len(self.grass.indices))(*
                                                  self.grass.indices),
            gl.GL_STATIC_DRAW)

        self.shader = shader.Shader("vert.glsl", "frag.glsl")
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")
        self.shader_sampler_location = self.shader.find_uniform(
            b"texture_array_sampler")
        self.shader.use()

        self.mv_matrix = matrix.Matrix()
        self.p_matrix = matrix.Matrix()

        self.x = 0
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)

    def update(self, dt):
        self.x += dt

    def on_draw(self):

        self.p_matrix.load_identity()
        self.p_matrix.perspective(
            90, float(self.width) / self.height, 0.1, 500)

        self.mv_matrix.load_identity()
        self.mv_matrix.translate(0, 0, -3)
        self.mv_matrix.rotate_2d(self.x, math.sin(self.x / 3 * 2) / 2)

        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY,
                         self.texture_manager.texture_array)
        gl.glUniform1i(self.shader_sampler_location, 0)

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()

        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(self.grass.indices),
            gl.GL_UNSIGNED_INT,
            None)

    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")
        gl.glViewport(0, 0, width, height)


class Game:
    def __init__(self):
        self.config = gl.Config(
            double_buffer=True, major_version=3, minor_version=3, depth_size=16)
        self.window = Window(config=self.config, width=800, height=600,
                             caption="Minecraft clone", resizable=True, vsync=False)

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = Game()
    game.run()
