from OpenGL.GL import *

import glm
from utils.glut_window import GlutWindow
from utils.mvp_controller import MVPController
from OpenGL.GL import shaders
from utils.texture_loader import TextureLoader
import random
import math
import time
from dataclasses import dataclass
from typing import List
import ctypes


@dataclass
class Vertex:
    position: glm.vec3
    uv: glm.vec2
    normal: glm.vec3
    sizeof: int = 2 * 3 * 4 + 2 * 4  # 3 vectors, 3 floats, 4 size of float

    def tolist(self) -> List[float]:
        return list(self.position) + list(self.uv) + list(self.normal)

    @staticmethod
    def todata(l: List["Vertex"]) -> List[float]:
        return [number for vertex in l for number in vertex.tolist()]

# Define 12 vertices of a icosahedron 
icosahedron = [
    Vertex(glm.normalize(glm.vec3(-0.26286500, 0.0000000, +0.42532500)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(-0.26286500, 0.0000000, +0.42532500))),
    Vertex(glm.normalize(glm.vec3(+0.26286500, 0.0000000, +0.42532500)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(+0.26286500, 0.0000000, +0.42532500))),
    Vertex(glm.normalize(glm.vec3(-0.26286500, 0.0000000, -0.42532500)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(-0.26286500, 0.0000000, -0.42532500))),
    Vertex(glm.normalize(glm.vec3(+0.26286500, 0.0000000, -0.42532500)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(+0.26286500, 0.0000000, -0.42532500))),

    Vertex(glm.normalize(glm.vec3(0.0000000, +0.42532500, +0.26286500)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(0.0000000, +0.42532500, +0.26286500))),
    Vertex(glm.normalize(glm.vec3(0.0000000, +0.42532500, -0.26286500)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(0.0000000, +0.42532500, -0.26286500))),
    Vertex(glm.normalize(glm.vec3(0.0000000, -0.42532500, +0.26286500)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(0.0000000, -0.42532500, +0.26286500))),
    Vertex(glm.normalize(glm.vec3(0.0000000, -0.42532500, -0.26286500)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(0.0000000, -0.42532500, -0.26286500))),

    Vertex(glm.normalize(glm.vec3(+0.42532500, +0.26286500, 0.0000000)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(+0.42532500, +0.26286500, 0.0000000))),
    Vertex(glm.normalize(glm.vec3(-0.42532500, +0.26286500, 0.0000000)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(-0.42532500, +0.26286500, 0.0000000))),
    Vertex(glm.normalize(glm.vec3(+0.42532500, -0.26286500, 0.0000000)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(+0.42532500, -0.26286500, 0.0000000))),
    Vertex(glm.normalize(glm.vec3(-0.42532500, -0.26286500, 0.0000000)), glm.vec2(1.0, 0.0),
           glm.normalize(glm.vec3(-0.42532500, -0.26286500, 0.0000000))),
]

ico_inds = [0, 6, 1, 0, 11, 6, 1, 4, 0, 1, 8, 4, 1, 10, 8, 2, 5, 3, 2, 9, 5, 2, 11, 9, 3, 7, 2, 3, 10, 7, 4, 8, 5, 4, 9, 0, 5, 8, 3, 5, 9, 4, 6, 10, 1, 6, 11, 7, 7, 10, 6, 7, 10, 6, 7, 11, 2, 8, 10, 3, 9, 11, 0
]

# Generate a sphere by subdivide each faces of a icosahedron
def create_sphere(
        sphere: List[Vertex], sphere_indices: List[int], tesselation_num: int
):
    for i in range(tesselation_num):
        triangles_num = len(sphere_indices) // 3
        for t in range(triangles_num):
            tpos = 3 * t
            v0ind = sphere_indices[tpos]
            v1ind = sphere_indices[tpos + 1]
            v2ind = sphere_indices[tpos + 2]
            v0 = sphere[v0ind]
            v1 = sphere[v1ind]
            v2 = sphere[v2ind]

            # New vertices
            v3 = Vertex(
                glm.normalize(v0.position + v1.position),
                0.5 * (v0.uv + v1.uv),
                glm.normalize(v0.position + v1.position)
            )
            v4 = Vertex(
                glm.normalize(v1.position + v2.position),
                0.5 * (v1.uv + v2.uv),
                glm.normalize(v1.position + v2.position)
            )
            v5 = Vertex(
                glm.normalize(v2.position + v0.position),
                0.5 * (v2.uv + v0.uv),
                glm.normalize(v2.position + v0.position)
            )
            v3ind = len(sphere)
            sphere.append(v3)
            v4ind = len(sphere)
            sphere.append(v4)
            v5ind = len(sphere)
            sphere.append(v5)

            sphere_indices[tpos + 1] = v3ind
            sphere_indices[tpos + 2] = v5ind

            sphere_indices.extend([v3ind, v1ind, v4ind])
            sphere_indices.extend([v3ind, v4ind, v5ind])
            sphere_indices.extend([v5ind, v4ind, v2ind])

create_sphere(icosahedron, ico_inds, 4)

start_time = time.time()

