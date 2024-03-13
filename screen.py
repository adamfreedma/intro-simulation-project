import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from custom_types import *
from custom_types import *
from typing import List, Dict
from walker import Walker
from obstacle import Obstacle
from teleporter import Teleporter
import random
import threading


class Screen:

    __STARTING_LOCATION = (20, -20, 20)
    INF = 50000
    __WALKER_COLOR = (0.2, 0.6, 0.2)

    def __init__(self, width: float, height: float):
        self.__display = (width, height)
        self.__screen_center = (width // 2, height // 2)

        self.__obstacles: List[Obstacle] = []
        self.__teleporters: List[Teleporter] = []

        self.__walkers: List[Walker] = []
        self.__trails: Dict[Walker, List[vector3]] = {}
        self.__trails_lock = threading.Lock()
        self.__colors: Dict[Walker, vector3] = {}
        self.__run = True

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
        self.__trails_lock.acquire()
        del self.__trails[walker]
        self.__trails_lock.release()

    def reset_trail(self, walker: Walker):
        self.__trails_lock.acquire()
        self.__trails[walker] = []
        self.__trails_lock.release()
        self.__colors[walker] = (random.random(), random.random(), random.random())

    def add_to_trail(self, walker: Walker, position: vector3):
        if walker in self.__trails:
            self.__trails[walker].append(position)

    def set_teleporters(self, teleporters: List[Teleporter]):
        self.__teleporters = teleporters

    def set_obstacles(self, obstacles: List[Obstacle]):
        self.__obstacles = obstacles

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
            self.render_sphere(walker.get_location(), 0.5, self.__WALKER_COLOR)

            self.__trails_lock.acquire()
            if walker in self.__trails:
                for step in range(len(self.__trails[walker]) - 1):
                    self.draw_line(
                        self.__trails[walker][step],
                        self.__trails[walker][step + 1],
                        self.__colors[walker],
                    )
            self.__trails_lock.release()

        # render teleporters
        for teleporter in self.__teleporters:
            self.render_sphere(
                teleporter.get_location(), teleporter.get_radius(), (0.1, 0.1, 0.5)
            )

        # render obstacles
        for obstacle in self.__obstacles:
            self.render_sphere(
                obstacle.get_location(), obstacle.get_radius(), (0.1, 0.1, 0.1)
            )

        # drawing the axis
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

    def run(self, stop_event: threading.Event):
        self.initialize()

        # init mouse movement and center mouse on screen
        displayCenter = [self.__display[i] // 2 for i in range(2)]
        mouse_change = [0, 0]
        pygame.mouse.set_pos(displayCenter)

        up_down_angle = 0.0
        paused = False
        self.__run = True
        while self.__run:
            for event in pygame.event.get():
                # checking for quits/ pauses
                if event.type == pygame.QUIT:
                    self.__run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.__run = False
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

        stop_event.set()
        pygame.quit()

    
    def stop(self):
        self.__run = False