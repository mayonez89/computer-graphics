# -------------------------------------------------------------------------------
# Name: 521140S：4 Computer Graphics (2022) Programming Assignment 0 
# Purpose: Environment setting for Python and OpenGL
# Copyright (C) 2019 Haoyu Chen <chenhaoyucc@icloud.com>,
# author: Chen Haoyu

# Center of Machine Vision and Signal Analysis (CMVS),
# Department of Computer Science and Engineering,
# University of Oulu, Oulu, 90570, Finland
# -------------------------------------------------------------------------------
""" This file contains different utility functions that are not connected
in anyway to the networks presented in the tutorials, but rather help in
processing the outputs into a more understandable way.

"""

import OpenGL.GLUT as oglut
import OpenGL.GL as gl
import OpenGL.GLU as glu


class GlutWindow(object):

    def __init__(self):
        oglut.glutInit()

        # initialize display mode
        oglut.glutInitDisplayMode(oglut.GLUT_RGBA | oglut.GLUT_DOUBLE | oglut.GLUT_DEPTH)

        '''1. change different window size here'''
        # change the parameter of glutInitWindowSize(int width, int height)
        oglut.glutInitWindowSize(800, 480)
        oglut.glutCreateWindow(b"CG_Programming_Assignment_0")
        oglut.glutDisplayFunc(self.display)
        oglut.glutReshapeFunc(self.resize)

    def ogl_draw(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        '''2. change a different Polygon mode here'''
        # glPolygonMode(	GLenum face, GLenum mode): GL_FRONT ==> GL_FRONT_AND_BACK
        gl.glPolygonMode(gl.GL_FRONT, gl.GL_LINE)
        glu.gluLookAt(4.0, 3.0, -3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        '''3. change a different model here'''
        # model types can be find here: https://www.opengl.org/resources/libraries/glut/spec3/node80.html
        # Note: different objects have different input parameters
        # glutSolidCube ==> glutSolidTeapot
        oglut.glutSolidCube(1)

    def display(self):
        self.ogl_draw()
        oglut.glutSwapBuffers()

    def resize(self, Width, Height):
        gl.glViewport(0, 0, Width, Height)
        glu.gluPerspective(45.0, float(Width) / float(Height), 0.1, 1000.0)

    def run(self):
        oglut.glutMainLoop()


if __name__ == "__main__":
    win = GlutWindow()
    win.run()
