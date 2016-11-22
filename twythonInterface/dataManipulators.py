MONTHS = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6,
          'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}

def tweetDateToInt(dateString):
    """
    Convert twitters date string format to an easily comparable integer. As a base 10
    integer the date will be represented with the first 4 significant digits as the
    year. The next two are the month by the dictionary MONTHS, and the last two are
    the day. Since this is an integer, the dates can be easily compared with math
    operators.
    @param String dateString - Twitter's string representation of a date.
    @return int dateAsNum - The date encoded as an int.
    """

    #Indices of the date string entries after a split
    I_YEAR = 5
    I_MONTH = 1
    I_DAY = 2

    dateArr = dateString.split()

    dateAsNum = int(dateArr[I_YEAR]) * 10000
    m = dateArr[I_MONTH]
    dateAsNum = MONTHS[m] * 100 + dateAsNum
    dateAsNum = int(dateArr[I_DAY]) + dateAsNum

    return dateAsNum
