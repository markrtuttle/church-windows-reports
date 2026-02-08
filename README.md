# Church Windows Reports

Church Windows Reports is a command line tool written in Python that extracts accounting data from Church Windows and produces custom reports that are not easy to produces with Church Windows itself.  The key objects extracted from Church Windows are the chart of accounts, the transaction journal, the account initial values, and the account budgets.  From these objects other reports can be produced.

[Church Windows](https://churchwindows.com) is church management software from [Computer Helper Publishing](https://churchwindows.com/about/) that provides Donations and Accounting modules to help with church finance.  Church Windows supports double-entry bookkeeping using [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server) to store a few tables, but provides no programatic accesses to the database, making it hard to produce custom reports.  The package works by reconstructing things like the hierarchy of the charge of accounts from a flat csv file dumped by Church Windows.

## Installation

### Install python

To install the package, first install Python and pipx.  

On MacOS, use the [Homebrew package manager](https://brew.sh) and run the following command from a terminal: 

```
brew install python pipx
```

On Windows, install Python using the latest [Python install manager](https://www.python.org/downloads/windows/) from the [Microsoft Store](https://apps.microsoft.com/detail/9nq7512cxl7t).  Be sure the check the box to add Python to your PATH.  With python installed, open an terminal windows and run the commands

```
python -m pip install --user pipx
python -m pipx ensurepath
```

### Install church windows reports

Now clone the repository, build the package, and install the package with 

```
git clone https://github.com/markrtuttle/church-windows-reports.git
cd church-windows-reports
make build
pipx install dist/cwr-*-py3-none-any.whl
```

This will install the tools in something like `$HOME/.local/bin` and you wil have to ensure that this directory is in your path.
## Extracting data

This report generator depends on data extracted from Church Windows.  You will have to extract journal.csv every time your generate a report, but you will have to extract the other files only once, and then only when the chart of account or the budget changes.

Export four files from Church Windows:
* journal.csv: Go to the transaction browser
    * add "date posted" to the list of columns, and
    * export the transcations to CSV.

* balance.csv: Generate the balance statement, but
    * select "zero balances", 
    * confirm the columns tab includes account number, account name, period activity, ytd balance
    * conform the details tab has checked all items, and
    * export to csv

* income.csv: Generate the treasurer's statement, but 
    * select "zero balances"
    * set the fund to general fund
    * set the month
    * confirm the columns tab includes act num, act name, period acty, prev year, ytd bal, budget, and
    * export to csv

* chart.csv: Export COA to CSV.

Now run the commands

```
make-chart
make-initial
make-budget
```

to generate the files chart.json, initial.json, and budget.json that will be used by the report command.

## Generating reports

Now commands like the following will generate text files on the standard output that can be converted to PDF for distribution.

```
report --date 1/1/2026 1/31/2026 --posted 1/5/2026 2/8/2026 --width 120 --bills
report --date 1/1/2026 1/31/2026 --width 120 --subfunds
report --date 1/1/2026 1/31/2026 --posted 1/5/2026 2/8/2026 --width 120 --vendors
report --date 1/1/2026 1/31/2026 --posted 1/5/2026 2/8/2026 --width 120 --ministries
```

## Implementation

The only interesting parts of this package are the three commands like make-chart that reconstruct the hierarchy of the chart of accounts from the flat list exported by Church Windows.  Everything else is routine selection of the interesting transactions to report and text manipulation required for report generation.  The code itself is not particularly Pythonic, even for code written in the days of Python 2.  There is a lot of room for refactoring, simplification, better use of immutable data.