from datetime import time
import re

def match_hours(hours: str):
    # This pattern tests for list of ints between 0 and 23 separated by a comma.
    pattern = r'^(\d|1\d|2[0-3])(, ?(\d|1\d|2[0-3]))*$'
    return re.match(pattern, hours)

def convert_binary(hours: list):
    """ Creates a binary representation of a list of hours. """
    o = ['1' if str(i) in hours else '0' for i in range(24)][::-1]
    return int(''.join(o), 2)

def convert_time(number):
    """ Creates a list of hours from its binary representation. """
    binary = bin(number)[2:][::-1] # Strips the '0b' at the begining
    return [str(i) for (i, v) in enumerate(binary) if int(v)]


def generate_chart(medications):
    hours = {
        int(hour)
        for med in medications
        for hour in convert_time(med.given_hours)
    }

    for h in hours:
        meds = [med for med in medications if str(h) in convert_time(med.given_hours)]
        yield ','.join([time(hour=h).strftime("%I%p"), meds[0].name]) + '\n'
        # if there is more than one drug for this hour.
        for i in range(1, len(meds)):
            yield ','.join(["", meds[i].name]) + '\n'