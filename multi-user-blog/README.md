								Multi-User Blog

Function:

A blog for multiple users. Once an account is registered, users can post and comment. 

Steps:

1. Reach the front page by one of two methods:
	* go to the URL https://jdalcinblog.appspot.com .
	* your localhost server using the file "main.py" in Google App Engine:
   		i. Make sure the location of the files within the "main.py" directory are unaltered. 
   		ii. Get google app engine launcher to reach them (File --> Add existing application). 
   		iii. Make sure your application is assigned to a port not in use. If you have command line "git bash", typing in "netstat -ano" 
   		     into the command line will show all ports currently in use.
   		iv. open on a browser by typing in URL "localhost:<PORT-ID>". <PORT-ID> is the port number that you chose for google app 
   		     engine to launch the project on.
2. register or log into the blog.
3. update the blog with posts and comments.
4. logout when finished.

Notes:
* "main.py" can only be opened with Python 2.7
* the blog consists of one page that continually updates based off the posts of all users.
* users cannot have access to the blog until they register their accounts.
* users can only rate others' posts. 
* users can only edit/delete their own posts and comments.
* users can only register usernames that have yet to be taken.
