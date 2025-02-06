import numpy as np
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import QOpenGLVersionFunctionsFactory, QOpenGLVersionProfile
from PySide6.QtGui import QOpenGLFunctions, QSurfaceFormat
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_COMPONENT, GL_DEPTH_TEST, GL_FLOAT, GL_LESS, GL_LIGHTING, GL_MODELVIEW, GL_PROJECTION, GL_VIEWPORT
from PIL import Image
import Sofa.SofaGL
import Sofa.Simulation


class SofaWidget(QOpenGLWidget, QOpenGLFunctions):
    def __init__(self, sofa_visuals_node):
        QOpenGLWidget.__init__(self)
        self.initializeOpenGLFunctions()
        profile = QOpenGLVersionProfile()
        profile.setVersion(3, 2)
        profile.setProfile(
            QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)
        self.funcs = QOpenGLVersionFunctionsFactory.get(profile)
        self.funcs.initializeOpenGLFunctions()

        self.visuals_node = sofa_visuals_node
        # self.setMinimumSize(800, 600)
        self.z_far = sofa_visuals_node.camera.findData('zFar').value
        self.z_near = sofa_visuals_node.camera.findData('zNear').value

    def initializeGL(self):
        self.glViewport(0, 0, self.width(), self.height())
        self.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.glEnable(GL_LIGHTING)
        self.glEnable(GL_DEPTH_TEST)
        self.glDepthFunc(GL_LESS)
        Sofa.SofaGL.glewInit()
        Sofa.Simulation.initVisual(self.visuals_node)
        Sofa.Simulation.initTextures(self.visuals_node)
        self.funcs.glMatrixMode(GL_PROJECTION)
        self.funcs.glLoadIdentity()
        self.gluPerspective(45, (self.width() / self.height()), 0.1, 50.0)
        self.glMatrixMode(GL_MODELVIEW)
        self.glLoadIdentity()

    def paintGL(self):
        self.glViewport(0, 0, self.width(), self.height())
        self.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.glMatrixMode(GL_PROJECTION)
        self.glLoadIdentity()
        self.gluPerspective(45, (self.width() / self.height()), 0.1, 50.0)
        self.glMatrixMode(GL_MODELVIEW)
        self.glLoadIdentity()

        cameraMVM = self.visuals_node.camera.getOpenGLModelViewMatrix()
        self.glMultMatrixd(cameraMVM)

        Sofa.SofaGL.draw(self.visuals_node)

    def get_depth_image(self):
        _, _, width, height = self.glGetIntegerv(GL_VIEWPORT)
        buff = self.glReadPixels(
            0, 0, width, height, GL_DEPTH_COMPONENT, GL_FLOAT)
        image = np.frombuffer(buff, dtype=np.float32)
        image = image.reshape(height, width)
        image = np.flipud(image)  # <-- image is now a numpy array you can use
        depth_image = -self.z_far*self.z_near / \
            (self.z_far + image*(self.z_near-self.z_far))
        depth_image = (depth_image - depth_image.min()) / \
            (depth_image.max() - depth_image.min())
        depth_image = depth_image * 255

        img2 = Image.fromarray(depth_image.astype(np.uint8), 'L')
        img2.show()
