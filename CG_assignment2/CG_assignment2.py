from OpenGL.GL import *
import glm
from utils.obj_loader import ObjLoader
from utils.texture_loader import TextureLoader
from utils.glut_window import GlutWindow
from utils.mvp_controller import MVPController
from OpenGL.GL import shaders


# Define our object (Texture-mapped 2x2x2 cube centered at origin).
# 
# Because we need different texture coordinates (and normal coordinates for lighting calculations), we need to define different vertices
# for all the different parameter combinations even when position coordinates for the same vertex are the same. If _all_ the used vertex
# properties (position, normal, texture coordinates, vertex color, ...) are the same, we can reuse the same index value! This happens
# in this example when we define triangles that form each side of the cube.
#
# All the triangles should be defined in counter-clockwise orientation!!
#

'''
1. fill here your code to draw the cube with 12 pieces of triangles
'''
#     Vertex names for our cube
#            v8      v7
#            *------*     y
#           /|     /|     ^
#        v4/ |  v3/ |     |
#         *--*---*--*v6   +--->x
#         | /v5  | /     /
#         |/     |/     z
#         *------*
#        v1      v2
#

#-1.0,-1.0, 1.0, #v1
# 1.0,-1.0, 1.0, #v2
# 1.0, 1.0, 1.0, #v3
#-1.0, 1.0, 1.0, #v4
#-1.0,-1.0,-1.0, #v5
# 1.0,-1.0,-1.0, #v6
# 1.0, 1.0,-1.0, #v7
#-1.0, 1.0,-1.0, #v8


vertex_buffer_data = [
                #Front side
                #draw the triangle 1 for front side, v1, v2, v3
                -1.0,-1.0, 1.0, #v1
                 1.0,-1.0, 1.0, #v2
                 1.0, 1.0, 1.0, #v3
                #draw the triangle 2 of front side, v3, v4, v1
                 0,0,0,
		 0,0,0,
		 0,0,0,
                
                #Right side
                #draw the triangle 3 of right side, v2, v6, v7
                 0,0,0,
		 0,0,0,
		 0,0,0,
                #draw the triangle 4 of right side, v7, v3, v2
                 0,0,0,
		 0,0,0,
		 0,0,0,
                
                #Bottom side
                #draw the triangle 5 of bottom side, v1, v6, v2
                 0,0,0,
		 0,0,0,
		 0,0,0,

                #draw the triangle 6 of bottom side, v6, v1, v5
                 0,0,0,
		 0,0,0,
		 0,0,0,

                
                #Top side
                #draw the triangle 7 of top side, v4, v3, v7
                 0,0,0,
		 0,0,0,
		 0,0,0,
                #draw the triangle 8 of top side, v7, v8, v4
                 0,0,0,
		 0,0,0,
		 0,0,0,
                
                #Left side
                #draw the triangle 9 of left side, v5, v1, v4
                 0,0,0,
		 0,0,0,
		 0,0,0,
                #draw the triangle 10 of left side, v4, v8, v5
                 0,0,0,
		 0,0,0,
		 0,0,0,
                
                #Back side
                #draw the triangle 11 of back side, v6, v5, v8
                 0,0,0,
		 0,0,0,
		 0,0,0,

                #draw the triangle 12 of back side, v8, v7, v6
                 0,0,0,
		 0,0,0,
		 0,0,0,
]        


                 
# Texture coordinates with labeled sides      Vertex names for our cube
#                                                   v8      v7
#  3/3+---+---+---+         v                         *------*     y
#     | 1 | 2 | 3 |        ^                         /|     /|     ^
#  2/3+---+---+---+        |                     v4/ |  v3/ |     |
#     | 4 | 5 | 6 |        +--->u                 *--*---*--*v6   +--->x
#  1/3+---+---+---+                               | /v5  | /     /
#     |   |   |   |                               |/     |/     z
#    0+---+---+---+                               *------*
#     0  1/3 2/3 3/3                             v1      v2
#

# After we have defined each side, we also define vertex index values that are used for actual triangles that are drawn.


'''
2. fill here your code to map the texture to the cube with 12 pieces of triangles
'''
                
