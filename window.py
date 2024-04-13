import sdl2.ext
import sdl2


# color enum list
class color:
    black = sdl2.ext.Color(0, 0, 0)
    white = sdl2.ext.Color(255, 255, 255)
    red = sdl2.ext.Color(255, 0, 0)
    green = sdl2.ext.Color(0, 255, 0)
    blue = sdl2.ext.Color(0, 0, 255)


# Window object controller
class Window:

    # create a window
    def __init__(self, window_name=""):

        # init the SDL2 library
        sdl2.ext.init()

        # set the window in fullscreen
        sdl2.SDL_ShowCursor(sdl2.SDL_DISABLE)
        display_mode = sdl2.SDL_DisplayMode()
        sdl2.SDL_GetCurrentDisplayMode(0, display_mode)

        # create the window and renderer
        self.window = sdl2.ext.Window(window_name, size=(display_mode.w, display_mode.h), flags=sdl2.SDL_WINDOW_BORDERLESS)
        self.renderer = sdl2.ext.Renderer(self.window, flags=sdl2.SDL_RENDERER_ACCELERATED)

        # render the window
        self.set_color(color.black)
        self.window.show()

    # change the window color
    def set_color(self, color):
        self.renderer.color = color
        self.renderer.clear()
        self.renderer.present()
