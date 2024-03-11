import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from custom_types import *
from custom_types import *
from typing import List, Dict
from walker import Walker
import random


class Screen:

    __STARTING_LOCATION = (20, -20, 20)
    INF = 50000
    __WALKER_COLOR = (0.2, 0.6, 0.2)

    def __init__(self, width: float, height: float):
        self.__display = (width, height)
        self.__screen_center = (width // 2, height // 2)

        self.__pitch = 0

        self.__walkers: List[Walker] = []
        self.__trails: Dict[Walker, List[vector3]] = {}
        self.__colors: Dict[Walker, vector3] = {}

    def initialize(self):
        pygame.init()

        pygame.display.set_mode(self.__display, DOUBLEBUF | OPENGL)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.__display[0] / self.__display[1]), 0.1, 50000.0)

        glMatrixMode(GL_MODELVIEW)
        gluLookAt(*self.__STARTING_LOCATION, 0, 0, 0, 0, 0, 1)
        self.__view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()

    def add_walker(self, walker: Walker):
        self.__walkers.append(walker)
        self.__trails[walker] = []
        self.__colors[walker] = (random.random(), random.random(), random.random())

    def remove_walker(self, walker: Walker):
        self.__walkers.remove(walker)
        del self.__trails[walker]

    def reset_trail(self, walker: Walker):
        self.__trails[walker] = []
        self.__colors[walker] = (random.random(), random.random(), random.random())

    def add_to_trail(self, walker: Walker, position: vector3):
        if walker in self.__trails:
            self.__trails[walker].append(position)

    def draw_line(self, starting_point: vector3, final_point: vector3, color: vector3):
        glColor3fv(color)
        glLineWidth(5)
        glBegin(GL_LINES)
        glVertex3fv(starting_point)
        glVertex3fv(final_point)
        glEnd()

    def render_sphere(self, location: vector3, radius: float, color: vector3):

        glTranslatef(*location)
        glColor3fv(color)
        gluSphere(gluNewQuadric(), radius, 32, 16)
        glTranslatef(-location[0], -location[1], -location[2])

    def render_all(self):
        for walker in self.__walkers:
            self.render_sphere(walker.get_location(), 1, self.__WALKER_COLOR)

            if walker in self.__trails:
                for step in range(len(self.__trails[walker]) - 1):
                    # making sure the other thread isn't changing the trail
                    if self.__trails[walker]:
                        self.draw_line(
                            self.__trails[walker][step],
                            self.__trails[walker][step + 1],
                            self.__colors[walker],
                        )

        self.draw_line((-self.INF, 0, 0), (self.INF, 0, 0), (1, 0, 0))
        self.draw_line((0, -self.INF, 0), (0, self.INF, 0), (0, 1, 0))
        self.draw_line((0, 0, -self.INF), (0, 0, self.INF), (0, 0, 1))

    def move(self, movement: vector3):
        # init model view matrix
        glLoadIdentity()
        # init the view matrix
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(*movement)
        # apply the left and right rotation
        # multiply the current matrix by the get the new view matrix and store the final vie matrix
        glMultMatrixf(self.__view_matrix)
        self.__view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        # apply view matrix
        glPopMatrix()
        glMultMatrixf(self.__view_matrix)

        glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(1, 1, 1, 1)

        glPushMatrix()
        self.render_all()
        glPopMatrix()

        pygame.display.flip()

    def run(self):
        self.initialize()

        # init mouse movement and center mouse on screen
        displayCenter = [self.__display[i] // 2 for i in range(2)]
        mouse_change = [0, 0]
        pygame.mouse.set_pos(displayCenter)

        up_down_angle = 0.0
        paused = False
        run = True
        while run:
            for event in pygame.event.get():
                # checking for quits/ pauses
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        run = False
                    if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                        paused = not paused
                        pygame.mouse.set_pos(self.__screen_center)

            if not paused:
                # get keys
                keypress = pygame.key.get_pressed()

                # init model view matrix
                glLoadIdentity()
                # init the view matrix
                glPushMatrix()
                glLoadIdentity()

                movement = (0, 0, 0)
                # apply the movement
                if keypress[pygame.K_s]:
                    movement = (0, 0, -0.5)
                if keypress[pygame.K_w]:
                    movement = (0, 0, 0.5)
                if keypress[pygame.K_d]:
                    movement = (-0.5, 0, 0)
                if keypress[pygame.K_a]:
                    movement = (0.5, 0, 0)
                if keypress[pygame.K_SPACE]:
                    movement = (0, -0.5, 0)
                if keypress[pygame.K_LSHIFT]:
                    movement = (0, 0.5, 0)

                glPopMatrix()
                self.move(movement)

                pygame.time.wait(10)

    pygame.quit()
