.PHONY: all update venv venvupdate docker cleanpy cleanvenv cleanall

# run one shell only
.ONESHELL: all update venv venvupdate docker cleanpy cleanvenv cleanall

# disable running of targets in parallel
.NOTPARALLEL: all update venv venvupdate docker cleanpy cleanvenv cleanall

# predefined variables
CURRDIRECTORY := "$(notdir $(CURDIR))"
DOCKERTAG := "$(shell python -c "print('$(CURRDIRECTORY)'.lower())"):latest"

# check if os is windows or linux/mac
ifeq ($(OS),Windows_NT)
	# windows
	# set python executable path for python virtualenv
	PYTHONVENV := .venv/Scripts/
	PYTHONVENVEXE := .venv/Scripts/python.exe
else
	# linux or mac
	# set python executable path for python virtualenv
	PYTHONVENV := .venv/bin/
	PYTHONVENVEXE := .venv/bin/python
endif

# default target
all: cleanpy update venv
	@echo
	@echo "******************* all FINISHED *******************"
	@echo

# local update of pip/virtualenv
update:
	@echo "+++++++++++++++++++ update START +++++++++++++++++++"
	@echo
	python -m pip install --upgrade pip setuptools wheel poetry virtualenv uv ruff
	@echo
	@echo "******************* update FINISHED *******************"
	@echo

# target for bulding the python venv
venv:
	@echo "+++++++++++++++++++ virtualenv venv START +++++++++++++++++++"
	@echo
	@echo "Local Python Version..."
	python --version
	which python
	@echo
	@echo "Make Virtual Environment..."
#  python -m venv .venv --clear --upgrade-deps
	python -m uv venv --seed
	@echo
	@echo "Check Virtual Environment Python Version..."
	$(PYTHONVENVEXE) --version
	$(PYTHONVENVEXE) -c "import sys; print(sys.executable)"
	@echo
	@echo "Install/Update venv dependencies..."
# $(PYTHONVENVEXE) -m pip install --upgrade pip setuptools wheel poetry
	uv pip install --upgrade pip setuptools wheel poetry jupyter
	@echo
	@echo "Install project dependencies..."
# $(PYTHONVENVEXE) -m pip install --upgrade -r requirements.txt
	uv pip install --upgrade --requirement requirements.txt
	@echo
	@echo "Check for outdated dependencies and just list them..."
	$(PYTHONVENVEXE) -m pip list --outdated
	@echo
	@echo "******************* virtualenv venv FINISHED *******************"
	@echo

# target for upgrading venv
venvupdate:
	@echo "+++++++++++++++++++ venvupdate START +++++++++++++++++++"
	@echo
	@echo "Check Virtual Environment Python Version..."
	$(PYTHONVENVEXE) --version
	$(PYTHONVENVEXE) -c "import sys; print(sys.executable)"
	@echo
	@echo "Update venv dependencies..."
# $(PYTHONVENVEXE) -m pip install --upgrade pip setuptools wheel poetry
	uv pip install --upgrade pip setuptools wheel poetry jupyter
	@echo
	@echo "Update project dependencies..."
# $(PYTHONVENVEXE) -m pip install --upgrade -r requirements.txt
	uv pip install --upgrade --requirement requirements.txt
	@echo
	@echo "Check for outdated dependencies and just list them..."
	$(PYTHONVENVEXE) -m pip list --outdated
	@echo
	@echo "******************* venvupdate FINISHED *******************"
	@echo

# build docker image
docker:
	@echo "+++++++++++++++++++ docker START +++++++++++++++++++"
	@echo
	@echo "Build docker image with TAG: $(DOCKERTAG)"
	@echo
	docker build --progress=plain --tag $(DOCKERTAG) .
	@echo
	@echo "******************* docker FINISHED *******************"
	@echo

# remove cache files
cleanpy:
	@echo "+++++++++++++++++++ cleanpy START +++++++++++++++++++"
	@echo
	rm -rf __pycache__
	@echo
	@echo "******************* cleanpy FINISHED *******************"
	@echo

# remove venv
cleanvenv:
	@echo "+++++++++++++++++++ cleanvenv START +++++++++++++++++++"
	@echo
	rm -rf .venv
	@echo
	@echo "******************* cleanvenv FINISHED *******************"
	@echo

# clean all
cleanall: cleanpy cleanvenv
	@echo
	@echo "******************* cleanall FINISHED *******************"
	@echo
