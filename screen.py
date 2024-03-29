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
        """
        Initializes a Screen object with the given width and height.

        Parameters:
            width (float): The width of the screen.
            height (float): The height of the screen.
        """
        self.__display = (width, height)
        self.__screen_center = (width // 2, height // 2)

        self.__obstacles: List[Obstacle] = []

        self.__walkers: List[Walker] = []
        self.__trails: Dict[Walker, List[vector3]] = {}
        self.__trails_lock = threading.Lock()
        self.__colors: Dict[Walker, vector3] = {}
        
        self.__run = True

    def initialize(self) -> None:
        """
        Initializes initializes the Pygame screen and sets up the OpenGL settings for rendering.
        It enables depth testing, lighting, color material, and sets up the projection and modelview matrices.
        """
        pygame.init()

        pygame.display.set_mode(self.__display, DOUBLEBUF | OPENGL)
        # enabling openGL settings
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_LIGHTING)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glColorMaterial(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE)
        # enabling openGL lightning
        GL.glEnable(GL.GL_LIGHT0)
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
        # setting up the matrix
        GL.glMatrixMode(GL.GL_PROJECTION)
        GLU.gluPerspective(45, (self.__display[0] / self.__display[1]), 0.1, 50000.0)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GLU.gluLookAt(*self.__STARTING_LOCATION, 0, 0, 0, 0, 0, 1)
        self.__view_matrix = GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX)
        GL.glLoadIdentity()

    def get_walkers(self) -> List[Walker]:
        """
        Returns a list of Walker objects currently on the screen.

        Returns:
            List[Walker]: A list of Walker objects.
        """
        return self.__walkers

    def add_walker(self, walker: Walker) -> None:
        """
        Adds a walker to the screen.

        Parameters:
            walker (Walker): The walker object to be added.
        """
        self.__walkers.append(walker)
        self.__trails[walker] = []
        self.__colors[walker] = (random.random(), random.random(), random.random())

    def remove_walker(self, walker: Walker) -> None:
        """
        Removes a walker from the screen.

        Args:
            walker (Walker): The walker object to be removed.
        """
        self.__walkers.remove(walker)
        self.__trails_lock.acquire()
        del self.__trails[walker]
        self.__trails_lock.release()

    def reset_trail(self, walker: Walker) -> None:
        """
        Resets the trail of a given walker.

        Parameters:
            walker (Walker): The walker whose trail needs to be reset.
        """
        self.__trails_lock.acquire()
        self.__trails[walker] = []
        self.__trails_lock.release()
        self.__colors[walker] = (random.random(), random.random(), random.random())

    def add_to_trail(self, walker: Walker, position: vector3) -> None:
        """
        Adds a position to the trail of a given walker.

        Args:
            walker (Walker): The walker object.
            position (vector3): The position to be added to the trail.
        """
        if walker in self.__trails:
            self.__trails[walker].append(position)
            
    def get_trails(self) -> Dict[Walker, List[vector3]]:
        """
        Returns a dictionary containing the trails of each walker.

        Returns:
            Dict[Walker, List[vector3]]: A dictionary where the keys are Walker objects and the values are lists of vector3 objects representing the trails.
        """
        return self.__trails

    def set_obstacles(self, obstacles: List[Obstacle]) -> None:
        """
        Set the obstacle list on the screen.

        Args:
            obstacles (List[Obstacle]): A list of obstacles to be set on the screen.
        """
        self.__obstacles = obstacles
        
    def get_obstacles(self) -> List[Obstacle]:
        """
        Returns the list of obstacles on the screen.

        Returns:
            List[Obstacle]: The list of obstacles on the screen.
        """
        return self.__obstacles

    def draw_line(self, starting_point: vector3, final_point: vector3, color: vector3) -> None:
        """
        Draws a line on the screen from the starting point to the final point with the specified color.

        Args:
            starting_point (vector3): The starting point of the line.
            final_point (vector3): The final point of the line.
            color (vector3): The color of the line.
        """
        GL.glColor3fv(color)
        GL.glLineWidth(5)
        GL.glBegin(GL.GL_LINES)
        GL.glVertex3fv(starting_point)
        GL.glVertex3fv(final_point)
        GL.glEnd()

    def render_sphere(self, location: vector3, radius: float, color: vector3) -> None:
        """
        Renders a sphere at the specified location with the given radius and color.

        Args:
            location (vector3): The location of the sphere.
            radius (float): The radius of the sphere.
            color (vector3): The color of the sphere.
        """
        GL.glTranslatef(*location)
        GL.glColor3f(*color)
        GLU.gluSphere(GLU.gluNewQuadric(), radius, 32, 16)
        GL.glTranslatef(-location[0], -location[1], -location[2])

    def render_all(self) -> None:
        """
        Renders all the elements in the simulation.
        """
        for walker in self.__walkers:
            # render walker
            self.render_sphere(walker.get_location(), 0.5, self.__WALKER_COLOR)
            # render trail
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
        """
        Moves the view by applying translation transformations.

        Args:
            movement (vector3): The translation vector representing the movement in x, y, and z coordinates.
        """
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
        """The screen main loop.

        Args:
            stop_event (threading.Event): An event to tell the simulation the screen is closed.
        """
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
        """Closes the screen.
        """
        pygame.quit()
    
    def stop(self) -> None:
        """Stops the screen loop.
        """
        self.__run = False
        
    def get_stop(self) -> bool:
        """Return if the screen is stopped or not.

        Returns:
            bool: Is the screen stopped.
        """
        return self.__run == False