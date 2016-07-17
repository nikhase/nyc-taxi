import datetime as dt
from dateutil import parser

def price_estimation(timestamp, travelDistance, carTravelTime, bikeTravelTime):
    """
    Calculates estimations for the prices for the different possibilities
    :param timestamp: Timestamp for the trip
    :param travelDistance: Estimation of the distance to be travelled in Miles!!
    :param carTravelTime: Estimation of the time of travel in Minutes
    :return: Dictionary: Key = Type, Value = Price inf USD
    """
    prices = {}

    timestamp = parser.parse(timestamp)
    uber_estimation(prices, travelTime=carTravelTime, travelDistance=travelDistance)
    cab_estimation(prices, timestamp=timestamp, travelTime=carTravelTime, travelDistance=travelDistance)
    bike_estimation(prices, travelTime=bikeTravelTime)

    return prices


def uber_estimation(prices, travelTime, travelDistance):
    """
    Estimation of the prices for different Uber Types
    :param prices: dictionary to added the prices to
    :param travelTime: Estimation of the travel time in Minutes
    :param travelDistance: Estimation of the travel distance Miles

    Based on http://uberestimate.com/prices/New-York-City/
    """
    baseFare = (2.55 , 3.85 , 7, 14)
    timeFare = (0.35 , 0.5 , 0.65, 0.8)
    distFare = (1.75 , 2.85, 3.75, 4.5)
    minimumFare = (8, 10.5, 15, 25)
    uberX = baseFare[0] + timeFare[0] * travelTime + distFare[0] * travelDistance
    uberXL = baseFare[1] + timeFare[1] * travelTime + distFare[1] * travelDistance
    uberBlack = baseFare[2] + timeFare[2] * travelTime + distFare[2] * travelDistance
    uberSUV = baseFare[3] + timeFare[3] * travelTime + distFare[3] * travelDistance

    prices['uberX'] = str(int(max(uberX, minimumFare[0])))
    prices['uberXL'] = str(int(max(uberXL, minimumFare[1])))
    prices['uberBlack'] = str(int(max(uberBlack, minimumFare[2])))
    prices['uberSUV'] = str(int(max(uberSUV, minimumFare[3])))



def cab_estimation(prices, timestamp, travelTime, travelDistance):
    """
    Calculates the estimated cost of a yellow cab trip
    :param prices: dictionary to added the prices to
    :param timestamp: timestamp
    :param travelTime: Estimation of the travel time in Minutes
    :param travelDistance: Estimation of the travel distance Miles

    Based on http://www.nyc.gov/html/tlc/html/passenger/taxicab_rate.shtml
    """

    baseFare = 2.5 + 0.5  # 0.5 State Tax

    # Nightfare
    if timestamp.hour >= 20 or timestamp.hour < 6:
        baseFare += 0.5

    # Rushhour 4 pm to 8 pm only on weekdays
    if timestamp in range(16,20) and timestamp.weekday() > 4:
        baseFare += 1

    # Slow Traffic Exception
    travelTimeInH = float(travelTime /60.0)

    if travelTimeInH == 0:
        prices['yellow_cab'] = str(int(0))
        return

    avgSpeed = float( travelDistance / travelTimeInH)  #mph
    if avgSpeed <= 6: # Slower than 6 mp/h
        fare = baseFare + travelTime * 0.5
    else:
        distFare = 2.5  # 0.5$ per 1/5 Mile
        fare = baseFare + distFare * travelDistance

    prices['yellow_cab'] = str(int(fare))


def bike_estimation(prices, travelTime):
    '''

    :return:
    The annual membership is $14.95/mo with annual commitment (or $155/year if you pay in full).
    It includes unlimited 45-minute rides.
    Rides longer than 45 minutes incur extra fees: $2.50 for the first additional 30 minutes,
    $6.50 for the next additional 30 minutes,
    then $9 for each additional 30 minutes after that.
    '''

    #Shorter than 45 minutes
    if travelTime <= 45:
        prices['citibike'] = int(0)

    elif travelTime in range(45, 75):
        prices['citibike'] = 2.5

    elif travelTime in range(75, 105):
        prices['citibike'] = 2.5 + 6.5
    elif travelTime > 105:
        price = 2.5 + 6.5
        t = int(travelTime - 105 / 30)
        price += t*9
        prices['citibike'] = price


