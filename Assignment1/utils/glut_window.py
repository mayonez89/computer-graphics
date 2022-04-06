import OpenGL.GLUT as oglut
import sys
import OpenGL.GL as gl
from abc import ABC, abstractmethod


class GlutWindow(ABC):
    """
    Defines the window using glut and is responsible for
    initialization and drawing.
    """
    def __init__(self, width: int, height: int, *args, **kwargs):
        self.width = width
        self.height = height
        oglut.glutInit(sys.argv)
        oglut.glutInitWindowSize(self.width, self.height)
        self.window = oglut.glutCreateWindow(b"Window")
        oglut.glutDisplayFunc(self.display)
        oglut.glutIdleFunc(self.idle)
        oglut.glutReshapeFunc(self.resize)
        oglut.glutKeyboardFunc(self.on_keyboard)
        oglut.glutSpecialFunc(self.on_special_key)
        oglut.glutMouseFunc(self.on_mouse)
        oglut.glutMotionFunc(self.on_mousemove)
        self.update_if = oglut.glutPostRedisplay
        self.controller = None

    def init_opengl(self):
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

    @abstractmethod
    def draw(self):
        """
        The main drawing function. Is called whenever an update occurs.
        Needs to be implemented in the main window class.
        """
        pass

    def display(self):
        self.draw()
        oglut.glutSwapBuffers()

    def idle(self):
        self.update_if()

    @abstractmethod
    def resize(self, width, height):
        pass

    def on_keyboard(self, key, x, y):
        self.controller.on_keyboard(key, x, y)

    def on_special_key(self, key, x, y):
        self.controller.on_special_key(key, x, y)

    def on_mouse(self, *args, **kwargs):
        self.controller.on_mouse(*args, **kwargs)

    def on_mousemove(self, *args, **kwargs):
        self.controller.on_mousemove(*args, **kwargs)

    def run(self):
        oglut.glutMainLoop()


if __name__ == "__main__":
    win = GlutWindow()
    win.run()
