Benchmarking for graphql-python/graphene-django#1394

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
Document Length:        974 bytes

Concurrency Level:      100
Time taken for tests:   13.670 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      1246000 bytes
Total body sent:        245000
HTML transferred:       974000 bytes
Requests per second:    73.15 [#/sec] (mean)
Time per request:       1367.026 [ms] (mean)
Time per request:       13.670 [ms] (mean, across all concurrent requests)
Transfer rate:          89.01 [Kbytes/sec] received
                        17.50 kb/s sent
                        106.51 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.9      0       4
Processing:    49 1327 200.0   1386    1597
Waiting:       43 1309 198.4   1369    1586
Total:         49 1327 200.0   1386    1597

Percentage of the requests served within a certain time (ms)
  50%   1386
  66%   1425
  75%   1446
  80%   1459
  90%   1486
  95%   1502
  98%   1530
  99%   1540
 100%   1597 (longest request)
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
Document Length:        47489 bytes

Concurrency Level:      100
Time taken for tests:   24.465 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      47913000 bytes
Total body sent:        239000
HTML transferred:       47489000 bytes
Requests per second:    40.87 [#/sec] (mean)
Time per request:       2446.534 [ms] (mean)
Time per request:       24.465 [ms] (mean, across all concurrent requests)
Transfer rate:          1912.50 [Kbytes/sec] received
                        9.54 kb/s sent
                        1922.04 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.7      0       7
Processing:   350 2293 355.0   2375    2715
Waiting:      340 2292 355.1   2374    2714
Total:        350 2294 353.5   2375    2717

Percentage of the requests served within a certain time (ms)
  50%   2375
  66%   2405
  75%   2434
  80%   2447
  90%   2473
  95%   2498
  98%   2531
  99%   2552
 100%   2717 (longest request)
```

## More tests

Async:

`ab -n 1000 -c 100 -p ./request.txt -T application/json http://127.0.0.1:8000/graphql-async/`
`uvicorn octopus.asgi:application --host 0.0.0.0 --port 8000`

```
Concurrency Level:      100
Time taken for tests:   13.411 seconds
Complete requests:      1000
Failed requests:        0
```
Mem usage: 80mb, 100threads

Sync:

`ab -n 1000 -c 100 -p ./request.txt -T application/json http://127.0.0.1:8000/graphql/`
`gunicorn octopus.wsgi -w 9 -p 8000`

```
Concurrency Level:      100
Time taken for tests:   23.384 seconds
Complete requests:      1000
Failed requests:        0
```

Mem usage: 80mb*9, one thread per process.
