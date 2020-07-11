# Collect_Perfomer_information
Collect area, contact info, activity and equipment of performer in the city. [Multiple account, IP blocked, Header parameter]

## User :
Run the program  
<img src="https://github.com/m1596284/Collect_Perfomer_information/blob/master/Collect_Performers_info.png" width="647" height="426">
<img src="https://github.com/m1596284/Collect_Perfomer_information/blob/master/IG_Host_Tag.gif" width="647" height="426">

## Backstage : Python + Selenium + Request + Beautifulsoup + UserAgent
For example: Hoster  
Phase 1 : Use chromedriver, search #hoster, scroll down for dynamically loading, record all post link.  
Phase 2 : Send "get" to the link and then get the author's ID of each post.  
Phase 3 : Use mulitple threading to login each account then search the ID main page to get the user information.