# Calculate uv coordinates to sphere
for vertex in icosahedron:
    u = math.atan2(vertex.normal.x, vertex.normal.z) / (2 * math.pi) + 0.5
    v = vertex.normal.y * 0.5 + 0.5
    vertex.uv = glm.vec2(u, v)


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
        self.model_matrix = glm.mat4(1.0)

    def init_context(self):
        # Read shader files and compile them
        vertex_shader_string = read_file("shaders/vertex_shader.glsl")
        fragment_shader_string = read_file("shaders/fragment_shader.glsl")
        vertex_shader = shaders.compileShader(vertex_shader_string, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(
            fragment_shader_string, GL_FRAGMENT_SHADER
        )
        self.shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
        # Textures from https://www.solarsystemscope.com/textures/ under CC BY 4.0 license
        self.context.texture_sun = TextureLoader("data/2k_sun.jpg")
        self.context.texture_earth = TextureLoader("data/2k_earth_daymap.jpg")
        self.context.texture_moon = TextureLoader("data/2k_moon.jpg")
        # Get location of the MVP matrix
        self.context.mvp_location = glGetUniformLocation(self.shader_program, "MVP")
        self.context.m_location = glGetUniformLocation(self.shader_program, "M")
        self.context.v_location = glGetUniformLocation(self.shader_program, "V")
        self.context.light_location = glGetUniformLocation(self.shader_program, "lightPosition")
        self.context.color_location = glGetUniformLocation(self.shader_program, "planetColor")
        self.context.light_bool_location = glGetUniformLocation(self.shader_program, "lightBool")
        self.context.texture_location = glGetUniformLocation(self.shader_program, "sampler")
        self.light_position = glm.vec4(0, 0, 0, 1)
        # Generate buffers for vertices and color data and buffer the data
        self.context.vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.context.vertex_buffer)
        ico_data = Vertex.todata(icosahedron)
        glBufferData(
            GL_ARRAY_BUFFER,
            len(ico_data) * 4,
            (GLfloat * len(ico_data))(*ico_data),
            GL_STATIC_DRAW,
        )
        self.context.index_buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.context.index_buffer)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            len(ico_inds) * 2,
            (GLushort * len(ico_inds))(*ico_inds),
            GL_STATIC_DRAW
        )
        
        glEnableVertexAttribArray(0)
        # 0th attribute, 3 numbers, floats, normalized=False, stride = 3 attributes * 3 numbers * 4 bytes
        #, offset = c pointer 2 attributes * 3 numbers * 4 bytes
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, Vertex.sizeof, None)
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, Vertex.sizeof, ctypes.c_void_p(3 * 4))
        
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, Vertex.sizeof, ctypes.c_void_p(3 * 4 + 2 * 4))


    def calc_mvp(self):
        self.calc_model()
        self.context.mvp = self.controller.calc_mvp(self.model_matrix)

    def resize(self, width, height):
        glViewport(0, 0, width, height)
        self.calc_mvp()

    def calc_model(self):
        pass

    def draw(self):
        """
        The main drawing function. Is called whenever an update occurs.
        
        Please implement the codes of Task 2, Task 3 and Task 4 described in our tutorial document.
        
        Task 2: Draw the moon.
        
        Task 3: The rotation of the sun, earth and moon.
        
        Task 4: The revolution of the earth and moon. 
        
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader_program)
        mvp_stack = []
        
        # Sun
        mvp_stack.append(glm.mat4(1.0))
        self.model_matrix = mvp_stack[-1]
        self.calc_mvp()
        glBindTexture(GL_TEXTURE_2D, self.context.texture_sun.id)
        glUniformMatrix4fv(self.context.mvp_location, 1, GL_FALSE, glm.value_ptr(self.context.mvp))
        glUniformMatrix4fv(self.context.m_location, 1, GL_FALSE, glm.value_ptr(self.model_matrix))
        glUniformMatrix4fv(self.context.v_location, 1, GL_FALSE, glm.value_ptr(self.controller.view_matrix))
        light_view = self.controller.view_matrix * (self.model_matrix * self.light_position)
        glUniform4fv(self.context.light_location, 1, glm.value_ptr(light_view))
        glUniform3f(self.context.color_location, 1, 1, 0)
        glUniform1f(self.context.light_bool_location, -1.0)
        glDrawElements(GL_TRIANGLES, len(ico_inds), GL_UNSIGNED_SHORT, None)
        
        # Earth
        glBindTexture(GL_TEXTURE_2D, self.context.texture_earth.id)
        mvp_stack[-1] = glm.scale(mvp_stack[-1], 0.1 * glm.vec3(1, 1, 1))
        mvp_stack[-1] = glm.translate(mvp_stack[-1], glm.vec3(-20, 0, 3))
        self.model_matrix = mvp_stack[-1]
        self.calc_mvp()
        glUniformMatrix4fv(self.context.mvp_location, 1, GL_FALSE, glm.value_ptr(self.context.mvp))
        glUniformMatrix4fv(self.context.m_location, 1, GL_FALSE, glm.value_ptr(self.model_matrix))
        glUniform3f(self.context.color_location, 0, 0, 1)
        glUniform1f(self.context.light_bool_location, 1.0)
        glDrawElements(GL_TRIANGLES, len(ico_inds), GL_UNSIGNED_SHORT, None)

        # Moon

        
        glUseProgram(0)


if __name__ == "__main__": 
    win = Win()
    win.controller = MVPController(win.update_if, width=win.width, height=win.height)
    win.init_opengl()
    win.init_context()
    win.run()