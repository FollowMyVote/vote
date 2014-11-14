#These two lines need to exist if you are running from a virtual environment########


##you must customize this path for each webserver
activate_this = 'D:/inetpub/wwwroot/vote/ballot_box/env/Scripts/activate_this.py'

execfile(activate_this, dict(__file__=activate_this))
####################################################################################

import sys
##Enter the path to the site here, this should be the folder containing runserver.py
path_to_site = 'D:/inetpub/wwwroot/vote/ballot_box/'

sys.path.append(path_to_site)

from ballot_box import app as application

