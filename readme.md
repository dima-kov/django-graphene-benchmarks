# TL;DR


16.547s vs 83.194s for i/o bound queries. 5x faster.
async wins

-----

## Methodology
1. project is a simple django project with a single app.
2. sqlite3 is used as the database, with 3 tables filled in with data (up to a million records)
3. two endpoints are created, one for sync and one for async.
4. versions:
    - `Django==5.0`
    - `uvicorn==0.27.0`
    - `gunicorn==21.2.0`
5. ab - 1000 requests, 10 concurrent requests.

-----

## Async

### Server run:

```uvicorn octopus.asgi:application --host 0.0.0.0 --port 8000```

### AB command



```ab -n 1000 -c 10 -p ./request.txt -T application/json http://127.0.0.1:8000/graphql-async/```

or 
`./run-async.sh.`

### Results:

```
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        uvicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /graphql-async/
Document Length:        959 bytes

Concurrency Level:      10
Time taken for tests:   16.547 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      1231000 bytes
Total body sent:        245000
HTML transferred:       959000 bytes
Requests per second:    60.43 [#/sec] (mean)
Time per request:       165.472 [ms] (mean)
Time per request:       16.547 [ms] (mean, across all concurrent requests)
Transfer rate:          72.65 [Kbytes/sec] received
                        14.46 kb/s sent
                        87.11 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:    14  165  27.8    167     272
Waiting:       13  163  27.5    164     270
Total:         14  165  27.8    167     272

Percentage of the requests served within a certain time (ms)
  50%    167
  66%    174
  75%    179
  80%    183
  90%    196
  95%    211
  98%    224
  99%    235
 100%    272 (longest request)
```

-----


## Sync

### Server run:

```gunicorn octopus.wsgi -w 4 -p 8000```

### AB command:

```ab -n 1000 -c 10 -p ./request.txt -T application/json http://127.0.0.1:8000/graphql/```

or `./run-sync.sh.`

### Results:

```
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        gunicorn
Server Hostname:        127.0.0.1
Server Port:            8000

Document Path:          /graphql/
Document Length:        46975 bytes

Concurrency Level:      10
Time taken for tests:   83.194 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      47399000 bytes
Total body sent:        239000
HTML transferred:       46975000 bytes
Requests per second:    12.02 [#/sec] (mean)
Time per request:       831.942 [ms] (mean)
Time per request:       83.194 [ms] (mean, across all concurrent requests)
Transfer rate:          556.39 [Kbytes/sec] received
                        2.81 kb/s sent
                        559.19 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:   279  825 113.5    823    1180
Waiting:      279  825 113.5    822    1179
Total:        280  826 113.5    823    1180

Percentage of the requests served within a certain time (ms)
  50%    823
  66%    871
  75%    897
  80%    915
  90%    966
  95%   1020
  98%   1090
  99%   1126
 100%   1180 (longest request)
```