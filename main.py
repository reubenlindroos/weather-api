import argparse
import json

import numpy as np

import api_calls

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--url",
                        required=False,
                        default="http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/",
                        help="url to fetch the json data from")
    parser.add_argument("-n", "--candidate_nr",
                        required=True,
                        help="Candidate number from which to select the data")
    parser.add_argument("-o", "--output_file",
                        required=True,
                        help="path/to/outputfile.json to store results")
    args = parser.parse_args()
    handler = api_calls.APIHandler(args.candidate_nr, args.url)
    answers = {}

    # 1. What will the temperature be in Bath at 10am on
    # Wednesday morning? int
    answer = handler.get_val("bath", "temperature", "wednesday", 9)
    answers["1"] = answer[0]

    # 2. Does the pressure fall below 1000 millibars in Edinburgh at
    # any time on Friday? boolean
    answer = False
    edinburgh_pressure = handler.get_val("edinburgh", "pressure",
                                         "friday")
    for press in edinburgh_pressure:
        if press < 1000:
            answer = True
            break
    answers["2"] = answer

    # 3. What is the median temperature during the week for Cardiff? int
    cardiff_temp = handler.get_val("cardiff", "temperature")
    answers["3"] = np.median(cardiff_temp)

    # 4. In which city is the highest wind speed recorded this week?
    # If there is more than one city shares the maximum speed,
    # choose the one which is first alphabetically. string
    fmax = 0
    fcity = ''
    for city in handler.get_cities():
        windspeed = handler.get_val(city, "wind_speed")
        if np.max(windspeed) == fmax:
            lst = [city, fcity]
            lst.sort()
            fcity = lst[0]

        if np.max(windspeed) > fmax:
            fmax = np.max(windspeed)
            fcity = city

    answers["4"] = fcity

    # 5. It is likely to snow if there is precipitation when the
    # temperature is below 2 degrees. Will it snow in any of the
    # cities this week? Boolean
    answer = False
    for city in handler.get_cities():
        temp = handler.get_val(city, "temperature")
        precipitation = handler.get_val(city, "precipitation")
        for val, enum in enumerate(temp):
            if precipitation[enum] and val < 2:
                answer = True

    answers["5"] = answer

    with open(args.output_file, "w") as ofile:
        ofile.write(json.dumps(answers))
