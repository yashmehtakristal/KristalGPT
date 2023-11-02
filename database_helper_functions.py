import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta
from dotenv import load_dotenv
import os


DETA_KEY = st.secrets["DETA_KEY"]

# Initialize
deta = Deta(DETA_KEY)

# Connect to or create new Deta Base
db = deta.Base('Kristal_Detabase')


def insert_user(email, username, password):
    """
    Inserts Users into the DB
    :param email:
    :param username:
    :param password:
    :return User Upon successful Creation:
    """

    # Log the date when user was registered
    date_joined = str(datetime.datetime.now())

    # From Documentation: put is the fastest way to store an item in a Base. 
    # If an item already exists under the given key, it will be replaced. 
    # In the case you do not provide a key, Base will automatically generate a 12-character string as a key.

    # Parameters are:
    # Data: The data to be stored.
    # Key: The key (aka ID) to store the data under. Will be auto generated if not provided.
    # Expire_in: Seconds after which the item will expire in
    # Expire_at: Time at which the item will expire

    # Return values:
    # db.put returns a dict with the item’s data.

    # Store inserted object into database
    return db.put({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})


def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """

    # db.fetch() retrieves a list of items matching a query.
    # It will retrieve everything if no query is provided, up to a limit of 1 MB or 1000 items.

    # A query is composed of a single query object or a list of query objects.
    # In the case of a list, the indvidual queries are OR’ed.

    # This returns an instance of FetchResponse.
    # The attributes of FetchResponse are:
    # count (int): The number of items in the response.
    # last (str or None): The last key seen in the fetch response. If last is not None further items are to be retreived.
    # items	(list): The list of items retreived.

    users = db.fetch()
    return users.items


def get_user_emails():
    """
    Fetch User Emails
    :return List of user emails:
    """
    
    users = db.fetch()
    emails = []

    # Accessing the items of the dictionary to get the "key" key (email attribute)
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():
    """
    Fetch Usernames
    :return List of user usernames:
    """


    users = db.fetch()
    usernames = []

    # Accessing the items of the dictionary to get the "username" key (username attribute)
    for user in users.items:
        usernames.append(user['username'])
    return usernames


def validate_email(email):
    """
    Check Email Validity
    :param email:
    :return True if email is valid else False:
    """

    # Pattern start matching from beginning of input string (^)
    # [a-zA-Z0-9_.-]+: This part of the pattern matches the username portion of the email address. It consists of one or more characters that can be letters (both uppercase and lowercase), digits (0-9), hyphens (-), underscores (_) and dots (.)
    # @: This is a literal character and must appear in the email address.
    # [a-zA-Z0-9]+: This part of the pattern matches the domain name (the part after the '@' symbol). It consists of one or more characters that can be letters (both uppercase and lowercase) or digits (0-9).
    # .: This part of the pattern matches the period (dot) character, which separates the domain name from the top-level domain (TLD).
    # [a-z]{1,3}: This part of the pattern matches the TLD (top-level domain), which consists of one to three lowercase letters. 
    # $: This symbol represents the end of a string. It ensures that the pattern matches until the end of the input string.

    # In summary, it checks for the following:
    # Username can contain letters, digits, hyphens, or underscores.
    # Must be an '@' symbol
    # Domain name must consist of letters and/or digits
    # Must be a period (dot) separating the domain name from the TLD
    # The TLD must consist of one to three lowercase letters.

    #pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,9}$" #tesQQ12@gmail.com
    pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # If match, return True. Else, return False
    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    """
    Checks Validity of username
    :param username:
    :return True if username is valid else False:
    """

    # ^: Pattern start matching from beginning of input string
    # [a-zA-Z0-9]: This part of the pattern matches zero or more characters that can be letters (both uppercase and lowercase) or digits (0-9).
    # *: The * quantifier allows for the presence of zero or more such characters.
    # +: The + quantifier allows for the presence of one or more such characters.
    # $: This symbol represents the end of a string. It ensures that the pattern matches until the end of the input string.

    # In summary, this regex pattern is designed to validate strings that meet the following criteria:
    # The string can contain only alphanumeric characters (letters and digits).
    # The string can be empty (zero characters).

    pattern = "^[a-zA-Z0-9]+$"

    if re.match(pattern, username):
        return True
    
    return False


def sign_up():
    with st.form(key='signup', clear_on_submit=True):
        st.subheader('Sign Up')

        email = st.text_input('Email', placeholder='Enter Your Email',
                              help =
                              '''
                              Please make sure:
                              1) You enter a valid email
                              '''
                              )

        username = st.text_input('Username', placeholder='Enter Your Username', 
                                 help =
                                '''
                                Please make sure:
                                1) Username is at least 2 characters long
                                2) Username contains only alphanumeric characters (letters and digits)
                                '''
                                )

        password1 = st.text_input('Password', placeholder='Enter Your Password', type='password',
                                  help =
                                  '''
                                  Please make sure:
                                  1) Length of password is at least 6 characters long
                                  2) Password can contain any characters (letters, digits, underscore, dashes, period etc)
                                  '''
                                  )
        
        password2 = st.text_input('Confirm Password', placeholder='Confirm Your Password', type='password',
                                  help = "Please make sure the password inputted in this field is the same as password inputted in the above field"
                                  )

        # If email is provided
        if email:

            # If email string is according to expected format
            if validate_email(email):

                # If email not in current database
                if email not in get_user_emails():

                    # If username is according to expected format
                    if validate_username(username):

                        # If username not in current database
                        if username not in get_usernames():

                            # If length of username >= 2
                            # & length of password >= 6
                            if len(username) >= 2:
                                if len(password1) >= 6:

                                    # Check if password and confirm password fields are equal to each other
                                    if password1 == password2:
                                        
                                        # Hash the password using stauthenticator library
                                        hashed_password = stauth.Hasher([password2]).generate()

                                        # Add the email, username and hashed password corresponding to the user
                                        insert_user(email, username, hashed_password[0])


                                        st.success('Account created successfully!!')
                                        st.balloons()


                                    else:
                                        st.warning('Passwords Do Not Match')
                                else:
                                    st.warning('Password is too Short')
                            else:
                                st.warning('Username Too short')
                        else:
                            st.warning('Username Already Exists')

                    else:
                        st.warning('Invalid Username')
                else:
                    st.warning('Email Already exists!!')
            else:
                st.warning('Invalid Email')

        # Position & create the sign up button
        btn1, bt2, btn3, btn4, btn5 = st.columns(5)

        with btn1:
            st.form_submit_button('Sign Up')

# sign_uo()