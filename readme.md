# What is in this repository?

A simple command based chatbot developed for institutional queries. User suggestions can also be added into the database.

# Steps to run the program :

1. Install python (latest version preferred)

2. Open _command prompt_. Type ```pip install python-aiml``` and press enter to install aiml modules for python. Your device should be connected to internet.

3. Type ```python -m pip install cx_Oracle --upgrade pip```.

4. Then download the file available [here]("https://download.oracle.com/otn_software/nt/instantclient/19600/instantclient-basic-windows.x64-19.6.0.0.0dbru.zip"). Extract it to "C:/oracle"

5. In system environment variables find out the "PATH" variable. Then add "C:/oracle/instantclient" path to it. Make sure you add it on the top.

6. Extract these files to one folder.

7. Copy all the sql commands and programs written in _sqlFile.txt_ and paste them to oraclexe. It will create all the required tables, procedures and functions.

8. Open _command prompt_ in that folder. Type ```python chatbot.py``` and press enter to run the bot.

9. While the programm is running, type "save" and press enter to save the changes in _zerone.aiml_ file.

10. While the programm is running, type "load aiml bot" and press enter to load the changes saved.

11. To make the bot learn, type "learn" and press enter.

12. To end learning process, type "end" and press enter.

13. To terminate the program, type "bye" and press enter.

14. Set a strong _password_.

15. Remember your _userid_. Because it is randomly generated. You can't change it.

# Report
Report can be found [here](./chatbotreport.pdf)
