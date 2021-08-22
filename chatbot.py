# import the required modules
import aiml
import os
import cx_Oracle
import re
import random

# connecting to database
try:
    dbTNS = cx_Oracle.makedsn('192.168.43.168','1521',service_name='XE')
    connection = cx_Oracle.connect(user='prateekshyap',password='Soni19994$',dsn=dbTNS)
    cur = connection.cursor()

except cx_Oracle.DatabaseError as e:
    print("Error in Database: ",e)

# take the first user input
status = input("1- register\n2- login\nEnter a number - ")

while (status == "1" or status == "2"):

    # if the user wants to register
    if status == "1":

        try:

            un = input("Enter your name - ")
            umail = input ("Enter you email id - ")
            upw = input("Enter a password - ")

            # generate a suitable user id for the user
            i = len(un)
            flag = 0

            # extract the first index to userid variable
            uid = un[0].lower()
            j = 1

            # loop runs for the entire length of the name
            while (j != i):

                # if the character is a space
                if un[j].isspace():

                    # increment the flag to stop adding every character 
                    flag = flag + 1

                    # add the next character to the userid
                    uid = uid + un[j+1].lower()

                # if no space is encountered yet
                elif flag == 0:

                    # add all the characters one by one
                    uid = uid + un[j].lower()

                # increment the index
                j = j + 1

            # generate a 1/2/3 digit random number
            arr = random.sample(range(1,999),10)
            index = random.sample(range(0,9),1)[0]
            randomInt = arr[index]

            # concatenate the generated number to the userid
            uid = uid + str(randomInt)

            # prepare a query string to save the user details to the database
            queryString = "insert into usertable values ('"+un+"','"+uid+"','"+upw+"','"+umail+"')"

            # execute the query
            cur.execute(queryString)

            # commit 
            connection.commit()
            print("Registered Successfully! Your userid is- ",uid)

        except cx_Oracle.DatabaseError as e:
            print("Error in Database: ", e)

        # set status = 2 because the user will try to login after registration
        status = "2"

    # if the user wants to login
    elif status == "2":

        uid = input("Enter your userid - ")
        password = input("Enter your password - ")

        try:

            # prepare a query string to retrieve the saved password from the database
            queryString = "select password from usertable where userid = ('"+uid+"')"

            # refresh the cursor
            cur = connection.cursor();

            # execute the query
            cur.execute(queryString)

            # match whether the entered password and save password are same or not
            result = cur.var(cx_Oracle.STRING)
            cur.callfunc('matchpassword',result,[uid,password])

            # if both the passwords are same
            if result.getvalue()=="true":

                # refresh the cursor
                cur = connection.cursor()

                # save user id and current date and time for security purpose
                cur.callproc('savelogindetails',[uid])

                # commit
                connection.commit()

                #start the bot
                kernel = aiml.Kernel()
                if os.path.isfile("botBrain.brn"):
                    kernel.bootstrap(brainFile = "botBrain.brn")
                else:
                    kernel.bootstrap(learnFiles = "startup.xml", commands = "load aiml bot")
                    kernel.saveBrain("botBrain.brn")

                # kernel now ready for use
                while True:

                    # this variable stores the query put by the user
                    message = input(uid+" >> ")

                    # refresh the cursor
                    cur = connection.cursor()

                    # save the userid and query for security purpose
                    cur.callproc('savequerydetails',[uid,message])

                    # commit
                    connection.commit()

                    # if the user wants to save and reload tha bot
                    if message == "save":
                        kernel.saveBrain("botBrain.brn")

                    # if user wants to give some suggestions then turn into learn mode
                    elif message == "learn":

                        # stop the bot replies and take input from the user only
                        query = input (uid+" >> ")

                        # as long as the user doesn't want to end
                        while (query != "end"):

                            try:

                                # refresh the cursor
                                cur = connection.cursor()

                                # save the suggestions and user id
                                cur.callproc('savesuggestiondetails',[uid,query])

                                # commit
                                connection.commit();

                            except cs_Oracle.DatabaseError as e:
                                print("Error in Database: ", e)

                            # take input for the next query
                            query = input (uid+" >> ")

                        # when the user types end    
                        print("bot >> Thanks for teaching me! Go ahead.");

                    # in all other cases
                    else:

                        # save the bot response
                        botResponse = kernel.respond(message)

                        # if bot replies for "hello", "bye", "good bye"
                        if botResponse == "Hey! How can I help you?" or botResponse == "Hope to see you again! Have a good day! Bye!" or botResponse == "Okay, have a happy life ahead!":

                            # refresh the cursor
                            cur = connection.cursor()

                            # find out the user name of the user
                            name = cur.var(cx_Oracle.STRING)
                            cur.callfunc('findusername',name,[uid])

                            # extract the first name
                            printName = name.getvalue()[0]
                            i = len(name.getvalue())

                            flag = 0
                            j = 1

                            # run the loop, add characters till first spaee is encountered
                            while (j != i):
                                if name.getvalue()[j].isspace():
                                    flag = flag + 1
                                elif flag == 0:
                                    printName = printName + name.getvalue()[j]

                                #increment the index
                                j = j + 1

                            # if bot replies for "hello"
                            if botResponse == "Hey! How can I help you?":
                                print ("bot >> Hey, "+printName+"! How can I help you?")

                            # if bot replies for "bye"
                            elif botResponse == "Hope to see you again! Have a good day! Bye!":

                                # display message along with the user name
                                print ("bot >> Hope to see you again! Have a good day, "+printName+"! Bye!")

                                # refresh the cursor
                                cur = connection.cursor()

                                # save the user id and current date and time for security purpose
                                cur.callproc('savelogoutdetails',[uid])

                                # commit
                                connection.commit()

                                #terminate the program
                                exit()

                            # if bot replies for "good bye"
                            elif botResponse == "Okay, have a happy life ahead!":

                                # display farewell message with the user name
                                print ("bot >> Okay, "+printName+"! Have a happy life ahead!")

                                # refresh the cursor
                                cur = connection.cursor()

                                # save the user id and current date and time for security purpose
                                cur.callproc('savelogoutdetails',[uid])

                                # commit
                                connection.commit()

                                # terminate the program
                                exit()

                        # in all other cases
                        else:

                            # just print the response of the bot
                            print ("bot >> "+botResponse)

            # in all other cases
            else:
                print("Wrong userid or password!")

        except cx_Oracle.DatabaseError as e:
            print("Error in Database: ",e)

        # set status = -1 at the end to prevent looping and terminate the program successfully
        status = "-1"
        cur.close()
        connection.close()

    #    select userid,query,to_char(dt,'DD-MON-YYYY HH:MI:SS') from querieshistory;