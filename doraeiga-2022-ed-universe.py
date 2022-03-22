from pyonfx import *
import random

io = Ass("D:\\Videos\\Doraeiga 2021\\Universe - Official HigeDANdism.ass")
io.path_output = "D:\\Videos\\Doraeiga 2021\\gen.ass"
meta, styles, lines = io.get_data()

# Creating the star and extracting all the color changes from the input file
star = Shape.star(5, 4, 10)

rand_radius = random.uniform(6, 17)
circle = Shape.ellipse(rand_radius, rand_radius)


def romaji(line: Line, l: Line):
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
        rand = random.uniform(-10, 10)

        for s, e, i, n in FU:
            l.start_time = s
            l.end_time = e

            fsc = 100
            fsc += FU.add(0, syl.duration / 3, 20)
            fsc += FU.add(syl.duration / 3, syl.duration, -20)

            random_initial_shape_size = random.uniform(80, 140)

            # fsc_shape =

            l.text = "{\\an5\\pos(%.3f, %.3f)\\fscy%.3f}%s" % (
                syl.center,
                syl.middle,
                fsc,
                syl.text
            )

            io.write_line(l)

            # Move the circle inside
            l.text = (
                "{\\an5\\pos(%.3f, %.3f)\\fscx%.3f\\fscy%.3f\\\\1c&H0000FF&\\bord3\\clip(%s)\\p1}%s"
                % (
                    syl.center + rand,
                    syl.middle + rand,
                    fsc,
                    fsc,
                    Convert.text_to_clip(syl, an=5),
                    circle,
                )
            )
            io.write_line(l)

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
