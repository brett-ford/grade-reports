## Automated Grade Reports 

This project automates the process of communicating with students about their grades.

I use Google Sheets to record grades. one file per course. It's important for students to receive regular feedback, both qualitative and quantitative. Exchanging feedback is time consuming and prone to miscommunication. To solve this problem, I developed this project so that each student would have their own grade record accessible on their Google Drive account. 

The app consists of two processes.

1) The setup process is run at the benning of a school year to create the necessary files for each student. It reads students' names and other pertinent information from my grade books via the Google Sheets API. It then creates a Google Sheet with the necessary headers for each student and shares the sheet with the student's school Google Drive account. It also shares the sheet with the student's advisor. 

2) When run, the update process reads my grade books and inserts a new line in each student's sheet. The update includes the student's current grade in addition to all significant milestone grades such as quarter and
semester grades.

Students' Google Sheet IDs are stored in a csv file with their school email address as a primary key. Their advisor's email address is also included on the record. 

Students can check their grades any time. If they agree with the assessment, then no student-teacher communication is necessary. If not, then we can work together to resolve the discrepancy. 
