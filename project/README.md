## Report on assignment 2A and 2B
#### By Henriette and Maria

#### How to get started with our project
After cloning you will have two directories, one named project, and one names auth. auth is our virtual 
environment. You can try activating it, but if your IDE does not recognize it as such, just delete the auth directory and
run these commands in the terminal inside the project inf226_oblig2:
```
python3 -m venv auth 
source auth/bin/activate 
export FLASK_APP=project`
```
Hopefully you don't run into too much trouble installing the different packages you will need. 
Now this may be caused by some shortcomings on our part, but sometimes installing a package requires using
pip3 but most of the time pip works. Sometimes it only works outside the virtual environment and sometimes
it only works inside the virtual environment. 

A last resort that has never failed (me) has been to go to
Pycharm (in the toolbar) -> preferences -> Python Interpreter -> click the plus -> search up the package there.
Remember that the _ in package names when importing them are replaced by - here. 
(these are instructions for mac, I hope windows users have less problems.)

The other directory, project, contains all the python and html for the project. To run the project, assuming you 
have all the packages you need and that you have ran the three commands listed above, all you need to do is type
flask run (hopefully)

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
We found that a lot of secure procedures came free with FlaskLogin, and the tutorial 
also included the hashing of password, and of course password checking, which lacked 
in the original project. We decided to continue using SQLAlchemy, which the tutorial also
used, and it proved very useful in the protection of sql injections with the built
in methods for queries and inserts. In the login-server project we started out with, 
there was a lot of raw SQL, which is what one should especially avoid to protect oneself
against SQL-injections. The original project only used a dictionary as a database for
the users, so we created messages and user tables in the database.

The original project did not handle any of the common security exploits like session managing, password handling, CSRF, and
xss and SQL injections. We will now go into detail on how we have mitigated the risks of such attacks. After this
we will answer the questions from 2B.


#### Login, Logout, and Sessions
The FlaskLogin package provided us with some really useful tools for our application. We started out with
our database, and by using the parameter UserMixin, we did not need to implement any methods for the user class, as
the UserMixin provides this for us. In __init__.py we create the app, and create a login manager, which ties the
application and FlaskLogin together. We also have a user loader there, which is used by FlaskLogin to find a user 
by the ID stored in their session cookie. The database and the blueprints are also created here. Two elements we 
found especially useful from flask was the @login_required and current_user. With this built in method we were able 
to keep track of who was the logged in user, and were therefore able to retrieve the messages that had been sent to them. 
By using the login method in flask a session will be created automatically for that user and the cookie for that
session will be set. When logging out that session is disabled and the cookie is replaced as well. We have documented 
how we generated our secret key, now, we are not sure if we should have committed the actual secret key, but since this is a 
school project we hope that it is fine. For a real application one should not commit the secret key. It is important 
that it kept a secret, as it is crucial for securely signing the session cookie. If the secret key is obtained,
it makes it easier to guess the session cookie value, and from there a lot of security breaches can happen. 
More on session cookies in the cookie section below. 

#### Cookie inspection
Session cookies makes it possible for a user to move in between websites and still be logged in, and it also gives crucial security as it gives the single session-id that 
that user can be and stay logged in with. They are generated and deleted within that "session", so they are not stored anywhere,
which also makes them more secure. 
Upon inspecting the cookies stored, we noticed that there was a check missing in the
"Secure" column of the cookie attributes. If this attribute is checked, it means that the 
cookie is only ever sent to the server over the HTTPS protocol. Flask has an easy way of 
setting this attribute to true, so we did just that in __init__.py. This unfortunately led to 
some bugs discovered when testing in safari, where it did not seem that the logout
function from flask worked any longer. We therefore decided to leave it out. 
We found from searching that there were differing opinions on exactly how secure the session cookie provided by
flask really was. According to some, decrypting it was not at all that hard. To further secure
our application, we set the login_manager.session_protection to "strong". This protects 
the users from attacks involving stolen cookies, because the correct IP-address will be attached to the cookie

#### Handling passwords
We implemented password checking from the package password_strength, 
and decided to not worry about enforcing uppercase letters, digits, special characters,
etc., as length is the most important attribute when it comes to password guessing and 
brute force attacks. We saw the recommendation of limiting the password strength requirement
at 0.66, while testing we thought it was very strict and not very 
user friendly, but simple passwords are one of the mayor contributors to
security breaches, so our users will just have to come up with long passwords. 
It is quite tiresome though, to come up with a password that works, so here is one
that will pass: prcjdøGusbnr3klfud87.

We use the generate_password_hash() from werkzeug.security to hash the
passwords before they are stored in the database. This method both adds
salt and hashes the password. We have manually checked that the password
is not stored directly in the database, and that they are all different. 

#### CSRF - attack prevention
In order to prevent CSRF attacks we enabled CSRF protection globally for our Flask app in __init__.py. 
CSRF attacks are made possible because browser requests automatically include the session cookies, we
therefore need to attach a CSRF token to our POST requests in our app. The reason why we need to add CSRF
tokens to our POST methods is because these are request that modifies the state on the server.
Since CSRF tokens are random and unguessable strings we now have a way of validating the request origin, hence
preventing malicious requests from the same browser by an attacker. 

We have attached csrf token to these requests (comment added in the code as well):
- When we are signing up a user in auth.py we are making a POST-request in signup.html
- When we are logging in a user in auth.py we are making a POST-request in login.html 
- When we are sending a message in sending.html we are making a POST-request

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


#### Testing 
Testing is important to ensure that the application works as expected, and to validate that it is resistant to exploits.
Optimally, we should have created unit and integration tests, but we instead did some manual tests to check that the 
security measures that we have implemented works as expected. 
- We created a user named B'; DROP TABLE messages'; -- which is a SQL injection that was successful in the search field 
of the old application. The search function would be the most vulnerable to SQL injections, though it is possible in insert 
statements as well. After we created this user we tried to search for messages from this user to see if the injection 
would work now. We also tried sending messages to this user, and it did not hurt our database. These are the only two 
functions that use the SQLAlchemy functions with user input. We also created a user named B, and wrote the same as above
in the search field. Neither this hurt our database.
- Try to create a new user with a weak password -> fails as expected
- Try to create a new user that already exists -> fails as expected
- Try to alter the cookie value for the session of the logged in user in the web 
developer tool -> behaves as expected : when refreshing page the user is automatically logged out 

### Answers to the questions

##### Threat Model
The assets that we need to protect are the user credentials as well as the messages that the users have sent
to each other as these can contain sensitive and private information. The threat agents therefore
have interests in gaining access to this information for a number of reasons. 
If an attacker is successful in a password attack then confidentiality, authenticity, and availability would be compromised.
Private messages would be made available, and the attacker could also impersonate as the user and send messages
to others. Furthermore, the attacker being logged into the account would disable the actual user from accessing it. 

Phishing, brute-forcing, and dictionary attacks are some ways of retrieving a password, so how can we counter measure these?
By enforcing the user to create a strong passwords with a good length we make it much harder for an attacker to 
successfully brute-force the password, and to prevent dictionary attacks we can encrypt the password with salt in our database.

It is, however, quite hard to protect against all phishing attacks during application development as a successful phishing attack
often is a result of a weakness from the user. One phishing attack we can counter measure is CSRF, which happens when a user is tricked
into clicking a link or loading page. In CSRF the attacker gains access over the session cookie which contains authentication data and
represents the user’s session. This is exploited to impersonate the user to perform malicious actions. If we add CSRF tokens to the users requests we have a 
way of validating the origin of the request which mitigates these types of attacks. 

Injection attacks like xss and sql injections could also result in compromised user credentials. These types of attacks
pose a threat to not only confidentiality, integrity and availability as the data within the application could be 
changed in an unauthorized manner which could cause issues with the availability of the application. To prevent these types
of attacks it is important to sanitize user input so that it cannot be interpreted as SQL queries, html tags or css. 

The limitations of the hacker depends heavily on the difficulty of the attack compared to how high the reward is. If our application
were to be used as a mailing system in a successful business were the employees were to share sensitive and valuable information then the likelihood 
of being exposed to attacks would most certainly increase. The limitations of what we can sensibly protect against follows the same rules. Questions like : should we
spend a lot of resources on protecting something that has a low likelihood on being attacked?, and How big is the impact of that attack? Are important in order to
determine what mitigations are within reason to perform. 

##### What are the main attack vectors for the application?
- Compromised credentials where the username and password are exposed to an unauthorized entity. 
- Missing encryption on data in transit. For now our application runs locally, but if this was not the case 
the users messages would be vulnerable to passive attackers, compromising integrity and confidentiality. 
- We are dealing with an email system so the users could be tricked into giving away personal and sensitive information 
as a result of phishing. 
- Injection of malicious scripts in our input fields

##### What should we do (or what have you done) to protect against attacks?
See the other sections on XSS, CSRF, Cookies and SQL Injections to read what we have done
to prevent them. We have had secure design in mind throughout  the process, always checking
if an imported functionality provides good enough security, and we have done our best to 
make the weaker parts of our application resilient enough. We have not been able to attempt
to hack into our own system as much as we would have liked to, but the ways we have tried is
described above. The next step in protecting against attacks would therefore definitely be 
to set up a lot of tests to find every vulnerability our application has.

##### What is the access control model? 
In order for a user to access the mailing system that user first needs to be authenticated. Once
authenticated that user gains access to their own emails and profile, it is not possible for any user
to view conversations between others. Furthermore, a user can message any existing user, it is 
therefore no restrictions on who you can send messages to. Given more time, we would have liked to change
this and added functionality that would make it possible to block other users. But, for now all users
have the same access rights, hence there exists no users with more privileged rights than others. 

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

