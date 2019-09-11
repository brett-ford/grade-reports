## Automated Grade Reports 

This project automates the process of communicating my students' grades to them. I maintain three Google Sheets files, 
one for each course I teach, to store grades. Since it's important for students to be able to monitor their performance, 
regular grade updates are helpful but time consuming. Previously, students needed to ask for their grades, either in,
either in person or via email. 

This project allows me to send grade updates to all students by running one script. The app consists of two processes.
The setup process reads my grade books through the Google Sheets API and creates, shares, and inserts headers for each 
student listed in the grade book. The update process reads my grade books and inserts a new line in each student's sheet. 
The update includes the student's current grade in addition to all significant milestone grades such as quarter and
semester grades.