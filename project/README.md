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
at 0.66, while testing we thought it was very strict and not very 
user friendly, but simple passwords are one of the mayor contributors to
security breaches, so our users will just have to come up with long passwords. 
It is quite tiresome though, to come up with a password that works, so here is one
that will pass: prcjdøGusbnr3klfud87.

We use the generate_password_hash() from werkzeug.security to hash the
passwords before they are stored in the database. This method both adds
salt and hashes the password. We have manually checked that the password
is not stored directly in the database, and that they are all different. 

#### Login, Logout, and Sessions
The FlaskLogin package provided us with some really useful tools for our application. We started out with
our database, and by using the parameter UserMixin, we did not need to implement any methods for the user class, as
the UserMixin provides this for us. In __init__.py we create the app, and create a login manager, which ties the
application and FlaskLogin together. We also have a user loader there, which is used by FlaskLogin to find a user 
by the ID stored in their session cookie. The database and the blueprints are also created here. Two elements we 
found especially useful from flask was the @login_required and current_user. With this built in method we were able 
to keep track of who was the logged in user, and were therefore able to retrieve the messages that had been sent to them. 
By using the login method in flask a session will be created automatically for that user and the cookie for that
session will be set. When logging out that session is disables and the cookie is replaced as well. We have documented 
how we generated our secret key, now, we are not sure if we should have committed the actual secret key, but since this is a 
school project we hope that it is fine. For a real application one should not commit the secret key. It is important 
that it kept a secret, as it is crucial for securely signing the session cookie. If the secret key is obtained,
it makes it easier to guess the session cookie value, and from there a lot of security breaches can happen. 
More on session cookies in the cookie section below. 



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

We also tried sqlmap to test for any vulnerabilities, but we are not sure it worked as it 
did not seem to do much. It did not warn about anything critical in relation to the sql, but
it did warn about some technical issues we had no problems with. We decided not to look further
into this, and hoped that what we read about SQLAlchemy's filter_by is enough to protect 
our application. 

#### Cross-Site Scripting Protection
Flask automatically sets the httpOnly flag to true. According to Mozilla MDN Web Docs, 
a cookie with the httpOnly attribute will only be sent to the server, and they are
not accessible by Javascript's `document.cookie `API. One is not fully protected 
against XSS attacks with this attribute, in fact, it kind of just lessens the impact
if one were to be submitted to an attack. To actually prevent XSS attacks, one has to 
filter and validate every input. We have used the Jinja templating language to render our HTML templates, meaning that 
whenever a user requests something from our application (such as the login-, signup-, profile- or messaging-page) 
Jinja will respond with an HTML template. Jinja will also automatically escape the HTML which is the primary means to protect
us from xss attacks because we are strictly telling the browser that the data we are sending should be interpreted only as data. 
When displaying the sent and received messages we are not rendering the page, we therefore need to add a countermeasure to 
xss attacks here. We solved this by adding a simple HTML encoder in messaging.py in order to properly sanitize the user input.

#### Cookie inspection
Session cookies makes the user moving in between websites and still being logged in, and it also gives crucial security as it gives the single session-id that 
that user can be and stay logged in with. They are generated and deleted within that "session", so they are not stored anywhere,
which also makes them more secure. 
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


### Answers to the questions


Threat model – who might attack the application? What can an attacker do? What damage could be done (in terms of confidentiality, integrity, availability)? Are there limits to what an attacker can do? Are there limits to what we can sensibly protect against?
##### What are the main attack vectors for the application?
Now that we have committed our secret key several times, it is easier to steal session cookies than it should be.
Furthermore, our session cookie is not set to secure, as it kept creating a bug in Safari, so
that puts us further at risk. Other than that, we think the user input getting messed with is
what puts us  most at risk, but we hope we have implemented enough security to avoid the big three 


##### What should we do (or what have you done) to protect against attacks?
See the other sections on XSS, CSRF, Cookies and SQL Injections to read what we have done
to prevent them. We have had secure design in mind throughout  the process, always checking
if an imported functionality provides good enough security, and we have done our best to 
make the weaker parts of our application resilient enough. We have not been able to attempt
to hack into our own system as much as we would have liked to, but the ways we have tried is
described above. The next step in protecting against attacks would therefore definitely be 
to set up a lot of tests to find every vulnerability our application has.

What is the access control model? 

##### How can you know that your security is good enough?
We have not implemented any logging for this application. It is common to write an event log, and it is smart to keep 
track and know what has happened in one's application. We can see in the terminal 
that flask logs all the requests made to the api, but these are not stored anywhere. It is 
especially important to log events that involve something failing, as the application
often times is at its most vulnerable during these events. If a security breach were to happen, 
it is important to know what exactly happened and what data was exposed. This is especially
important if one is sitting on personal information about users.

We have not tested our application well enough to say that it is completely secure, but that
would be a statement we probably would not have proclaimed after testing every possible attack one
could think of. 

What we have done is read up on the different ways one might be attacked, and implemented 
what we could to protect our application from it. 

