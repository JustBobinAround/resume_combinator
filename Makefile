run:
	sh ./run.sh

gen-resume-template:
	./.venv/bin/python ./gen_template.py

order66:
	rm ./combos/*
	rm ./pdfs/*
	rm ./texts/*
	rm ./geckodriver
	rm ./geckodriver.log

