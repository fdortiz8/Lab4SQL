#! /usr/bin/env python

#  runElectionsApplication Solution

import psycopg2, sys, datetime

# usage()
# Print error messages to stderr
def usage():
    print("Usage:  python3 runElectionsApplication.py userid pwd", file=sys.stderr)
    sys.exit(-1)
# end usage

# The three Python functions that for Lab4 should appear below.
# Write those functions, as described in Lab4 Section 4 (and Section 5,
# which describes the Stored Function used by the third Python function).
#
# Write the tests of those function in main, as described in Section 6
# of Lab4.


 # printNumPartyCandidatesAndOfficeHolders (myConn, theParty):
 # party is an attribute in the CandidatesForOffice table, indicating the candidate for office’s
 # party in an election.  A candidate for office in an election runs in a particular party.
 # Every office holder must be a candidate for office (referential integrity), but some
 # candidates for office are office holders and some are not.  Any office holder was in a
 # particular party in the election in which they were candidates for office.
 #
 # The arguments for the printNumPartyCandidatesAndOfficeHolders Python function are the database
 # connection and a string argument, theParty, which is a party.  This Python function prints
 # out the number of candidates for office and the number of offfice holders who were in myParty
 # when they ran as candidates for office in an election.
 #
 # For more details, including error handling and return codes, see the Lab4 pdf.
def candidatesFromParty(myConn, theParty, query):
    try:
        cursor = myConn.cursor()
        cursor.execute(query, (theParty,))
    except:
        print("Statement", query, "is bad", file=sys.stderr)
        cursor.close()
        myConn.close()
        sys.exit(-1)
    row = cursor.fetchone()
    
    cursor.close()
    return row[0]

def officeHoldersFromParty(myConn, theParty, query):
    try:
        cursor = myConn.cursor()
        cursor.execute(query,(theParty,))
    except:
        print("Statement", query, "is bad", file=sys.stderr)
        cursor.close()
        myConn.close()
        sys.exit(-1)
    row = cursor.fetchone()
    #print("Number of office holders from party", theParty, "is", row[0])
    cursor.close()
    return row[0]

def printNumPartyCandidatesAndOfficeHolders (myConn, theParty):
    if (theParty == ''):
        return -1;
    
    numPartyMembers_query = "SELECT COUNT(party) FROM CandidatesForOffice WHERE party = (%s)"
    candidatesAndOfficeHolders_query = "SELECT COUNT(candidateID) FROM CandidatesForOffice WHERE party = (%s) AND candidateID IN (SELECT candidateID FROM OfficeHolders)"
    
    numPartyMembers = officeHoldersFromParty(myConn, theParty, numPartyMembers_query)
    numOfficeHolders = officeHoldersFromParty(myConn, theParty, candidatesAndOfficeHolders_query)
    
    print("Number of candidates from party", theParty, "is", numPartyMembers)
    print("Number of office holders from party", theParty, "is", numOfficeHolders)
    # Python function to be supplied by students

# end printNumPartyCandidatesAndOfficeHolders


# increaseLowSalaries (myConn, theSalaryIncrease, theLimitValue):
# salary is an attribute of the ElectedOffices table.  We’re going to increase the salary by a
# certain amount (theSalaryIncrease) for all the elected offices who salary value is less than
# or equal some salary limit (theLimitValue).'
#
# Besides the database connection, the increaseLowSalaries Python function has two arguments,
# a float argument theSalaryIncrease and another float argument, theLimitValue.  For every
# elected office in the ElectedOffices table (if any) whose salary is less than or equal to
# theLimitValue, increaseLowSalaries should increase that salary value by theSalaryIncrease.
#
# For more details, including error handling, see the Lab4 pdf.

def increaseLowSalaries (myConn, theSalaryIncrease, theLimitValue):
    if (theSalaryIncrease <= 0.00):
        return -1;
    if (theLimitValue <= 0.00):
        return -2;
    query = "UPDATE ElectedOffices SET salary = salary + (%s) WHERE salary <= (%s)"
    try:
        cursor = myConn.cursor()
        cursor.execute(query, (theSalaryIncrease, theLimitValue))
        count = cursor.rowcount
    except:
        print("Statement", query, "is bad", file=sys.stderr)
        cursor.close()
        myConn.close()
        sys.exit(-1)
    cursor.close()
    print("Number of elected offices whose salaries under", theLimitValue, "were updated by", theSalaryIncrease, "is", count)
    return count
    #print("Printing all ElectedOffices salary with <=", theLimitValue)
    #for row in records:
        #print("|officeId:", row[0], "officeName:", row[1],"|city:", row[2],"|state:", row[3],"|salary:", row[4], "|")
        
    # Python function to be supplied by students
    # You'll need to figure out value to return.

# end increaseLowSalaries


