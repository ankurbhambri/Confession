# CONFESSION

Confession is a multi-user blogging application. There are three types of users who can use this application, Editor, Chief, and anonymous. Anonymous can read only those blogs which are approved by the chief. This project also contains API's with all the functionalities.

    - Editor: Can create and read blogs.
    - Chief: Can read, write, and approve editors' blogs.
    - Anonymous: Only read approved blogs.
#### Features
- Any registered user can write a blog, comment, and reply on approved blogs.
- Custom notification system
- Custom comment-reply system
### Quick Setup
- Create a virtual environment.
  - `virtualenv -p python3.6 venv`
- Activate your virtual environment by
  - `source venv/bin/activate`
- Install required python libraries by using `pip`.
  - `pip install -r requirements.txt`
- Migrate database queries.
  - `python manage.py migrate`
- Finally, run your django runserver.
  - `python manage.py runserver`
