import math
from pyonfx import *
import random

# https://pyonfx.readthedocs.io/en/latest/
io = Ass("Universe - Official HigeDANdism.ass")
io.path_output = "gen.ass"
meta, styles, lines = io.get_data()

# Creating the star and extracting all the color changes from the input file
star = Shape.star(5, 4, 10)

rand_radius = random.uniform(6, 17)
circle = Shape.ellipse(rand_radius, rand_radius)

COLOR_GREY = "#8F8F8F"
COLOR_CRIMSON = "#BE6C6C"
COLOR_YELLOW = "#E6CD80"
COLOR_GREEN = "#B3FFBE"
COLOR_AZURE = "#A6F7EE"
COLOR_BLUE = "#98D5F4"
COLOR_DARK_BLUE = "#869FED"
COLOR_VIOLET = "#AF96E5"
COLOR_DARK_PINK = "#E099EC"
COLOR_APPLE = "#D391A8"


def romaji(line: Line, l: Line):
    # Random color per line
    random_color = random.choice(
        [
            COLOR_GREY,
            COLOR_CRIMSON,
            COLOR_YELLOW,
            COLOR_GREEN,
            COLOR_AZURE,
            COLOR_BLUE,
            COLOR_DARK_BLUE,
            COLOR_VIOLET,
            COLOR_DARK_PINK,
            COLOR_APPLE
        ]
    )

    for syl in Utils.all_non_empty(line.syls):
        delay = 300

        # Leadin
        l.start_time = line.start_time + 25 * syl.i - delay - 80
        l.end_time = line.start_time + syl.start_time
        l.duration = l.end_time - l.start_time

        l.text = (
            "{\\an5\\move(%.3f, %.3f, %.3f, %.3f, 0, %d)\\fad(%d, 0)}%s"
        ) % (
            syl.center,
            syl.middle - 20,
            syl.center,
            syl.middle,
            delay,
            delay,
            syl.text
        )

        io.write_line(l)

        # Main Effect 1 - Scale
        l.layer = 1
        l.start_time = line.start_time + syl.start_time
        l.end_time = line.start_time + syl.end_time
        l.duration = l.end_time - l.start_time

        l.text = "{\\an5\\pos(%f, %f)\\t(0, %f,\\fscy125\\1c%s)\\t(%f, %f,\\fscy100\\1c%s)}%s" % (
            syl.center,
            syl.middle,
            syl.duration / 3,
            Convert.color_rgb_to_ass(random_color),
            syl.duration / 3,
            syl.duration,
            line.styleref.color1,
            syl.text
        )

        io.write_line(l)

        # Main Effect 2 - Create random growing dots
        number_of_dots = 2

        FU = FrameUtility(line.start_time + syl.start_time,
                          line.start_time + syl.end_time)

        rand_dot_scale = random.uniform(80, 300)

        for dot_index in range(0, number_of_dots):
            offset_x1 = syl.center + random.randrange(-16, 16)
            offset_y1 = syl.middle + random.randrange(-20, 20)

            for s, e, i, n in FU:
                l.start_time = s
                l.end_time = e

                # Text scaling for reference
                fsc = 100
                fsc += FU.add(0, syl.duration / 3, 20)
                fsc += FU.add(syl.duration / 3, syl.duration, -20)

                dot_fsc = 100
                dot_fsc += FU.add(0, syl.duration, rand_dot_scale)

                # Starts at fully invisible => fully visible => invisible again``
                scale = 120
                dot_alpha = scale
                dot_alpha += FU.add(0, syl.duration / 3, -scale)
                dot_alpha += FU.add(syl.duration / 3, syl.duration, scale)
                dot_alpha = Convert.alpha_dec_to_ass(int(dot_alpha))

                l.text = (
                    "{\\an5\\pos(%.3f, %.3f)\\fscx%.3f\\fscy%.3f\\alpha%s\\1c%s\\bord3\\clip(%s)\\p1}%s"
                    % (
                        offset_x1,  # syl.center + rand,
                        offset_y1,  # syl.middle + rand,
                        dot_fsc,
                        dot_fsc,
                        dot_alpha,
                        Convert.color_rgb_to_ass(random_color),
                        Convert.text_to_clip(syl, an=5, fscx=fsc, fscy=fsc),
                        circle,
                    )
                )
                io.write_line(l)

        # Leadout
        off_x = 35
        off_y = 15

        l.start_time = line.start_time + syl.end_time
        l.end_time = line.end_time - 25 * \
            (len(line.syls) - syl.i) + delay
        l.duration = l.end_time - l.start_time

        l.text = "{\\an5\\move(%.3f, %.3f, %.3f, %.3f, %d, %d)\\fad(0, %d)}%s" % (
            syl.center,
            syl.middle,
            syl.center + math.cos(syl.i / 2) * off_x,
            syl.middle + math.sin(syl.i / 4) * off_y,
            l.duration - delay,
            l.duration,
            delay,
            syl.text
        )

        io.write_line(l)


def kanji(line: Line, l: Line):
    l.start_time = line.start_time - min(1000, line.leadin / 2)
    l.end_time = line.end_time + min(1000, line.leadout / 2)

    n = 2

    for i in range(n):
        l.text = "{\\fad(200, 200)\\pos(%.3f, %.3f)\\alpha%s}%s" % (
            l.center + 2*i,
            l.middle + 2*i,
            Convert.alpha_dec_to_ass(235),
            l.text
        )

        io.write_line(l)

    return


def sub(line, l):
    return


for line in lines:
    # Generating lines
    if line.style == "Romaji":
        romaji(line, line.copy())
    elif line.style == "Kanji":
        kanji(line, line.copy())
    else:
        sub(line, line.copy())

io.save()
io.open_mpv("gen.mp4", "00:52")
