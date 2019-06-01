class NegativeIntConverter:
    # a matcher to accept negative values in url
    # ref: https://stackoverflow.com/a/48868140
    regex = '-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%d' % value
