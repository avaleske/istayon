istayon
=======

A super simple Django site to see if Taylor Swift is on Tumblr right now. You can see it at [istayontumblr.com](http://istayontumblr.com)

<img src="screenshot.png?raw=true" width="250" >

It polls the Tumblr API to see if she's liked or posted anything recently, and makes a guess as to whether or not she's currently online. It's pretty simple so far.

I built this over my winter break because I thought it would be both useful and good practice with Django and web development. It uses Heroku, Django, Memcached, Numpy, the Tumblr API, and a javascript plotting library.

Django provides the web app framework, and I use the dj-static package to serve static files from Django. (There’s not enough traffic yet to warrant setting up S3 for static files.)

I don’t want to hit the Tumblr API on every request, since that would lock up the app for a long time, but I also didn’t want to pay for a second dyno to run a background process that queries the API. My solution was to query the API on the first request, and then use Memcached to store the information from the API for a minute. Since it’s user requests that prompt a cache refresh, I use a Stale-While-Revalidate strategy to avoid the thundering herd problem. You should see the difference in the New Relic stats before and after I got caching working properly.

I use Numpy to bin the results from the “blog/likes” API call into five minute intervals, so I end up with a histogram of likes/interval. I use flot.js to plot this histogram and provide a visual representation of recent activity.

It also scales responsively between desktop browsers and mobile size browsers. It’s based solely on the browser window width.

I recently added a check to see if the site is being loaded on an iPhone/iPad/iPod, and if that’s the case any links to Tumblr use the x-callback-url spec to open the Tumblr app. It’s unlikely anyone using this doesn’t have Tumblr installed on their phone, so I don’t handle that case yet. Based on Google Analytics Android devices are a small minority as well, so on Android links still go the the Tumblr website.
