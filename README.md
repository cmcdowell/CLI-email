#CLI-email  

Do you find yourself having to copy and paste log files, configuration files,
and text documents to email them?  
  
How about needing to send a quick email when you are using the command line?  
  
Well how easy does this look?  
  
    $ tail logfile.log | emailer.py 'Here's the latest log' pete@example.com

Run interactively.

    $ emailer.py Lunch pete@example.com
    Please enter your message> Were heading to the coffe shop, meet you there.

Send to multiple email address by separating them wiht a comma.

    $ heroku logs | grep 500 | emailer.py '500 errors for our site' dev@example.com,sysadmin@example.com

##Installation Instructions##

Clone the git repo.

    $ git clone https://github.com/cmcdowell/CLI-email.git
    $ mkdir ~/.bin

Move emailer.py and settings.ini to `~/.bin`
Add this to your .bashrc

    export PATH=$PATH:$HOME/.bin

##Settings##

Add your user name and password to the settings.ini config file. If you aren't
using gmail change the smtp_server and smtp_port to the appropriate values for
your smtp server.

##TODO##

*Attachments  

*Multiple Sender Address