uv_buffer_data = [
                
                #Front side with texutre number 1
                #map the texture to the triangle 1 of side, v1, v2, v3
                0.0 / 3.0, 2.0 / 3.0, #v1
		1.0 / 3.0, 2.0 / 3.0, #v2
		1.0 / 3.0, 3.0 / 3.0, #v3
                #map the texture to the triangle 2 of side, v3, v4, v1
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,
                
                #Right side with texutre number 2
                #map the texture to the triangle 1 of side, v2, v6, v7
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,
                #map the texture to the triangle 2 of side, v7, v3, v2
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,
                
                #Bottom side with texutre number 3
                #map the texture to the triangle 1 of side, v1, v6, v2
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,

                #map the texture to the triangle 2 of side, v6, v1, v5
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,

                
                #Top side with texutre number 4
                #map the texture to the triangle 1 of side, v4, v3, v7
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,
                #map the texture to the triangle 2 of side, v7, v8, v4
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,
                
                #Let side with texutre number 5
                #map the texture to the triangle 1 of side, v5, v1, v4
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,
                #map the texture to the triangle 2 of side, v4, v8, v5
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,
                
                #Back side with texutre number 6
                #map the texture to the triangle 1 of side, v6, v5, v8
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,
                #map the texture to the triangle 2 of side, v8, v7, v6
                0.0, 0.0,
		0.0, 0.0,
		0.0, 0.0,
]

def read_file(file_path: str) -> str:
        """Reads a text file given a path and returns it as a string."""
        with open(file_path, mode="r") as f:
                contents = f.readlines()
        return contents


class GLContext:
        """Used for storing context data in the main window."""
        pass


class Win(GlutWindow):
        def __init__(self, width: int = 800, height: int = 480):
                super().__init__(width, height)
                self.context = GLContext()

        def init_shaders(self):
                vertex_shader_string = read_file("resources/vertex_shader.glsl")
                fragment_shader_string = read_file("resources/fragment_shader.glsl")
                vertex_shader = shaders.compileShader(vertex_shader_string, GL_VERTEX_SHADER)
                fragment_shader = shaders.compileShader(
                        fragment_shader_string, GL_FRAGMENT_SHADER
                )
                shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
                return shader_program

        def init_context_raw(self):
                self.shader_program = self.init_shaders()

                self.context.mvp_location = glGetUniformLocation(self.shader_program, "mvp")
                self.context.texture_location = glGetUniformLocation(self.shader_program,
                                                                     "texture_sampler")

                texture = TextureLoader("resources/uvtemplate.png")
                
                self.context.textureGLID = texture.textureGLID

                self.context.vertexbuffer  = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
                glBufferData(
                        GL_ARRAY_BUFFER,
                        len(vertex_buffer_data) * 4,
                        (GLfloat * len(vertex_buffer_data))(*vertex_buffer_data),
                        GL_STATIC_DRAW
                )

                if texture.inversedVCoords:
                        for index in range(len(uv_buffer_data)):
                                if(index % 2):
                                        uv_buffer_data[index] = 1.0 - uv_buffer_data[index]

                '''
		3. fill here your code to define data buffer for storing the
		cube's texture (uv).
		'''
                
                
        def init_context_load(self):
                '''
		4. fill here your code to complete the init_context_load function to
		load an external object instead of drawing one with raw triangle.
		'''

                

        def calc_mvp(self):
                self.calc_model()
                self.context.mvp = self.controller.calc_mvp(self.model_matrix)
                
        def resize(self, width, height):
                glViewport(0, 0, width, height)
                self.calc_mvp()

        def calc_model(self):
                self.model_matrix = glm.mat4(1)

        def draw(self):
                """
                The main drawing function. Is called whenever an update occurs.
                """
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                self.calc_mvp()
                glUseProgram(self.shader_program)
                glUniformMatrix4fv(
                        self.context.mvp_location,
                        1,
                        GL_FALSE,
                        glm.value_ptr(self.context.mvp))

                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, self.context.textureGLID)
                glUniform1i(self.context.texture_location, 0)

                glEnableVertexAttribArray(0)
                glBindBuffer(GL_ARRAY_BUFFER, self.context.vertexbuffer)
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
                '''
		3. fill here your code to to enable and bind the texture buffer.
		'''

                
                glDrawArrays(GL_TRIANGLES, 0, int(len(vertex_buffer_data) / 3))

                glDisableVertexAttribArray(0)
                glDisableVertexAttribArray(1)
                glUseProgram(0)
        

if __name__ == "__main__":
        win = Win()
        win.controller = MVPController(win.update_if, width=win.width, height=win.height)
        win.init_opengl()
        
        #win.init_context_load()
        win.init_context_raw()
        win.run()
