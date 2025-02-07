import numpy as np
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import QOpenGLShaderProgram, QOpenGLShader
from PySide6.QtGui import QOpenGLFunctions, QSurfaceFormat
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_COMPONENT, GL_DEPTH_TEST, GL_FLOAT, GL_LESS, GL_LIGHTING, GL_MODELVIEW, GL_PROJECTION, GL_VIEWPORT, GL_FALSE
from PIL import Image
import Sofa.SofaGL
import Sofa.Simulation


class SofaWidget(QOpenGLWidget, QOpenGLFunctions):
    def __init__(self, sofa_visuals_node):
        super().__init__()
        # QOpenGLFunctions.__init__(self)

        # self.initializeOpenGLFunctions()

        self.visuals_node = sofa_visuals_node
        self.camera = sofa_visuals_node.camera
        # self.setMinimumSize(800, 600)
        self.z_far = sofa_visuals_node.camera.findData('zFar').value
        self.z_near = sofa_visuals_node.camera.findData('zNear').value

    def initializeGL(self):
        # print('not yet crashed')
        QOpenGLFunctions.__init__(self)
        self.initializeOpenGLFunctions()
        # print('not yet crashed')
        self.glViewport(0, 0, self.width(), self.height())
        self.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.glEnable(GL_LIGHTING)
        self.glEnable(GL_DEPTH_TEST)
        self.glDepthFunc(GL_LESS)
        print('not yet crashed2')
        Sofa.SofaGL.glewInit()
        print('not yet crashed3')
        # Sofa.Simulation.initVisual(self.visuals_node)
        # print('not yet crashed4')
        # Sofa.Simulation.initTextures(self.visuals_node)
        # print('not yet crashed5')

        # # DEPRICATED!!!
        # self.glMatrixMode(GL_PROJECTION)
        # self.glLoadIdentity()
        # self.gluPerspective(45, (self.width() / self.height()), 0.1, 50.0)
        # self.glMatrixMode(GL_MODELVIEW)
        # self.glLoadIdentity()
        # Convert matrices to NumPy arrays

        shader = QOpenGLShader(QOpenGLShader.Vertex)
        shader.compileSourceCode("""#version 330 core

layout(location = 0) in vec3 a_Position;  // Vertex-Position als Input

uniform mat4 u_ModelViewMatrix;  // SOFA Model-View-Matrix
uniform mat4 u_ProjectionMatrix; // SOFA Projektionsmatrix

void main() {
    gl_Position = u_ProjectionMatrix * \
        u_ModelViewMatrix * vec4(a_Position, 1.0);
}""")
        self.shader_program = QOpenGLShaderProgram()
        self.shader_program.addShader(shader)
        # self.glUseProgram(self.shader_program.)
        self.shader_program.link()

        modelview_matrix = np.array(
            self.camera.getOpenGLModelViewMatrix(), dtype=np.float32)
        projection_matrix = np.array(
            self.camera.getOpenGLProjectionMatrix(), dtype=np.float32)

        # Get shader locations
        modelview_loc = self.glGetUniformLocation(
            self.shader_program, "u_ModelViewMatrix")
        projection_loc = self.glGetUniformLocation(
            self.shader_program, "u_ProjectionMatrix")

        # Upload to shader
        self.glUniformMatrix4fv(modelview_loc, 1, GL_FALSE, modelview_matrix)
        self.glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection_matrix)

    def paintGL(self):
        self.glViewport(0, 0, self.width(), self.height())
        self.glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # # DEPRICATED!!!
        # self.glMatrixMode(GL_PROJECTION)
        # self.glLoadIdentity()
        # self.gluPerspective(45, (self.width() / self.height()), 0.1, 50.0)
        # self.glMatrixMode(GL_MODELVIEW)
        # self.glLoadIdentity()

        modelview_matrix = np.array(
            self.camera.getOpenGLModelViewMatrix(), dtype=np.float32)
        projection_matrix = np.array(
            self.camera.getOpenGLProjectionMatrix(), dtype=np.float32)

        # Get shader locations
        modelview_loc = self.glGetUniformLocation(
            self.shader_program, "u_ModelViewMatrix")
        projection_loc = self.glGetUniformLocation(
            self.shader_program, "u_ProjectionMatrix")

        self.glUniformMatrix4fv(modelview_loc, 1, GL_FALSE, modelview_matrix)
        self.glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection_matrix)

        # cameraMVM = self.visuals_node.camera.getOpenGLModelViewMatrix()
        # self.glMultMatrixd(cameraMVM)

        # Sofa.SofaGL.draw(self.visuals_node)

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
