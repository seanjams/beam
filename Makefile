shell:
	pipenv run flask shell

clean:
	rm -rf instance && rm -f beam.log
