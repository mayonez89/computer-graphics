from OpenGL.GL import *

import glm
from utils.glut_window import GlutWindow
from utils.mvp_controller import MVPController
from OpenGL.GL import shaders
import random
import time

# Define a tetrahedron using triangles
vertex_buffer_data = [
	-1, +0, -1, +1, +0, -1, -1, +0, +1,  # Base 0
	+1, +0, -1, +1, +0, +1, -1, +0, +1,  # Base 1
	-1, +0, -1, +0, +1, +0, +1, +0, -1,  # Side 0
	+1, +0, -1, +0, +1, +0, +1, +0, +1,  # Side 1
	+1, +0, +1, +0, +1, +0, -1, +0, +1,  # Side 2
	-1, +0, +1, +0, +1, +0, -1, +0, -1,  # Side 3
]
# Set random colors for each of the vertices
color_buffer_data = [random.random() for _ in range(len(vertex_buffer_data))]

start_time = time.time()


def read_file(file_path: str) -> str:
	"""Reads a text file given a path and returns it as a string."""
	with open(file_path, mode="r") as f:
		contents = f.readlines()
	return contents


class GLContext:
	"""Used for storing context data in the main window."""
	pass


class Win(GlutWindow):
	"""The main application. Inherits from glut_window.py."""
	def __init__(self, width: int = 800, height: int = 480):
		super().__init__(width, height)
		self.context = GLContext()

	def init_context(self):
		# Read shader files and compile them
		vertex_shader_string = read_file("shaders/vertex_shader.glsl")
		fragment_shader_string = read_file("shaders/fragment_shader.glsl")
		vertex_shader = shaders.compileShader(vertex_shader_string, GL_VERTEX_SHADER)
		fragment_shader = shaders.compileShader(
			fragment_shader_string, GL_FRAGMENT_SHADER
		)
		self.shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

		# Get location of the MVP matrix
		self.context.mvp_location = glGetUniformLocation(self.shader_program, "mvp")
		# Generate buffers for vertices and color data and buffer the data
		self.context.vertex_buffer = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.vertex_buffer)
		glBufferData(
			GL_ARRAY_BUFFER,
			len(vertex_buffer_data) * 4,
			(GLfloat * len(vertex_buffer_data))(*vertex_buffer_data),
			GL_STATIC_DRAW,
		)

		self.context.color_buffer = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.color_buffer)
		glBufferData(
			GL_ARRAY_BUFFER,
			len(color_buffer_data) * 4,
			(GLfloat * len(color_buffer_data))(*color_buffer_data),
			GL_STATIC_DRAW,
		)

	def calc_mvp(self):
		self.calc_model()
		self.context.mvp = self.controller.calc_mvp(self.model_matrix)

	def resize(self, width, height):
		glViewport(0, 0, width, height)
		self.calc_mvp()

	def calc_model(self):
		self.model_matrix = glm.mat4(1)
		# 2. Add code here to make the object rotate



	def draw(self):
		"""
		The main drawing function. Is called whenever an update occurs.
		"""
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.calc_mvp()
		glUseProgram(self.shader_program)
		glUniformMatrix4fv(
			self.context.mvp_location, 1, GL_FALSE, glm.value_ptr(self.context.mvp)
		)

		glEnableVertexAttribArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.vertex_buffer)
		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

		glEnableVertexAttribArray(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.context.color_buffer)
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

		glDrawArrays(GL_TRIANGLES, 0, len(vertex_buffer_data))

		glDisableVertexAttribArray(0)
		glDisableVertexAttribArray(1)
		glUseProgram(0)


if __name__ == "__main__":
	win = Win()
	win.controller = MVPController(win.update_if, width=win.width, height=win.height)
	win.init_opengl()
	win.init_context()
	win.run()
