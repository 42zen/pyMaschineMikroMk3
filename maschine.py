import pymikro
import time


# MaschineMikroMk3 object controller
class MaschineMikroMk3:

    # create the Maschine object
    def __init__(self, screen_text=None):
        self.maschine = pymikro.MaschineMikroMk3()
        self.pads_count = 16
        self.pads = [ {'pushed': False, 'velocity': 0, 'color': None} ] * self.pads_count
        self.rotary_knob_pushed = False
        self.strip_pos = [0, 0]
        self.buttons_pressed = []
        self.screen_text = screen_text
        if screen_text is not None:
            self.screen_delay = 0.1
            self.set_screen_text(screen_text)

    # run the maschine controller
    def run(self):
        try:
            while True:
                self.frame()
        except KeyboardInterrupt:
            pass

    # run a maschine controller frame
    def frame(self):
        self.handle_next_event()
        if self.screen_text is not None:
            self.update_screen_text()

    # set the screen text
    def set_screen_text(self, text):
        self.current_screen_text = text
        self.maschine.setScreen(self.current_screen_text)
        self.screen_time = time.time() + self.screen_delay

    # set the screen text
    def update_screen_text(self):
        if self.screen_text != '':
            current_time = time.time()
            if current_time >= self.screen_time:
                if len(self.current_screen_text) == 0:
                    self.current_screen_text = (" " * 32) + self.screen_text
                else:
                    self.current_screen_text = self.current_screen_text[1:]
                self.screen_time = current_time + self.screen_delay
                self.maschine.setScreen(self.current_screen_text)

    # set a pad to a color
    def set_pad_color(self, pad_id, color, update=True):
        brightness = 2
        if color == 'black':
            color = 'white'
            brightness = 0
        self.maschine.setLight('pad', pad_id, brightness, color)
        self.pads[pad_id]['color'] = color
        if update == True:
            self.maschine.updLights()

    # set all pads to a color
    def set_pads_color(self, color):
        brightness = 2
        if color == 'black':
            color = 'white'
            brightness = 0
        for pad_id in range(self.pads_count):
            self.maschine.setLight('pad', pad_id, brightness, color)
            self.pads[pad_id]['color'] = color
        self.maschine.updLights()

    # TODO: set_pad_brightness, set_pads_brightness

    # TODO: set_button_light, set_buttons_light

    # handle the next event
    def handle_next_event(self):

        # parse the next command
        cmd = self.maschine.readCmd()
        if cmd is None:
            return

        # parse the pad event
        if cmd['cmd'] == 'pad':

            # check which pad is touched and it velocity
            pad_id = cmd['pad_nb']
            velocity = cmd['pad_val']

            # check if the pad was pushed
            pushed = False if cmd['released'] == True else True
            if pushed == True and velocity == 0:
                pushed = False

            # update the pad status
            if self.pads[pad_id]['pushed'] != pushed:
                self.pads[pad_id]['pushed'] = pushed
                if pushed == True:
                    self.pad_pushed(pad_id)
                else:
                    self.pad_released(pad_id)

            # update the pad velocity
            if self.pads[pad_id]['velocity'] != velocity:
                self.pads[pad_id]['velocity'] = velocity
                self.pad_velocity_changed(pad_id, velocity)
        
        # parse the btn event
        if cmd['cmd'] == 'btn':

            # check if the pressed buttons changed
            if self.buttons_pressed != cmd['btn_pressed']:

                # check all pressed button
                for button in cmd['btn_pressed']:
                    if button not in self.buttons_pressed:
                        self.button_pushed(button)

                # check all released button
                for button in self.buttons_pressed:
                    if button not in cmd['btn_pressed']:
                        self.button_released(button)

                # save the pressed buttons
                self.buttons_pressed = cmd['btn_pressed']

            # check if the rotary knob was touched
            if self.rotary_knob_pushed != cmd['encoder_touched']:
                self.rotary_knob_pushed = cmd['encoder_touched']
                if self.rotary_knob_pushed == True:
                    self.knob_touched()
                else:
                    self.knob_released()

            # check if the rotary knob was moved
            if cmd['encoder_move'] != 0:
                if cmd['encoder_move'] == 1:
                    self.knob_moved_right()
                else:
                    self.knob_moved_left()

            # check if the strip changed
            if cmd['strip_pos_1'] != self.strip_pos[0] or cmd['strip_pos_2'] != self.strip_pos[1]:

                # check if the previous strip was empty
                if self.strip_pos == [0, 0]:
                    if cmd['strip_pos_2'] == 0:
                        self.strip_pushed()
                    else:
                        self.strip_pushed(2)

                # check if the previous strip was only one finger
                elif self.strip_pos[1] == 0:

                    # check if there is no finger left
                    if cmd['strip_pos_1'] == 0:
                        self.strip_released()

                    # check if a finger was added
                    elif cmd['strip_pos_2'] != 0:
                        self.strip_pushed()

                # check if the previous strip was two fingers
                else:

                    # check if there is no finger left
                    if cmd['strip_pos_1'] == 0:
                        self.strip_released(2)

                    # check if a finger was removed
                    elif cmd['strip_pos_2'] == 0:
                        self.strip_released()

                # save the strip pos
                self.strip_pos = [ cmd['strip_pos_1'], cmd['strip_pos_2'] ]
                self.strip_pos_changed(self.strip_pos)

    # default events implementation
    def pad_pushed(self, pad_id): pass
    def pad_released(self, pad_id): pass
    def pad_velocity_changed(self, pad_id, velocity): pass
    def button_pushed(self, button): pass
    def button_released(self, button): pass
    def knob_touched(self): pass
    def knob_released(self): pass
    def knob_moved_right(self): pass
    def knob_moved_left(self): pass
    def strip_pushed(self, finger_count=1): pass
    def strip_released(self, finger_count=1): pass
    def strip_pos_changed(self, strip_pos): pass
