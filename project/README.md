## Report on assignment 2A and 2B
#### By Henriette and Maria
We thought the app.py to be a very messy file, and it seemed as quite a big task to refactor everything to a neat file with
app.py as a starting point. We therefore decided to go for a different route, where we followed this tutorial to get
started with a good form of authentication, the tutorial can be found here: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

#### The functional aspect 
We wanted our web application to function like an email. The logged in user can send messages to
another user by typing their username in the form, and then enter their message in the message field before pressing send.
To receive messages from a specific user the logged in user must enter their username in the Search field and then press
the 'Receive single' button. If a logged in user wishes to see all messages that have been sent to them, then they can 
simply press the 'Receive all' button. There was some implementation already for an announcement function, but since the 
assignment did not mention anything about it, and how it should work, we chose to remove this entirely. We have removed the
announcement function from our code as well since it would have been unused. It is good practice to always remove unused code
as the greater the amount of code, the greater the risks for bugs which causes the application to be more vulnerable for exploits.

#### The issue with the previous application
The original application had many flaws that needed improving. The first thing
we wanted to improve was the structure. App.py was ill-structured, and had a lot 
of different purposes. We started out with isolating the login-logout stuff, and
followed a tutorial from this page: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
We found that a lot of secure procedures came free with flask_login, and the tutorial 
also included the hashing of password, and of course password checking, which lacked 
in the original project. We decided to continue using SQLAlchemy, which the tutorial also
used, and it proved very useful in the protection of sql injections with the built
in methods for queries and inserts. In the login-server project we started out with, 
there was a lot of raw SQL, which is what one should especially avoid to protect oneself
against SQL-injections. The original project only used a dictionary as a database for
the users, so we created messages and user tables in the database. 

The original project did not handle any of the common security exploits, and we will now discuss
how we have implemented protection against these. 


#### Handling passwords
We implemented password checking from the package password_strength, 
and decided to only check the strength, and not uppercase and length 
etc, because we know these requirements do not matter particularly, as
length is the most important when it comes to password guessing and 
brute force attacks. 
We saw the recommendation of limiting the password strength requirement
at 0.66, but while testing we thought it was very strict and not very 
user friendly, so we decided to be a bit more lenient than recommended
and set it at 0.5.
It is quite tiresome to come up with a password that works, so here is one
that will pass: prcjdøGusbnr3klfud87.

We use the generate_password_hash() from werkzeug.security to hash the
passwords before they are stored in the database. This method both adds
salt and hashes the password. We have manually checked that the password
is not stored directly in the database, and that they are all different. 

#### Login, Logout, and Sessions
@loginrequired
forklare hvordan vi henter dataeen til current user i messages. 

#### CSRF - attack prevention
In order to prevent CSRF attacks we enabled CSRF protection globally for our Flask app in __init__.py. 
CSRF attacks are made possible because browser requests automatically include the session cookies, we
therefore need to attach a CSRF token to our POST requests in our app. The reason why we need to add CSRF
token to our POST methods is because this is a request that modifies the state on the server.
Since CSRF tokens are random and unguessable strings we now have a way of validating the request origin, hence
preventing malicious requests from the same browser by an attacker. 

We have attached csrf token to these requests (comment added in the code as well):
- When we are signing up a user in auth.py we are making a POST-request in signup.html
- When we are logging in a user in auth.py we are making a POST-request in login.html 
- When we are sending a message in sending.html we are making a POST-request

#### SQL Injection Protection
As mentioned previously we decided to use SQLAlchemy to init our database for this app. SQLAlchemy provides 
useful builtin methods for queries and inserts. Because of this we avoid having to write 
raw SQL when querying our database which 

Since you mentioned you weren’t writing raw SQL and are instead using the methods such as `add` you are well protected.
This is because under the hood SQLAlchemy will auto escape any parameters and/or special characters
that would be interpreted as part of valid SQL commands if it were just part of a raw string.
Here is an example below:
When printing out the select query, we can see that it clearly uses
prepared statements, which gives us a much higher level of security t
than something like an f-string would. 

#### XSS PROTECTION
The HTTP Content-Security-Policy response header allows web site administrators to control
 resources the user agent is allowed to load for a given page. With a few exceptions, 
 policies mostly involve specifying server origins and script endpoints. 
 This helps guard against cross-site scripting attacks (Cross-site_scripting).
 This is especially important when dealing with href tags in html

### Testing 
Testing is important to ensure that the application works as expected, and to validate that it is resistant to exploits.
Optimally, we should have created unit and integration tests, but we instead did some manual tests to check that the 
security measures that we have implemented works as expected. 
- We created a user named B'; DROP TABLE messages'; -- which is a SQL injection that we tried on the old application. 
After we created this user we tried to search for messages from this user to see if the injection would work now. It 
was no longer successful, meaning that our 
- Try to create a new user with a weak password -> fails as expected
- Try to create a new user that already exists -> fails as expected
- Try to alter the cookie value for the session of the logged in user in the web developer tool -> behaves as expected : when refreshing page the user is automatically logged out 

. 

 https://flask-login.readthedocs.io/en/latest/?fbclid=IwAR0RpkIwylepretehwAcmYzGNh96EL4fbz8nMNtCpN5uLw5R3xe2gj2jRXE


The 

#### Cookie inspection
Upon inspecting the cookies stored, we noticed that there was a check missing in the
"Secure" column of the cookie attributes. If this attribute is checked, it means that the 
cookie is only ever sent to the server over the HTTPS protocol. Flask has an easy way of 
setting this attribute to true, so we did just that. We found from searching
that there were differing opinions on exactly how secure the session cookie provided by
flask really was. According to some, decrypting it was not at all that hard. To further secure
our application, we set the login_manager.session_protection to "strong". This protects 
the users from attacks involving stolen cookies, because the correct IP-address will be  
attached to the cookie