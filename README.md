IsTayOnTumblr?
=======

A super simple Django site to see if Taylor Swift is on Tumblr right now. You can see it at [istayontumblr.com](http://istayontumblr.com)

<img src="screenshot.png?raw=true" width="250" >

It polls the Tumblr API to see if she's liked or posted anything recently, and makes a guess as to whether or not she's currently online. It's pretty simple so far.

##Setup##
###Install Prereqs###
To run this locally you'll need a few things. (These instructions are for OS X. They're also from memory. I'll clean them up later, but some of you are playing with it now.)
- You need to have Python, pip, and setuptools installed. Do it with the instructions [here](http://docs.python-guide.org/en/latest/starting/install/osx/).
- Then use pip to install virtualenv and virtualenvwrapper with commands like `pip install <package name>`. Details about those can be found [here](https://github.com/kennethreitz/python-guide/blob/master/docs/dev/virtualenvs.rst). Basically, virtualenvs keep your python packages local to your projects.
- Installing the [Heroku Toolbet](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)) is the easiest way to install foreman and the other tools you'll need.
- You'll also need to have a local install of PostgreSQL. I used [Postgres.app](http://postgresapp.com/) because I'm lazy.
- You need to install memcached for the caching service, which you can do with `brew install memcached` if you installed Homebrew. (If you haven't, it's in the python installation instructions above.) Details on how to setup memcached to be easy to launch are [here](http://www.rahuljiresal.com/2014/03/installing-memcached-on-mac-with-homebrew-and-lunchy/).
- Go to the Tumblr API documentation and [request and API key](https://www.tumblr.com/oauth/apps).
- Also, add `alias fucking="sudo"` to your `.bash_profile`. It's not necessary, I just find it funny.

###Getting it running###
- Okay, you've cloned this this repo somewhere. If not, do that.
- Now you need to create a virtualenv. Do that with `mkvirtualenv istayon` assuming you got virtualenvwrapper installed.
- Then activate the virtualenv with `workon istayon`. Now your python should point to the python in the virtualenv. You can confirm that with `which python`.
- Install the required pip packages. From the same directory as the `requirements.txt` file, do 'pip install -r requirements.txt --allow-all-external'.
- create a `.env` file in the root of the project. Foreman sets the entries in the file as your environment variables, and `settings.py` checks environment variables for things like the API keys and database connection strings. This file is .gitignored so this sensitive stuff stays out of source control. If you deploy to Heroku, then you'll have to add these environment variable in the admin interface. We use the following entries for the local site:
```
PYTHONUNBUFFERED=true
DATABASE_URL=postgres://localhost/istayon
SECRET_KEY=<makup a long string for this with random characters>
DEBUG=Anything_because_strings_are_truthy
TUMBLR_API_KEY=
TUMBLR_API_SECRET_KEY=
NEW_RELIC_APP_NAME=default1
MEMCACHEDCLOUD_SERVERS=127.0.0.1:11211
MEMCACHEDCLOUD_USERNAME=<this can be blank for local>
MEMCACHEDCLOUD_PASSWORD=<you don't need this either>
```
- Open the postgres console (should just be able to hit the elephant in your menu bar) and create a database called `istayon` with `CREATE DATABASE istayon`. You might have to make a user first? Try it, and check the PostgreSQL documentation if it doesn't work. (I'm writing this from memory.)
- From the root of the project, run `foreman run ./manage.py syncdb` to setup the django databases. This might ask you to create a superuser. That's for the admin interface, which isn't currently used, but go ahead and make one if you want.
- I think you should just be able to do `foreman start web` at this point. I'm sorry if I'm missing something. If it's working, you chould be able to go to `localhost:5000` and see the site.

If I forgot something or it doesn't work, open an issue or let me know. If you want to deploy to Heroku, I'm using the Heroku Postgres, MemcachedCloud, Papertrail, and New Relic addons, so you'll need to provision those. They all have free tiers.

##About##

I built this over my winter break because I thought it would be both useful and good practice with Django and web development. It uses Heroku, Django, Memcached, Numpy, the Tumblr API, and a javascript plotting library.

Django provides the web app framework, and I use the dj-static package to serve static files from Django. (There’s not enough traffic yet to warrant setting up S3 for static files.)

I don’t want to hit the Tumblr API on every request, since that would lock up the app for a long time, but I also didn’t want to pay for a second dyno to run a background process that queries the API. My solution was to query the API on the first request, and then use Memcached to store the information from the API for a minute. Since it’s user requests that prompt a cache refresh, I use a Stale-While-Revalidate strategy to avoid the thundering herd problem. You should see the difference in the New Relic stats before and after I got caching working properly.

I use Numpy to bin the results from the “blog/likes” API call into five minute intervals, so I end up with a histogram of likes/interval. I use flot.js to plot this histogram and provide a visual representation of recent activity.

It also scales responsively between desktop browsers and mobile size browsers. It’s based solely on the browser window width.

I recently added a check to see if the site is being loaded on an iPhone/iPad/iPod, and if that’s the case any links to Tumblr use the x-callback-url spec to open the Tumblr app. It’s unlikely anyone using this doesn’t have Tumblr installed on their phone, so I don’t handle that case yet. Based on Google Analytics Android devices are a small minority as well, so on Android links still go the the Tumblr website.
