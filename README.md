# Light the Beam
This code hits the NBA.com API daily to check for a Sacramento Kings game.
If it finds a Kings game, it calls the API every 10 minutes to see who won the game.
If the Kings win, turn the porch light purple. Light the beam!!!

For RaspberryPi, adjust as needed for mac setup.
```bash
sudo nano /lib/systemd/system/lightthebeam.service
```

Copy the following contents and save. This will call `./run.sh` on system boot:
```
[Unit]
Description=Light the Beam
After=multi-user.target

[Service]
Type=simple
ExecStart=/bin/bash -c "PATH=$PATH:/home/pi/.local/bin exec /home/pi/Documents/code/beam/run.sh"
WorkingDirectory=/home/pi
User=pi
Environment=HUE_BRIDGE_IP=<Your Hue Bridge IP>
Environment=HUE_BRIDGE_USERNAME=<Your Hue Bridge Username>

[Install]
WantedBy=multi-user.target
```

Trigger the job manually with:
```bash
sudo systemctl start lightthebeam.service
sudo systemctl status lightthebeam.service
sudo systemctl stop lightthebeam.service
```
