import os

from pygame import mixer

current_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sfx_path = os.path.join(current_directory, 'sfx')

mixer.init(44100, -16, 2, 1024)

class Sound:
    def __init__(self):
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        self.sfx_channel = mixer.Channel(1)
        self.sfx_channel.set_volume(0.2)

        self.allowSFX = True

        self.soundtrack = mixer.Sound(sfx_path + "/" + "main_theme.ogg")
        self.coin = mixer.Sound(sfx_path + "/" + "coin.ogg")
        self.bump = mixer.Sound(sfx_path + "/" + "bump.ogg")
        self.stomp = mixer.Sound(sfx_path + "/" + "stomp.ogg")
        self.jump = mixer.Sound(sfx_path + "/" + "small_jump.ogg")
        self.death = mixer.Sound(sfx_path + "/" + "death.wav")
        self.kick = mixer.Sound(sfx_path + "/" + "kick.ogg")
        self.brick_bump = mixer.Sound(sfx_path + "/" + "brick-bump.ogg")
        self.powerup = mixer.Sound(sfx_path + "/" + 'powerup.ogg')
        self.powerup_appear = mixer.Sound(sfx_path + "/" + 'powerup_appears.ogg')
        self.pipe = mixer.Sound(sfx_path + "/" + 'pipe.ogg')

    def play_sfx(self, sfx):
        if self.allowSFX:
            self.sfx_channel.play(sfx)

    def play_music(self, music):
        self.music_channel.play(music)
