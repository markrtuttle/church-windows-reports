PKG = cwr
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
	pylint \
		--max-line-length=120 \
		--disable=duplicate-code \
		--disable=missing-docstring \
		--disable=too-many-arguments \
		--disable=too-many-instance-attributes \
		--disable=too-many-locals \
		--disable=too-many-positional-arguments \
		--disable=too-many-public-methods \
		src

ruff:
	ruff check --line-length=120 src

ruff-fix:
	ruff check --fix --line-length=120 src

black:
	black --check --line-length=120 src

black-fix:
	black --line-length=120 src

build:
	python3 -m build

install:
	python3 -m pip install --editable .
	python3 -m pip install '$(PKG)[dev]'

uninstall:
	python3 -m pip uninstall $(PKG)

