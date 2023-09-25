################################################################################################################################################################
# Notes:
# 
# Highlight table name or whatever -> right click -> Change all occurences
# Change all the repeated code into functions !!!
################################################################################################################################################################

# Header of the file 

import datetime
import os

# Change the current directory to the directory containing the sqlite3.h file.                                       Note: Database location
os.chdir('/Users/aaronberkness/Documents/Finances/Finances/FINANCE_DATABASE_FILES')

# Import the sqlite3.h file.
import sqlite3 
# Create a connection to the SQLite database.
con = sqlite3.connect("FINANCE_TABLE.db")
# Create a cursor object.
cur = con.cursor()

print("\n")

################################################################################

# Global Variables
# ---------------- 

# Total Spending

cur.execute("SELECT SUM(cost) FROM Spending")
total_spending = cur.fetchone()[0]
total_spending = round(total_spending, 2)

cur.execute("SELECT SUM(Amount) FROM Earnings")
total_earnings = cur.fetchone()[0]
total_earnings = round(total_earnings, 2)

total_left = total_earnings - total_spending
total_left = round(total_left, 2)

spending_columns = ["id", "Category", "Card", "Date", "Cost", "Notes"]
earning_columns = ["id", "Origin", "Amount", "Date"]

################################################################################################################################################################

# Functions

def chooseSpendingCategory():

    print("h: Housing        |  d: Dining        | f: Fun          ")
    print("u: Utilities      |  g: Groceries     | l: Learning     ")
    print("-" * 61)  # --------------------horizontal line-------------------

    letter = input("Which category do you want to choose? ")
    if letter == 'h':
        category = "Housing"
    elif letter == 'd':
        category = "Dining"
    elif letter == 'f':
        category = "Fun"
    elif letter == 'u':
        category = "Utilities"
    elif letter == 'g':
        category = "Groceries"
    elif letter == 'l':
        category = "Learning"
    else: 
        print("Invalid input")
    
    return category

#########################################################################################

def chooseCard():

    print("a: Apple Card     | f: 1387 Card       | c: Cash        ")
    print("-" * 61)  # --------------------horizontal line-------------------
    letter = input("Which card? ")
    
    if letter == 'a':
        card = "Apple Card"
    elif letter == 'f':
        card = "1387 Card"
    elif letter == 'c':
        card = "Cash"
    else: 
        print("Invalid input")
    
    return card

#########################################################################################

def chooseDate():

    print("Date format: xx/xx/xxxx")
    date = input("What was the date? ")
    if date == 'c':
        date = datetime.datetime.today()
        date = date.strftime("%m/%d/%Y")
    elif date == 's':
        day = input("What day this month? ")
        date = f"09/{day}/2023"

    return date

#########################################################################################

def chooseEarningCategory():
    print("p: Paycheck    | v: Venmo      | l: Student Loan     ")
    origin = input("What category do you want to choose? ")

    if origin == 'p':
        origin = "Paycheck"
    elif origin == 'v':
        origin = "Venmo"
    elif origin == 'l':
        origin = "Student Loan"

    return origin

#########################################################################################

def printColumnNames(table):
    if table == 's':
        print(f"{spending_columns[0]:<4} | {spending_columns[1]:<15} | {spending_columns[2]:<10} | {spending_columns[3]:<10} |  {spending_columns[4]:<8} | {spending_columns[5]}")
    elif table == 'e':
        print(f"{earning_columns[0]:<4} | {earning_columns[1]:<15} |  {earning_columns[2]:<8} | {earning_columns[3]:<10}")

#########################################################################################

def printLine(table):
    if table == 's':
        print("=" * 70)
    elif table == 'e':
        print("=" * 47) 

