## Report on assignment 2A and 2B
#### By Henriette and Maria
We thought the app.py to be a very messy file, and it seemed as quite a big task to refactor everything to a neat file with
app.py as a starting point. We therefore decided to go for a different route, where we followed this tutorial to get
started with a good form of authentication, the tutorial can be found here: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

#### The functional aspect 
We wanted our web application to function like an email. The logged in entity can send messages to
another user by typing their username in the form, and then enter their message in the message field before pressing send.
To receive messages from a specific user the logged in entity must enter a username in the Search field and then press
the 'Search' button. If a logged in entity wishes to see all messages that have been sent to them, then they can 
simply press the 'Show Inbox' button. There was some implementation already for an announcement function, but since the 
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
in methods for queries and inserts. It also serializes with JSON, which provides more security
than for example Python's Pickle Module. In the login-server project we started out with, 
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
Documentation for how Flask Login works:
https://flask-login.readthedocs.io/en/latest/?fbclid=IwAR0RpkIwylepretehwAcmYzGNh96EL4fbz8nMNtCpN5uLw5R3xe2gj2jRXE
- Need to explain how we use flask.current_user to retrieve the correct messages from the db.

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
raw SQL when querying our database which protects us from SQL injections. In our receive_message() function in messaging.py
we are querying our database with Messages.query.filter_by(sender=user_name, recipient=current_user.username) where 
sender = user_name is input from our form in our application. This could be vulnerable to an injection if user_name contained special 
characters, such as semicolons or apostrophes that could be interpreted as a SQL query. However, the SQLEngine object in SQLAlchemy
will automatically quote them for us,  making it secure from SQL injections. 
source : http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html 

Since you mentioned you weren’t writing raw SQL and are instead using the methods such as `add` you are well protected.
This is because under the hood SQLAlchemy will auto escape any parameters and/or special characters
that would be interpreted as part of valid SQL commands if it were just part of a raw string.
Here is an example below:
When printing out the select query, we can see that it clearly uses
prepared statements, which gives us a much higher level of security t
than something like an f-string would. 

We also tried sqlmap to test for any vulnerabilities, but we are not sure it worked as it 
did not seem to do much. It did not warn about anything critical in relation to the sql, but
it did warn about some technical issues we had no problems with. We decided not to look further
into this, and hoped that what we read about SQLAlchemy's filter_by is enough to protect 
our application. 

#### XSS PROTECTION

Escaping is the primary means to avoid cross-site scripting attacks. When escaping, you are effectively telling 
the web browser that the data you are sending should be treated as data and should not be interpreted in any other way.
f an attacker manages to put a malicious script on your page, the victim will not be affected because the browser will not execute
 the script if it is properly escaped. In HTML, you can escape dangerous characters by using HTML entities, for example, 
 the &# sequence followed by its character code


 - render_template() ensures that we properly escape the html.
 
The HTTP Content-Security-Policy response header allows web site administrators to control
 resources the user agent is allowed to load for a given page. With a few exceptions, 
 policies mostly involve specifying server origins and script endpoints. 
 This helps guard against cross-site scripting attacks (Cross-site_scripting).
 This is especially important when dealing with href tags in html.

Flask automatically sets the httpOnly flag to true. According to Mozilla MDN Web Docs, 
a cookie with the httpOnly attribute will only be sent to the server, and they are
not accessible by Javascript's `document.cookie `API. One is not fully protected 
against XSS attacks with this attribute, in fact, it kind of just lessens the impact
if one were to be submitted to an attack. To actually prevent XSS attacks, one has to 
filter and validate every input. Validating passwords and usernames would be pretty 
easy, as it is standard for websites to have some limitations on exactly what characters 
these can be made up of, but validating the messages seems a bit unrealistic for an email-
sending-and-receiving type application. 
We have not really done either in this application, 
but that would be one of the next steps we would take, if we had more time. 


#### Cookie inspection
Upon inspecting the cookies stored, we noticed that there was a check missing in the
"Secure" column of the cookie attributes. If this attribute is checked, it means that the 
cookie is only ever sent to the server over the HTTPS protocol. Flask has an easy way of 
setting this attribute to true, so we did just that in __init__.py. This unfortunately led to 
some bugs discovered when testing in safari, where it did not seem that the logout
function from flask worked any longer. We therefore decided to leave it out. 
We found from searching
that there were differing opinions on exactly how secure the session cookie provided by
flask really was. According to some, decrypting it was not at all that hard. To further secure
our application, we set the login_manager.session_protection to "strong". This protects 
the users from attacks involving stolen cookies, because the correct IP-address will be  
attached to the cookie

Using cookies for security opposed to access tokens is a conscious choice on our part. 
Access tokens take more time to implement, and they have to be stored somewhere. They are
immune to CSRF attacks, but we found that we would rather implement protection against the
CSRF attacks, and go for cookies. 
https://stackoverflow.com/questions/17000835/token-authentication-vs-cookies

#### Testing 
Testing is important to ensure that the application works as expected, and to validate that it is resistant to exploits.
Optimally, we should have created unit and integration tests, but we instead did some manual tests to check that the 
security measures that we have implemented works as expected. 
- We created a user named B'; DROP TABLE messages'; -- which is a SQL injection that we tried on the old application. 
After we created this user we tried to search for messages from this user to see if the injection would work now. It 
was no longer successful. The reason why we tried this particularly for search for messages is because this queries the database
with the filter function that accepts user input. All of the other queries do not use user input. 
- Try to create a new user with a weak password -> fails as expected
- Try to create a new user that already exists -> fails as expected
- Try to alter the cookie value for the session of the logged in user in the web developer tool -> behaves as expected : when refreshing page the user is automatically logged out 

attached to the cookie, and if the wrong ip-address occurs instead, the browser will jump
to the start page.

#### Further improvements
Validate data, make the cookie secure, 


