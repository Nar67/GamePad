


class ColorMapper(object):
    beat_line_color = 64

    @staticmethod
    def getChannelColor(i):
        colors = [
            72,
            122,
            79,
            9,
            116,
            3,
            13,
            53,
        ]
        return colors[i]