################################################################################################################################################################
table = input("What table do you want to use? ")
while table != 'q':

    choice = input("What is your choice? ")
    while choice != 'q':

        # Just a debugging move. Don't worry about this line +++++++++++++++++++++++
        cur.execute("SELECT SUM(cost) FROM Spending;")

        ############################################################################

        # Testing something ++++++++++++++++++++++++++++++++++++++++++++++++++++++++                                   if choice == 't'
        if choice == 't':
           category = chooseSpendingCategory()
           print(category)


        ############################################################################

        # Display the full table                                                                                       if choice == 'f'   !

        elif choice == 'f':
            print("\n")
            printColumnNames(table)
            printLine(table) #--------- horizontal line -----------
            if table == 's': # Spending Table
                for row in cur.execute("SELECT * FROM Spending ORDER BY date ASC"):
                    print(f"{row[0]:<4} | {row[1]:<15} | {row[2]:<10} | {row[3]:<10} | ${row[4]:>8} | {row[5]}")
                
                # Execute the SQL query to get the summed total from the cost column.
                cur.execute("SELECT SUM(cost) FROM Spending")

            elif table == 'e': # Earning Table
                for row in cur.execute("SELECT * FROM Earnings ORDER BY date ASC"):
                    print(f"{row[0]:<4} | {row[1]:<15} | ${row[2]:>8} | {row[3]:<10}")

                cur.execute("SELECT SUM(Amount) FROM Earnings")
                
        
        ############################################################################

        # Creating a table                                                                                              ** Reminder **
        # ------------------------------------------------- 
        # Can not create tables using python according
        # to the forums. Just use commands in the terminal.

        ############################################################################

        elif choice == 'd':      #                                                                                      if choice == 'd'     !
            letter = input("Do you want to delete the most recent entry? ")

            if table == 's':
                if letter == 'y':
                    cur.execute("DELETE FROM Spending WHERE id = (SELECT MAX(id) FROM Spending)")
                elif letter == 'n':
                    deletingRow = input("What row do you want to delete? ")
                    cur.execute("DELETE FROM Spending WHERE id = ?", (deletingRow,)) 

            elif table == 'e':
                if letter == 'y':
                    cur.execute("DELETE FROM Earnings WHERE id = (SELECT MAX(id) FROM Earnings)")
                elif letter == 'n':
                    deletingRow = input("What row do you want to delete? ")
                    cur.execute("DELETE FROM Earnings WHERE id = ?", (deletingRow,))

            else: 
                break
            
            deleteChoice = input("Are you sure you want to delete? ")
            if deleteChoice == 'y':
                con.commit()

            choice = input("What is your choice? ")

            continue

        ############################################################################

        # Searches for a specific category and displays it and then sums it up                                        if choice == 's'     !

        elif choice == 's':
            if table == 's':
                category = chooseSpendingCategory()
            elif table == 'e':
                category = chooseEarningCategory()

            print("\n")
            printLine(table) #--------- horizontal line -----------

            # Displaying table
            printColumnNames(table)
            printLine(table) #--------- horizontal line -----------
            for row in cur.execute("SELECT * FROM Spending WHERE category = ?", (category,)):
               print(f"{row[0]:<4} | {row[1]:<15} | {row[2]:<10} | {row[3]:<10} | ${row[4]:>8} | {row[5]}")

            # Execute the SQL query to get the summed total from the cost column.
            cur.execute("SELECT SUM(cost) FROM Spending WHERE category = ?", (category,))
        
        #############################################################################

        # Add a row                                                                                                      if choice == 'a'     !

        elif choice == 'a': 
            if table == 's':    # **** Spending *****
                category = chooseSpendingCategory()          
                print("\n")
                card = chooseCard()
                print("\n")  

                # Notes
                letter = input("Any notes?  ")
                if letter == 'y':
                    notes = input(">> ")
                else:
                    notes = "-"
            
            elif table == 'e':  # ***** Earning ******
                origin = chooseEarningCategory()
                print("\n")

            date = chooseDate()
            printLine(table) #--------- horizontal line -----------
            print("\n")

            amount = input("What was the amount? ")
            printLine(table) #--------- horizontal line -----------
            print("\n")

            if table == 's':
                cur.execute("INSERT INTO Spending (Category, Card, Date, Cost, Notes) VALUES (?, ?, ?, ?, ?)", (category, card, date, amount, notes))
            elif table == 'e':
                cur.execute("INSERT INTO Earnings (Origin, Amount, Date) VALUES (?, ?, ?)", (origin, amount, date,))

            con.commit()
            choice = input("What is your choice? ")
            continue


        #############################################################################

        else:
            printLine(table) #--------- horizontal line -----------
            print("invalid input")
            printLine(table) #--------- horizontal line -----------
            choice = input("What is your choice? ")
            continue

        ############################################################################################################################################################

        # Total Cost

        # Fetch the result of the query.
        total_cost = cur.fetchone()[0]
        total_cost = round(total_cost, 2)

        # Print the total cost column
        printLine(table)

        if table == 's':
            print(f"{str('Total'):<48} | ${total_cost:>8} |")
            printLine(table)
            print(f"{str('Account'):<48} | ${total_left:>8} |")

        elif table == 'e':
            print(f"{str('Total'):<22} | ${total_cost:>8}")
            printLine(table)
            print(f"{str('Account'):<22} | ${total_left:>8}")

        printLine(table)


        #############################################################################

        # End of the while loop question

        print("\n")
        choice = input("What is your choice? ")
    
    table = input("What table would you like to use? ")

#################################################################################################################################################################

# Close the cursor object.
cur.close()

# Close the connection to the SQLite database.
con.close()

