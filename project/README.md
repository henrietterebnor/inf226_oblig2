## Report on assignment 2A and 2B
#### By Henriette and Maria
We thought the app.py to be a very messy file, and it seemed as quite a big task to refactor everything to a neat file with
app.py as a starting point. We therefore decided to go for a different route, where we followed this tutorial to get
started with a good form of authentication, the tutorial can be found here: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

Testing :
Write unit and integration tests to validate that all critical flows are resistant to the threat model. 
Compile use-cases and misuse-cases for each tier of your application

Har testet selv:
- endre cookie, session avbrutt og vi blir logget ut.
- SQL injection 


The HTTP Content-Security-Policy response header allows web site administrators to control
 resources the user agent is allowed to load for a given page. With a few exceptions, 
 policies mostly involve specifying server origins and script endpoints. 
 This helps guard against cross-site scripting attacks (Cross-site_scripting).
 This is especially important when dealing with href tags in html. 
 

 https://flask-login.readthedocs.io/en/latest/?fbclid=IwAR0RpkIwylepretehwAcmYzGNh96EL4fbz8nMNtCpN5uLw5R3xe2gj2jRXE
 
 
 XSS:
 https://semgrep.dev/docs/cheat-sheets/flask-xss/ --> render_template with flask and xss attack
 mitigation. 
 
 Escaping is the primary means to avoid cross-site scripting attacks. When escaping, you are effectively telling 
 the web browser that the data you are sending should be treated as data and should not be interpreted in any 
 other way.

SQL INJECTION PROTECTION:
Since you mentioned you weren’t writing raw SQL and are instead using the methods such as `add` you are well protected.
This is because under the hood SQLAlchemy will auto escape any parameters and/or special characters
that would be interpreted as part of valid SQL commands if it were just part of a raw string.
Here is an example below:
When printing out the select query, we can see that it clearly uses
prepared statements, which gives us a much higher level of security t
than something like an f-string would. 

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
