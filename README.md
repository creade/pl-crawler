# pl-crawl

### API

```
curl -H "Content-Type: application/json" -X POST -d '["http://www.postlight.com", "http://www.beatport.com/"]' pl-crawler.herokuapp.com/jobs

curl -X GET pl-crawler.herokuapp.com/jobs/2/status

curl -X GET pl-crawler.herokuapp.com/jobs/2/
```

This was my first time using redis as a message broker/queue manager and it went
smoother than I expected it to. I looked at using AWS SQS, instead but I didn't find
the worker support to be nearly as logical as redis and rq. One of the chief frustrations
I had was expanding flask outside of a single app.py in a way that kept the worker and the
tests in contact with the db but without circular dependencies. Flask still felt the
right choice given the lack of web app-y requirements and the simplicity of the API.
I deployed on heroku, but wasted some time trying to get a worker and a daemonized web
process on the same dynamo. Given the low requirements load wise, that sounded
better than splitting them up but I have a feeling that the app dependency of the
worker complicated that enough to make it not justifiable.

My chief concerns with my solution are:
+ The lack of abstractions around the queuing and http requests. Missing these made
unit testing difficult. It sounds like rq has some functionality with SimpleWorker that
may have made this easier.
+ I'm not 100% confident about the behavior of the app as the number of workers
scale.
+ Error handling could be more robust in the present state. Errors during the crawl
stage in particular are being swallowed.

My next steps would be:
+ That gal-danged javascript seems to severely complicate web crawling. Sites like
https://blog.beatport.com/ load only with an svg and an ajax call so the crawler
misses out on the "Keys n Krates" playlist announcement and the like. The solution
would probably be to drop requests in favor of something heavier with a virtual browser.
(a cursory search says splinter?)
+ Images are only pulled from img tags currently, but can appear as css background-images
(like the thumbnails on https://posts.postlight.com/.) Again though, it would probably take
something that virtually rendered pages to tell if the image was actually present or not.
