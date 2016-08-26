# Basecamp 2 API scripts
Python scripts that get data about Basecamp projects from the Basecamp 2 API
## How to use

These should be used on your local machine only as password/username are included in the script.

It was created for some quick rsearch on usage figues but the `Comment` class in particular will run slowly if there are a large number of topics/messages to run through.

For both classes, you will need to define:

 - username and password
 - list of 1 or more topic urls to send when constructing the class (the API produces 50 objects per page with the remaining objects accessible via `?page=2`, `?page=3` etc.)
 
The `Comment` class also requires you to define a msg_url - this is the API list for the project you wish to access with `{}` used to insert the message id.

You can then call the class using the commented out test code.

## Documentation

Read the [Basecamp 2 API documentation](https://github.com/basecamp/bcx-api).