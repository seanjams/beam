shell:
	pipenv run flask shell

clean:
	rm -rf instance && rm -f beam.log

status:
	sudo systemctl status lightthebeam.service

start:
	sudo systemctl start lightthebeam.service

stop:
	sudo systemctl stop lightthebeam.service
