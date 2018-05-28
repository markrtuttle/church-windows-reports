# church-windows-reports
Create custom financial reports with data dumped from Church Windows church management software.

This project gives a few modules to manipulate data dumped from Church
Windows.  Church Windows is a common church management software system
that includes an accounting module for keeping the church books.  The
accounting module keeps the data in an sql database and can generate a
number of reports, but there is no programatic interface to the data
or report generation, so routine report generation is error prone and
unusual reports are difficult.

Four modules define objects that parse the csv files dumped by Church Windows
* chart.py: The chart of accounts
* balance.py: The balance sheet
* income.py: The income statement (called the treasurer's report)
* journal.py: The transaction journal

A few modules define manipulate types in the database
* amount.py: The dollar amounts
* date.py: The dates
* number.py: The account numbers

The remaining modules are used to generate reports for a finance committee.
* report: The command line report generator
* arguments.py: The command line argument parser
