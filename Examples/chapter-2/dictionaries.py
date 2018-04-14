options = {
    'Database': '127.0.0.1',
    'Cache': True,
    'CachePeriod': 15
}

print("Database: " + options["Database"])
if options["Cache"]:
    print("Cached for {} minutes.".format(options["CachePeriod"]))

print("Cache server: {}".format(options.get("CacheServer", "Redis")))
