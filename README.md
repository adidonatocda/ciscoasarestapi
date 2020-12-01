# ciscoasarestapi PROTOTYPE
Automating Cisco ASA Configuration Management with REST API

We work with many customers who are faced with the following business challenges:

•	Firewall Administrator Turnover: Whenever a firewall administrator leaves the organization, there is a need to change the LOCAL firewall passwords. If you are a larger organization, this could mean changing passwords on tens or even hundreds of firewalls.

•	Privileged Accounts and Password Rotation: As a best practice it is a good idea to change your passwords periodically based on a "Password Policy", which is usually determined by your enterprise security, audit, or risk teams. Changing the passwords is a good idea; however, not always easy, or fun to do when you have many devices and a little bit of time.

•	Security and Compliance Requirements: Sometimes periodically changing your password is not just a good idea or best practice, it is required by your organization to maintain compliance with some audit or regulatory mandate.

•	Limited Staff/Time: Changing passwords on a firewall is not a difficult thing to do, changing them periodically is a relatively mundane task, and should be automated. Any task you are going to perform often should be automated to minimize human error, and inefficiencies.

Journey Overview
To address this challenge, I took the following approach to build a tool that will allow for an automated and scheduled process to change Cisco ASA passwords on all devices in your inventory. To start this journey, I took the following approach:
•	Understand business case
•	Build Use Case/Pseudo Code
o	Connect
o	Login
o	Log Output
o	Backup Configuration
o	Get a list of users
o	Get a list of management interfaces # Optional
o	For each LOCAL user with management access and a high privilege level reset the password with a randomly generated strong password that aligns with the "password policy"
o	Log password changes for future use # Maybe later we want to store this information somewhere in the event of "break glass" situation. We could also build functionality to notify the account owner with the new password. If there is interest, we could add a lot more functionality to this tool such as SIEM integration or even integration with a privileged access management (PAM) system.
•	Design and setup the lab for testing
•	Explore Cisco ASA REST API: The Cisco ASA REST API is freely available if you have access Cisco.com. It has been around for a long time and is used by a lot of third-party management tools to interface with your firewalls. The third-party management tool companies will more than likely charge you to use their tool. I like free better 😊. Chances are if you have a Cisco device in your environment you have a login. The REST API has many capabilities and is well documented. Resetting passwords is only one of the possibilities. Over time I am sure I will get more use cases from my customers and team.
•	Test Cisco ASA REST API with PostMan
•	Build the script
•	Test the script
•	Document and post the script

....TRUNCATED...

This prototype script can be added to any job scheduler or automation engine (Jenkins), with some production ready refinements, to run on a periodic basis and allow for password rotation. I would recommend designing your logging and security since the credentials and output of this script could very easily create another audit issue because the passwords are exposed. Maybe later I will introduce some functionality to send the credentials to a vault for encrypted storage and recovery. For now, this is merely a prototype you can use to get up and running with your security automation. This script will also work well if your favorite Firewall admin just quit! If you need help build a production ready automation tool please contact me ( adidonato@criticaldesign.net ). This is more of “Shiv” than a samurai sword!

Script/Solution Overview
If you plan on using this script you will want to make sure you have the following:
o	Install Python
o	Install and create a Python Virtual Environment
o	Clone the repository
o	Test Functions (IN A TESTING ENVIRONMENT, don’t be that guy!)

Script Download/Source
Disclaimer: While this may go without saying, “Do NOT test this in your production environment”
You can access this script and supporting files at the following location. Simply “git clone” the repository and run it against your test environment.
o	Source Code: https://github.com/adidonatocda/ciscoasarestapi 


Script Execution and Testing
adidonato@ML-UBUNTU:~$python CiscoASARESTAPI-BlogPost.py

NOTE: You will be prompted for <username> <password> <enable password>

The rest of this blog is posted on https://criticaldesign.net
