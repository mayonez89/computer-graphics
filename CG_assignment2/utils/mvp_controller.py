import glm
import math


class MVPController:
    def __init__(self, callback_update, width: int, height: int):
        self.callback_update = callback_update
        self.width = width
        self.height = height
        self.position = glm.vec3(3, 3, 3)
        self.pitch = 0.5
        self.yaw = 0.5
        self.roll = 0.0
        self.speed = 0.4
        self.mouse_speed = 0.01
        self.fov = 90
        self.calc_view_projection()
        self.last_x = 0
        self.last_y = 0

    def calc_mvp(self, model_matrix=glm.mat4(1.0)):
        self.direction = glm.vec3(
            - math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch)),
            math.sin(glm.radians(self.pitch)),
            math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))

        )
        self.right = glm.normalize(glm.cross(glm.vec3(0, 1, 0), self.direction))
        self.up = glm.cross(self.direction, self.right)
        self.view_matrix = glm.lookAt(self.position,
                                      self.position + self.direction,
                                      self.up)

        self.projection_matrix = glm.perspective(glm.radians(self.fov), self.width / self.height, 0.1, 1000)
        return self.projection_matrix * self.view_matrix * model_matrix

    def calc_view_projection(self):
        self.direction = glm.vec3(-2, -2, -2.5)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(0, 1, 0)
        self.view_matrix = glm.lookAt(self.position,
                          self.position + self.direction,
                          self.up)

        self.projection_matrix = glm.perspective(glm.radians(self.fov), self.width / self.height, 0.1, 1000)

    def on_keyboard(self, key: bytes, x: int, y: int):

        vector = glm.vec3(0, 0, 0)
        if key == b'w':
            # forward
            vector = glm.vec3(+1, 0, 0)
        if key == b'a':
            # left
            vector = glm.vec3(0, 0, +1)
        if key == b'd':
            # right
            vector = glm.vec3(0, 0, -1)
        if key == b's':
            # backward
            vector = glm.vec3(-1, 0, 0)
        if key == b'e':
            # up
            vector = glm.vec3(0, +1, 0)
        if key == b'r':
            # down
            vector = glm.vec3(0, -1, 0)

        self.position -= vector * self.speed

        self.calc_view_projection()
        self.callback_update()

    def on_mouse(self, key: int, up: int, x: int, y: int):
        if key == 0 and up == 0:
            self.last_x = x
            self.last_y = y

    def on_mousemove(self, x: int, y: int):
        x_diff = self.last_x - x
        y_diff = self.last_y - y
        self.last_x = x
        self.last_y = y
        self.yaw -= y_diff * self.mouse_speed
        self.pitch -= x_diff * self.mouse_speed
        # print(self.yaw)
        # print(self.pitch)
        self.calc_view_projection()
        self.callback_update()

    def on_special_key(self, *args):
        pass

