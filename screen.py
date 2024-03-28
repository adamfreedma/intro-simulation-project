import pygame
from pygame.locals import *
import OpenGL.GL as GL # type: ignore[import]
import OpenGL.GLU as GLU # type: ignore[import]
from custom_types import *
from custom_types import *
from typing import List, Dict
from walker import Walker
from obstacle import Obstacle
from teleporter import Teleporter
from speed_zone import SpeedZone
import random
import threading


class Screen:

    __STARTING_LOCATION = (20, -20, 20)
    INF = 50000
    __WALKER_COLOR = (0.2, 0.6, 0.2)

    def __init__(self, width: float, height: float) -> None:
        self.__display = (width, height)
        self.__screen_center = (width // 2, height // 2)

        self.__obstacles: List[Obstacle] = []

        self.__walkers: List[Walker] = []
        self.__trails: Dict[Walker, List[vector3]] = {}
        self.__trails_lock = threading.Lock()
        self.__colors: Dict[Walker, vector3] = {}
        self.__run = True

    def initialize(self) -> None:
        pygame.init()

        pygame.display.set_mode(self.__display, DOUBLEBUF | OPENGL)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glColorMaterial(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE)

        GL.glEnable(GL.GL_LIGHT0)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

        GL.glMatrixMode(GL.GL_PROJECTION)
        GLU.gluPerspective(45, (self.__display[0] / self.__display[1]), 0.1, 50000.0)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GLU.gluLookAt(*self.__STARTING_LOCATION, 0, 0, 0, 0, 0, 1)
        self.__view_matrix = GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX)
        GL.glLoadIdentity()

    def get_walkers(self) -> List[Walker]:
        return self.__walkers

    def add_walker(self, walker: Walker) -> None:
        self.__walkers.append(walker)
        self.__trails[walker] = []
        self.__colors[walker] = (random.random(), random.random(), random.random())

    def remove_walker(self, walker: Walker) -> None:
        self.__walkers.remove(walker)
        self.__trails_lock.acquire()
        del self.__trails[walker]
        self.__trails_lock.release()

    def reset_trail(self, walker: Walker) -> None:
        self.__trails_lock.acquire()
        self.__trails[walker] = []
        self.__trails_lock.release()
        self.__colors[walker] = (random.random(), random.random(), random.random())

    def add_to_trail(self, walker: Walker, position: vector3) -> None:
        if walker in self.__trails:
            self.__trails[walker].append(position)
            
    def get_trails(self) -> Dict[Walker, List[vector3]]:
        return self.__trails

    def set_obstacles(self, obstacles: List[Obstacle]) -> None:
        self.__obstacles = obstacles
        
    def get_obstacles(self) -> List[Obstacle]:
        return self.__obstacles

    def draw_line(self, starting_point: vector3, final_point: vector3, color: vector3) -> None:
        GL.glColor3fv(color)
        GL.glLineWidth(5)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3fv(starting_point)
        GL.glVertex3fv(final_point)
        GL.glEnd()

    def render_sphere(self, location: vector3, radius: float, color: vector3) -> None:

        GL.glTranslatef(*location)
        GL.glColor3f(*color)
        GLU.gluSphere(GLU.gluNewQuadric(), radius, 32, 16)
        GL.glTranslatef(-location[0], -location[1], -location[2])

    def render_all(self) -> None:
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


        # render obstacles
        for obstacle in self.__obstacles:
            if type(obstacle) == Obstacle:
                self.render_sphere(
                    obstacle.get_location(), obstacle.get_radius(), (0.1, 0.1, 0.1)
                )
            elif type(obstacle) == Teleporter:
                self.render_sphere(
                    obstacle.get_location(), obstacle.get_radius(), (0.1, 0.1, 0.5)
                )
            elif type(obstacle) == SpeedZone:
                self.render_sphere(
                    obstacle.get_location(), obstacle.get_radius(), obstacle.get_color()
                )

        # drawing the axis
        self.draw_line((-self.INF, 0, 0), (self.INF, 0, 0), (1, 0, 0))
        self.draw_line((0, -self.INF, 0), (0, self.INF, 0), (0, 1, 0))
        self.draw_line((0, 0, -self.INF), (0, 0, self.INF), (0, 0, 1))

    def move(self, movement: vector3) -> None:
        # init model view matrix
        GL.glLoadIdentity()
        # init the view matrix
        GL.glPushMatrix()
        GL.glLoadIdentity()
        GL.glTranslatef(*movement)
        # apply the left and right rotation
        # multiply the current matrix by the get the new view matrix and store the final vie matrix
        GL.glMultMatrixf(self.__view_matrix)
        self.__view_matrix = GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX)
        # apply view matrix
        GL.glPopMatrix()
        GL.glMultMatrixf(self.__view_matrix)

        GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, [1, -1, 1, 0])

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(1, 1, 1, 1)

        GL.glPushMatrix()
        self.render_all()
        GL.glPopMatrix()

        pygame.display.flip()

    def run(self, stop_event: threading.Event) -> None:
        self.initialize()

        # init mouse movement and center mouse on screen
        displayCenter = [self.__display[i] // 2 for i in range(2)]
        pygame.mouse.set_pos(displayCenter)

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
                GL.glLoadIdentity()
                # init the view matrix
                GL.glPushMatrix()
                GL.glLoadIdentity()

                movement = (0.0, 0.0, 0.0)
                # apply the movement
                if keypress[pygame.K_s]:
                    movement = (0.0, 0.0, -0.5)
                if keypress[pygame.K_w]:
                    movement = (0.0, 0.0, 0.5)
                if keypress[pygame.K_d]:
                    movement = (-0.5, 0.0, 0.0)
                if keypress[pygame.K_a]:
                    movement = (0.5, 0.0, 0.0)
                if keypress[pygame.K_SPACE]:
                    movement = (0.0, -0.5, 0.0)
                if keypress[pygame.K_LSHIFT]:
                    movement = (0.0, 0.5, 0.0)

                GL.glPopMatrix()
                self.move(movement)

                pygame.time.wait(10)

        stop_event.set()
        self.close()
        
    def close(self) -> None:
        pygame.quit()
    
    def stop(self) -> None:
        self.__run = False
        
    def get_stop(self) -> bool:
        return self.__run == False