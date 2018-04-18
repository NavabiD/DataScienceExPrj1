This is the directory where your source code would reside.

I am using a Dictionary (ipSessions) for storing records to be printed in the sessionization.txt file.
Python 3.6 is used for this implementation. In this version Dictionary maintains insertion order by default.
    Use of Dictionary allows constant time for lookups based on the key (ip). A lookup operation based on the key value is performed for each record processed.
Sessions are written to the sessionization.txt file and then removed from the ipSessions data structure when: 1) It is noticed that a session has become inactive 2) At the end of file. Operations of removing a session and writing to the file is performed once for each session.
    Checking to see is a session is active is a constant time operation. This operation is performed for each record processed.
    Removing an item from dictionary is order of N operation as the whole dictionary needs to be copied.
    Writing a session to the sessionization.txt file is a constant time operation.
Further experimentation, analysis and benchmarking is required to optimize time and space complexities.
Error Handeling is not complete and needs improvement.
