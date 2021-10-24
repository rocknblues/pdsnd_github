import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    city, month, day = "","",""

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Enter a city from the following list: chicago, new york city, washington\n').lower()


    # get user input for month (all, january, february, ... , june)
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Enter a month from the following list: january, february, march, april, may, june, all(use all for all months)\n').lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Enter a day of the week from the following list: monday, tuesday, wednesday, thursday, friday, saturday, sunday, all(use all for all days)\n').lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # I am using a newer verion of Pandas, hence day_name() instead of
    # weekday_name()
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.capitalize()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = ['january', 'february', 'march', 'april', 'may', 'june'][df['month'].mode()[0]-1]
    print('The most common month is {}'.format(most_common_month.capitalize()))


    # display the most common day of week
    most_common_day = df['day'].mode()[0]
    print('The most common day of week is {}'.format(most_common_day))


    # display the most common start hour
    # most_common_hour = df['hour'].mode()[0]
    print('The most common start hour is {}'.format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}'.format(most_common_start_station))


    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commong end station is {}'.format(most_common_end_station))


    # display most frequent combination of start station and end station trip
    most_common_combination_station = (df['Start Station'] + ' --> ' + df['End Station']).mode()[0]
    print('The most frequent combination of start station and end station trip is {}'.format(most_common_combination_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = (df['End Time'] - df['Start Time']).sum()
    print('Total travel time is {}\n'.format(total_travel_time))


    # display mean travel time
    mean_travel_time = (df['End Time'] - df['Start Time']).mean()
    print('Mean travel time is {}'.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('Counts of user types are\n{}\n'.format(user_type_count))


    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('Counts of user types are\n{}'.format(gender_count))
    except KeyError:
        print('Washington did not track gender')


    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('The earliest birth year is {}\nThe most recent birth year is {}\nThe most common birth year is {}'.format(earliest_birth_year, recent_birth_year, common_birth_year))
    except KeyError:
        print('Washington did not track birth year')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Provides option to display raw data."""

    for i in range(0, len(df)-5, 5):
        choice = input('\nWould you like to display 5 rows of raw data? Enter yes or no.\n')
        if choice.lower() != 'yes':
            break

        print(df[i : i+5])


def test_all_combinations():
    """Tests all possible combinations of each filter."""

    print('Starting test run...\n')
    start_time = time.time()

    # define list of cities, months, days
    cities = ['chicago', 'new york city', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # loop through list of each filter combination
    for city in cities:
        for month in months:
            for day in days:
                df = load_data(city, month, day)
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)

    print('\nCongratulations, all combinations succesfully ran. This took {} seconds.\n'.format(time.time() - start_time))
    print('-'*40)


def main():

    # function to test all possible filter combinations
    test = input('Would you like to run all combinations prior to selecting filter criteria. Depending on how fast your computer is, you may want to grab a coffee. Enter yes or no.\n')
    if test.lower() == 'yes':
        test_all_combinations()

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
