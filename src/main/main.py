import csv
import sqlite3

# Connect to the SQLite in-memory database
conn = sqlite3.connect(':memory:')

# A cursor object to execute SQL commands
cursor = conn.cursor()


def main():

    # users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        userId INTEGER PRIMARY KEY,
                        firstName TEXT,
                        lastName TEXT
                      )'''
                   )

    # callLogs table (with FK to users table)
    cursor.execute('''CREATE TABLE IF NOT EXISTS callLogs (
        callId INTEGER PRIMARY KEY,
        phoneNumber TEXT,
        startTime INTEGER,
        endTime INTEGER,
        direction TEXT,
        userId INTEGER,
        FOREIGN KEY (userId) REFERENCES users(userId)
    )''')

    # You will implement these methods below. They just print TO-DO messages for now.
    load_and_clean_users('../../resources/users.csv')
    load_and_clean_call_logs('../../resources/callLogs.csv')
    write_user_analytics('../../resources/userAnalytics.csv')
    write_ordered_calls('../../resources/orderedCalls.csv')

    # Helper method that prints the contents of the users and callLogs tables. Uncomment to see data.
    # select_from_users_and_call_logs()

    # Close the cursor and connection. main function ends here.
    cursor.close()
    conn.close()


# TODO: Implement the following 4 functions. The functions must pass the unit tests to complete the project.


# This function will load the users.csv file into the users table, discarding any records with incomplete data
def load_and_clean_users(file_path):
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  

        for row in reader:
            if len(row) == 2:
                firstName, lastName = row

                if firstName.strip() and lastName.strip():
                    cursor.execute('''
                        INSERT INTO users (firstName, lastName) 
                        VALUES (?, ?)
                    ''', (firstName.strip(), lastName.strip()))
                     
    
    #print("TODO: load_users")


# This function will load the callLogs.csv file into the callLogs table, discarding any records with incomplete data
def load_and_clean_call_logs(file_path):

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        for row in reader:

            # Ensure the row has exactly 5 columns
            if len(row) == 5:
                phoneNumber, startTime, endTime, Direction, userId = row

                # Check if all required fields are present and non-empty
                if all(field.strip() for field in [phoneNumber, startTime, endTime, Direction, userId]):
                    try:
                        startTimeEpoch = int(startTime.strip())
                        endTimeEpoch = int(endTime.strip())
                        userId = int(userId.strip())
                    except ValueError:
                        continue

                    # Insert the valid row into the database
                    cursor.execute('''
                        INSERT INTO callLogs (phoneNumber, startTime, endTime, Direction, userId)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (phoneNumber.strip(), startTime, endTime, Direction.strip(), userId))

    #print("TODO: load_call_logs")


# This function will write analytics data to testUserAnalytics.csv - average call time, and number of calls per user.
# You must save records consisting of each userId, avgDuration, and numCalls
# example: 1,105.0,4 - where 1 is the userId, 105.0 is the avgDuration, and 4 is the numCalls.
def write_user_analytics(csv_file_path):

    query = '''
        SELECT
            userId,
            AVG(endTime - startTime) AS avgDuration,
            COUNT(*) AS numCalls
        FROM
            callLogs
        GROUP BY
            userId
    '''
    
    cursor.execute(query)
    results = cursor.fetchall()

    # Write results to CSV file
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(['userId', 'avgDuration', 'numCalls'])
        
        # Write data rows
        for row in results:
            userId, avgDuration, numCalls = row
            writer.writerow([userId, f"{avgDuration:.1f}", numCalls])

    print("TODO: write_user_analytics")


# This function will write the callLogs ordered by userId, then start time.
# Then, write the ordered callLogs to orderedCalls.csv
def write_ordered_calls(csv_file_path):

    query = '''
        SELECT
            callId,
            phoneNumber,
            startTime,
            endTime,
            direction,
            userId
        FROM
            callLogs
        ORDER BY
            userId,
            startTime
    '''
    
    # Execute the query and fetch all results
    cursor.execute(query)
    results = cursor.fetchall()

    # Open the CSV file for writing
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(['callId', 'phoneNumber', 'startTime', 'endTime', 'direction', 'userId'])
        
        # Write each result row
        for row in results:
            writer.writerow(row)

    #print("TODO: write_ordered_calls")



# No need to touch the functions below!------------------------------------------

# This function is for debugs/validation - uncomment the function invocation in main() to see the data in the database.
def select_from_users_and_call_logs():

    print()
    print("PRINTING DATA FROM USERS")
    print("-------------------------")

    # Select and print users data
    cursor.execute('''SELECT * FROM users''')
    for row in cursor:
        print(row)

    # new line
    print()
    print("PRINTING DATA FROM CALLLOGS")
    print("-------------------------")

    # Select and print callLogs data
    cursor.execute('''SELECT * FROM callLogs''')
    for row in cursor:
        print(row)


def return_cursor():
    return cursor


if __name__ == '__main__':
    main()
