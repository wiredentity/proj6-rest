"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    speeds = [
        (0, 200, 34),
        (200, 400, 32),
        (400, 600, 30),
        (600, 1000, 28),
        (1000, 1300, 26)
    ]

   #Handles control beyond brevet distance edge cases
    distance = min(control_dist_km, brevet_dist_km)

    time = 0

    for start_distance, end_distance, speed in speeds:

      # Handles edge cases
        if distance <= start_distance:
            break

        segment_distance = min(distance, end_distance) - start_distance

        time += segment_distance / speed

    total_minutes = round(time * 60)

    start = arrow.get(brevet_start_time)
    result = start.shift(minutes=total_minutes)

    return result.isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    speeds = [
        (0, 200, 15),
        (200, 400, 15),
        (400, 600, 15),
        (600, 1000, 11.428),
        (1000, 1300, 13.333)
    ]

    distance = min(control_dist_km, brevet_dist_km)

    # Special closing time for the start control
    if distance == 0:
        total_minutes = 60

    # Controls below 60 km
    elif distance < 60:
        total_minutes = round((distance / 20 + 1) * 60)

    # Official brevet finish times
    elif distance == brevet_dist_km:
        finish_times = {
            200: 13.5,
            300: 20,
            400: 27,
            600: 40,
            1000: 75
        }

        total_minutes = round(finish_times[brevet_dist_km] * 60)

    else:
        total_time = 0

        for start_distance, end_distance, speed in speeds:

            if distance <= start_distance:
                break

            segment_distance = min(distance, end_distance) - start_distance

            total_time += segment_distance / speed

        total_minutes = round(total_time * 60)

    start = arrow.get(brevet_start_time)
    result = start.shift(minutes=total_minutes)

    return result.isoformat()