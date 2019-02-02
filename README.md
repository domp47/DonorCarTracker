# DonorCarTracker
Instead of spending every morning checking websites for new vehicles on auction websites, this notifies me when a new vehicle is posted. In my case a corvette from 2006-present.

### Requirements
python3

BeautifulSoup4

python-dateutil

### Installation
0. Clone repository to desired location.
1. Install python3, pip3, and BeautifulSoup4 from pip3.
2. Run Setup.py and enter desired configurations.
3. Set up Cron job to execute script on the desired interval. (Refer to operating system documentation on how to set up cron job or equivalent)
    * For example on Ubuntu the following cron executes at 10 am everyday and outputs any errors to the "cronOutput" file in the DonorCarTracker folder.

```sh
0 10 * * * /usr/bin/python3 /home/dom/DonorCarTracker/DonorCarTracker.py > /home/dom/DonorCarTracker/cronOutput 
```

