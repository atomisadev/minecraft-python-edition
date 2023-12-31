
import world
import texturemanager as texture_manager
import blocktype as block_type
import camera
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

        self.world = world.World()

        self.shader = shader.Shader("vert.glsl", "frag.glsl")
        self.shader_sampler_location = self.shader.find_uniform(
            b"texture_array_sampler")
        self.shader.use()

        pyglet.clock.schedule_interval(self.update, 1.0 / 10000)
        self.mouse_captured = False

        self.camera = camera.Camera(self.shader, self.width, self.height)

    def update(self, dt):
        print(f"FPS: {1.0 / dt}")

        if not self.mouse_captured:
            self.camera.input = [0, 0, 0]

        self.camera.update_camera(dt)

    def on_draw(self):
        self.camera.update_matrices()

        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D_ARRAY,
                         self.world.texture_manager.texture_array)
        gl.glUniform1i(self.shader_sampler_location, 0)

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        self.clear()
        self.world.draw()

        gl.glFinish()

    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")
        gl.glViewport(0, 0, width, height)

        self.camera.w = width
        self.camera.h = height

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_captured = not self.mouse_captured
        self.set_exclusive_mouse(self.mouse_captured)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_captured:
            sensitivity = 0.004

            self.camera.rotation[0] -= dx * sensitivity
            self.camera.rotation[1] += dy * sensitivity

            self.camera.rotation[1] = max(-math.tau / 4,
                                          min(math.tau / 4, self.camera.rotation[1]))

    def on_key_press(self, key, modifiers):
        if not self.mouse_captured:
            return

        if key == pyglet.window.key.D:
            self.camera.input[0] += 1
        elif key == pyglet.window.key.A:
            self.camera.input[0] -= 1
        elif key == pyglet.window.key.W:
            self.camera.input[2] += 1
        elif key == pyglet.window.key.S:
            self.camera.input[2] -= 1

        elif key == pyglet.window.key.SPACE:
            self.camera.input[1] += 1
        elif key == pyglet.window.key.LSHIFT:
            self.camera.input[1] -= 1

    def on_key_release(self, key, modifiers):
        if not self.mouse_captured:
            return

        if key == pyglet.window.key.D:
            self.camera.input[0] -= 1
        elif key == pyglet.window.key.A:
            self.camera.input[0] += 1
        elif key == pyglet.window.key.W:
            self.camera.input[2] -= 1
        elif key == pyglet.window.key.S:
            self.camera.input[2] += 1

        elif key == pyglet.window.key.SPACE:
            self.camera.input[1] -= 1
        elif key == pyglet.window.key.LSHIFT:
            self.camera.input[1] += 1


class Game:
    def __init__(self):
        self.config = gl.Config(
            double_buffer=True, major_version=3, minor_version=3, depth_size=16)
        self.window = Window(config=self.config, width=800, height=600,
                             caption="Minecraft: Python Edition (alpha)", resizable=True, vsync=False)

    def run(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = Game()
    game.run()
