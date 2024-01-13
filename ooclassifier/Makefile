#### Assumes that ooclassifier.py (and test .py's)
####	are in the current working directory
#### There are total of 10 tests
####	= ( (3 units x 2 inputs) + (2 all tests x 2 inputs) )
DIFF_ARGS = -w --strip-trailing-cr

now:
	# Can change this
	make test

push:
	git commit -a
	git push

validate:
	python3 submission_validator.py

pep8:
# Might have to do, in the VM:  sudo apt install pep8
	pep8 ooclassifier.py

test:
	make unit
	make alltasks

unit:
	make unit1
	make unit2
	make unit3

alltasks:
	make alltasks1
	make alltasks2


# Tests for Task I
unit1:
	@echo "***************************"
	@echo "** Test: case01 - Unit 1 Input 1"
	python3 a1.task.1.unittest.v01.py NoDebug Tests/helpdata.v1 > Tests/helpdata.v1.task.1.out
	diff $(DIFF_ARGS) Tests/helpdata.v1.task.1.out Expected/helpdata.v1.task.1.out.expected
	@echo "** Passed: case01"
	@echo "***************************"
	@echo "** Test: case02 - Unit 1 Input 2"
	python3 a1.task.1.unittest.v01.py NoDebug Tests/weatherdata.v1 > Tests/weatherdata.v1.task.1.out
	diff $(DIFF_ARGS) Tests/weatherdata.v1.task.1.out Expected/weatherdata.v1.task.1.out.expected
	@echo "** Passed: case02"


# Tests for Task II
unit2:
	@echo "***************************"
	@echo "** Test: case03 - Unit 2 Input 1"
	python3 a1.task.2.unittest.v01.py NoDebug Tests/helpdata.v1 > Tests/helpdata.v1.task.2.out
	diff $(DIFF_ARGS) Tests/helpdata.v1.task.2.out Expected/helpdata.v1.task.2.out.expected
	@echo "** Passed: case03"
	@echo "***************************"
	@echo "** Test: case04 - Unit 2 Input 2"
	python3 a1.task.2.unittest.v01.py NoDebug Tests/weatherdata.v1 > Tests/weatherdata.v1.task.2.out
	diff $(DIFF_ARGS) Tests/weatherdata.v1.task.2.out Expected/weatherdata.v1.task.2.out.expected
	@echo "** Passed: case04"


# Tests for Task III
unit3:
	@echo "***************************"
	@echo "** Test: case05 - Unit 3 Input 1"
	python3 a1.task.3.unittest.v01.py NoDebug Tests/helpdata.v1 > Tests/helpdata.v1.task.3.out
	diff $(DIFF_ARGS) Tests/helpdata.v1.task.3.out Expected/helpdata.v1.task.3.out.expected
	@echo "** Passed: case05"
	@echo "***************************"
	@echo "** Test: case06 - Unit 3 Input 2"
	python3 a1.task.3.unittest.v01.py NoDebug Tests/weatherdata.v1 > Tests/weatherdata.v1.task.3.out
	diff $(DIFF_ARGS) Tests/weatherdata.v1.task.3.out Expected/weatherdata.v1.task.3.out.expected
	@echo "** Passed: case06"

# All tests
alltasks1:
	@echo "***************************"
	@echo "** Test: case07 - All Test 1 Input 1"
	python3 a1.alltasks.v01.py NoDebug Tests/helpdata.v1 > Tests/helpdata.v1.alltasks.v01.out
	diff $(DIFF_ARGS) Tests/helpdata.v1.alltasks.v01.out Expected/helpdata.v1.alltasks.v01.out.expected
	@echo "** Passed: case07"
	@echo "***************************"
	@echo "** Test: case08 - All Test 1 Input 2"
	python3 a1.alltasks.v01.py NoDebug Tests/weatherdata.v1 > Tests/weatherdata.v1.alltasks.v01.out
	diff $(DIFF_ARGS) Tests/weatherdata.v1.alltasks.v01.out Expected/weatherdata.v1.alltasks.v01.out.expected
	@echo "** Passed: case08"

alltasks2:
	@echo "***************************"
	@echo "** Test: case09 - All Test 2 Input 1"
	python3 a1.alltasks.v02.py NoDebug Tests/helpdata.v1 > Tests/helpdata.v1.alltasks.v02.out
	diff $(DIFF_ARGS) Tests/helpdata.v1.alltasks.v02.out Expected/helpdata.v1.alltasks.v02.out.expected
	@echo "** Passed: case09"
	@echo "***************************"
	@echo "** Test: case09 - All Test 2 Input 2"
	python3 a1.alltasks.v02.py NoDebug Tests/weatherdata.v1 > Tests/weatherdata.v1.alltasks.v02.out
	diff $(DIFF_ARGS) Tests/weatherdata.v1.alltasks.v02.out Expected/weatherdata.v1.alltasks.v02.out.expected
	@echo "** Passed: case10"


clean:
	# For MacOS
	-rm .DS_Store
	-rm -r __pycache__
	-rm Tests/*.out
