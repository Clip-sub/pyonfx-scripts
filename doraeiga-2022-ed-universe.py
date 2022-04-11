from pyonfx import *
import random

# https://pyonfx.readthedocs.io/en/latest/
io = Ass("D:\\Videos\\Doraeiga 2021\\Universe - Official HigeDANdism.ass")
io.path_output = "D:\\Videos\\Doraeiga 2021\\gen.ass"
meta, styles, lines = io.get_data()

# Creating the star and extracting all the color changes from the input file
star = Shape.star(5, 4, 10)

rand_radius = random.uniform(6, 17)
circle = Shape.ellipse(rand_radius, rand_radius)

COLOR_CRIMSON = "#301F1F"
COLOR_YELLOW = "#41430A"
COLOR_GREEN = "#03490E"
COLOR_BLUE = "#005989"
COLOR_DARK_BLUE = "#152B75"
COLOR_VIOLET = "#351575"
COLOR_DARK_PINK = "#570663"
COLOR_APPLE = "#8D0031"


def romaji(line: Line, l: Line):
    # Random color per line
    random_color = random.choice(
        [
            COLOR_CRIMSON,
            COLOR_YELLOW,
            COLOR_GREEN,
            COLOR_BLUE,
            COLOR_DARK_BLUE,
            COLOR_VIOLET,
            COLOR_DARK_PINK,
            COLOR_APPLE
        ]
    )

    for syl in Utils.all_non_empty(line.syls):

        # Leadin
        l.start_time = line.start_time - line.leadin / 2
        l.end_time = line.start_time + syl.start_time
        l.duration = l.end_time - l.start_time

        l.text = (
            "{\\an5\\pos(%.3f, %.3f)}%s"
        ) % (
            syl.center,
            syl.middle,
            syl.text
        )

        io.write_line(l)

        # Main Effect
        l.layer = 1
        FU = FrameUtility(line.start_time + syl.start_time,
                          line.start_time + syl.end_time)

        rand_dot_scale = random.uniform(80, 300)

        fsc = 120
        l.text = "{\\an5\\pos(%.3f, %.3f)\\fscy%.3f\\1c%s\\1a%s}%s" % (
            syl.center,
            syl.middle,
            fsc,
            Convert.color_rgb_to_ass(random_color),
            Convert.alpha_dec_to_ass(250),
            syl.text
        )

        io.write_line(l)

        # Create random growing dots
        number_of_dots = 2

        for di in range(0, number_of_dots):
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
        l.start_time = line.start_time + syl.end_time
        l.end_time = line.end_time + line.leadout / 2
        l.text = "{\\an5\\pos(%.3f, %.3f)}%s" % (
            syl.center,
            syl.middle,
            syl.text
        )

        io.write_line(l)


def kanji(line: Line, l: Line):
    l.text = ""
    return


def sub(line, l):
    return


for line in lines:
    # Generating lines
    if line.style == "Romaji":
        romaji(line, line.copy())
    elif line.styleref.alignment >= 4:
        kanji(line, line.copy())
    else:
        sub(line, line.copy())

io.save()
io.open_mpv("D:\\Videos\\Doraeiga 2021\\gen.mp4", "00:52")
