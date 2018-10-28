default:
	@echo "Nothing to make."

clean:
	$(RM) *.pyc *~

veryclean: clean
	$(RM) ministry.pdf unassigned.pdf vendor.pdf

pylint:
	pylint --disable=missing-docstring,duplicate-code *.py report

.PHONY: default clean veryclean pylint