# improveSomeRatings (myConn, theParty, maxRatingImprovements):
# Besides the database connection, this Python function has two other parameters, theParty which
# is a string, and maxRatingImprovements which is an integer.
#
# improveSomeRatings invokes a Stored Function, improveSomeRatingsFunction, that you will need to
# implement and store in the database according to the description in Section 5.  The Stored
# Function improveSomeRatingsFunction has all the same parameters as improveSomeRatings (except
# for the database connection, which is not a parameter for the Stored Function), and it returns
# an integer.
#
# Section 5 of the Lab4 tells you which ratings to improve and how to improve them, and explains
# the integer value that improveSomeRatingsFunction returns.  The improveSomeRatings Python
# function returns the same integer value that the improveSomeRatingsFunction Stored Function
# returns.
#
# improveSomeRatingsFunction doesn’t print anything.  The improveSomeRatings function must only
# invoke the Stored Function improveSomeRatingsFunction, which does all of the work for this part
# of the assignment; improveSomeRatings should not do any of the work itself.
#
# For more details, see the Lab4 pdf.

def improveSomeRatings (myConn, theParty, maxRatingImprovements):
    
# We're giving you the code for improveSomeRatings, but you'll have to write the
# Stored Function improveSomeRatingsFunction yourselves in a PL/pgSQL file named
# improveSomeRatingsFunction.pgsql
    try:
        myCursor = myConn.cursor()
        sql = "SELECT improveSomeRatingsFunction(%s, %s)"
        myCursor.execute(sql, (theParty, maxRatingImprovements))
    except:
        print("Call of improveSomeRatingsFunction with arguments", theParty, maxRatingImprovements, "had error", file=sys.stderr)
        myCursor.close()
        myConn.close()
        sys.exit(-1)
    
    row = myCursor.fetchone()
    myCursor.close()
    print("Number of ratings which improved for party", theParty, "for maxRatingImprovements value", maxRatingImprovements, "is", row[0])
    return(row[0])


#end improveSomeRatings

def main():

    if len(sys.argv)!=3:
       usage()

    hostname = "cse182-db.lt.ucsc.edu"
    userID = sys.argv[1]
    pwd = sys.argv[2]
    

    # Try to make a connection to the database
    try:
        myConn = psycopg2.connect(host=hostname, user=userID, password=pwd)
        test1_query1 = 'Silver'
        test2_query1 = 'Copper'
        printNumPartyCandidatesAndOfficeHolders(myConn, test1_query1)
        print("\n")
        printNumPartyCandidatesAndOfficeHolders(myConn, test2_query1)
        print("\n")
        
        test1_query2_salaryIncrease = 60000
        test1_query2_limitValue = 125000
        test2_query2_salaryIncrease = 4000
        test2_query2_limitValue = 131000
        increaseLowSalaries(myConn,test1_query2_salaryIncrease, test1_query2_limitValue)
        print("\n")
        increaseLowSalaries(myConn,test2_query2_salaryIncrease, test2_query2_limitValue)
        print("\n")
        
        test1_query3_party = "Copper"
        test1_query3_maxRatingImprovements = 6
        test2_query3_party = "Gold"
        test2_query3_maxRatingImprovements = 1
        test3_query3_party = "Silver"
        test3_query3_maxRatingImprovements = 1
        test4_query3_party = "Platinum"
        test4_query3_maxRatingImprovements = 0
        test5_query3_party = "Copper"
        test5_query3_maxRatingImprovements = 6
        
        improveSomeRatings(myConn, test1_query3_party, test1_query3_maxRatingImprovements)
        print("\n")
        improveSomeRatings(myConn, test2_query3_party, test2_query3_maxRatingImprovements)
        print("\n")
        improveSomeRatings(myConn, test3_query3_party, test3_query3_maxRatingImprovements)
        print("\n")
        improveSomeRatings(myConn, test4_query3_party, test4_query3_maxRatingImprovements)
        print("\n")
        improveSomeRatings(myConn, test5_query3_party, test5_query3_maxRatingImprovements)
        print("\n")
        
    except:
        print("Connection to database failed", file=sys.stderr)
        sys.exit(-1)
        
    # We're making every SQL statement a transaction that commits.
    # Don't need to explicitly begin a transaction.
    # Could have multiple statement in a transaction, using myConn.commit when we want to commit.
    
    myConn.autocommit = True
    
    # There are other correct ways of writing all of these calls correctly in Python.
        
    # Perform tests of printNumPartyCandidatesAndOfficeHolders, as described in Section 6 of
    # Lab4.  That Python function handles printing when there is no error.
    # Print error outputs here. You may use a Python method to help you do the printing.


    # Perform tests of increaseLowSalaries, as described in Section 6 of Lab4.
    # Print their outputs (including error outputs) here, not in increaseLowSalaries.
    # You may use a Python method to help you do the printing.
 
 
    # Perform tests of improveSomeRatings, as described in Section 6 of Lab4,
    # Print their outputs (including error outputs) here, not in improveSomeRatings.
    # You may use a Python method to help you do the printing.
  
  
    myConn.close()
    sys.exit(0)
#end

#------------------------------------------------------------------------------
if __name__=='__main__':

    main()

# end
