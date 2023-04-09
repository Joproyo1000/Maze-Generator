from array import array

import pygame
import moderngl


class Shader:
    def __init__(self, resolution, settings):
        # initialize display
        self.display = pygame.Surface(resolution)
        self.t = 0

        self.settings = settings

        # initialize context
        self.ctx = moderngl.create_context()

        # initialize quad_buffer (basically creates a square with 2 triangles onto which the screen is rendered
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,  # topright
            -1.0, -1.0, 0.0, 1.0,  # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))

        # the vert_shader handles the calculations of the uvs
        self.vert_shader = open('vertShader.glsl').read()

        # the frag_shader handles the calculation of the color for each pixel
        self.frag_shader = open('oldTVShader.glsl').read()

        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def render(self, img):
        """
        :param img: image to render
        Renders the image applying color modification using GPU optimization
        """

        self.display.fill((0, 0, 0))
        self.display.blit(img, img.get_rect())

        self.t += 1

        frame_tex = self.surf_to_texture(self.display)
        frame_tex.use(0)
        self.program['tex'] = 0
        self.program['time'] = self.t
        self.program['gamma'] = self.settings.GAMMA / 10
        if self.settings.SHOWHEARTBEATEFFECT:
            self.program['dst'] = self.settings.dstToClosestEnemy
        else:
            self.program['dst'] = 0
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

        pygame.display.flip()

        frame_tex.release()

    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex
