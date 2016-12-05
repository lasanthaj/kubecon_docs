#!/bin/bash
sudo echo "IncludeOptional sites-available/*.conf" >> /etc/apache2/apache2.conf
apache2ctl -D FOREGROUND
