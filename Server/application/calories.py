
def calories(distanceMiles, traveltimeMins):
    '''
    Returns the estimated calories
    :param distance: distance
    :param time:
    :return: dictionary containing the calories
    '''
    cal = {}
    cal['bike'] = biking_calories(distanceMiles, traveltimeMins)
    cal['walking'] = walking_calories(distanceMiles)

    return cal

def walking_calories(distanceMiles):
    '''
    Calories burnt for walking.
    Based on: http://caloriesburnedhq.com/calories-burned-walking/
    :param distanceMiles:
    :return: Calories
    '''
    # 250 Calories per Mile at 3 mph
    calPerMile = 250.0 / 3.0
    cal = distanceMiles * calPerMile

    return int(cal)

def biking_calories(distanceMiles, traveltimeMins):
    '''
    Calories burnt for biking.
    Based on: http://caloriesburnedhq.com/calories-burned-biking/
    :param distanceMiles:
    :param traveltimeMins:
    :return: Calories
    '''
    h = traveltimeMins / 60.0
    speed = distanceMiles / h

    # 150lb person: 14 mph ==> 48 Calories per Mile --> 3.43 Calories per Mile and mph
    cal = speed * 3.43 * distanceMiles

    return int(cal)


