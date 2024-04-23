hello:
	@echo "This file installs the service for the scoretracker application"
	@echo "this will create a service in your systemd folder and enable the service for you"
	@echo "for this to work you will need root privileges"

install: 
	cp ./install-files/scoretracker.service /etc/systemd/system/
	systemctl enable scoretracker.service
	
