import redis

r = redis.StrictRedis()

r.set("key", "val")
print (r.get("key"))
# outputs: 'val'

print (r.incr("counter"))
# outputs: 1

r.sadd("connections", "john")
r.sadd("connections", "mary")

print(r.smembers("connections"))
# outputs: {b'mary', b'john'}

print ([m for m in r.smembers("connections")])
# outputs: [b'mary', b'john']
