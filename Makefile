# chart.csv
# reports/export -> export -> coa data -> export
# 
# balance.csv
# reports/export -> financial -> balance sheet
# accounts with zero balancce
# detail -> total funds -> temporarily restricted -> check all
# export
# 
# income.csv
# reports/export -> financial -> treasurer's report
# accounts with zero balances
# fund -> general fund
# export
# 
# vendor.csv
# reports -> transaction -> general ledger -> account = accounts payable/vendor
# export
# 
# journal.csv
# date posted
# export
# 

FLAGS = --month $(shell date +%m)

default:
	@echo "Nothing to make."

ministry:
	report --ministry-report $(FLAGS)

unassigned:
	report --unassigned-report $(FLAGS)

vendor:
	report --vendor-report $(FLAGS)


ministry.pdf:
	report --ministry-report --landscape $(FLAGS) | \
		enscript -r -B -o - | \
		ps2pdf - $@

unassigned.pdf:
	report --unassigned-report $(FLAGS) | \
		enscript -B -o - | \
		ps2pdf - $@

vendor.pdf:
	report --vendor-report $(FLAGS) | \
		enscript -B -o - | \
		ps2pdf - $@

.PHONY: ministry.pdf unassigned.pdf vendor.pdf
.PHONY: ministry unassigned vendor

clean:
	$(RM) *.pyc *~

veryclean: clean
	$(RM) ministry.pdf unassigned.pdf vendor.pdf
pylint:
	pylint --disable=missing-docstring,duplicate-code *.py report



