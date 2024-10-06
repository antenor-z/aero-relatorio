def cache_it(func):
    async def wrapper(*args, **kargs):
        try:
            icao = kargs.get("icao") or args[0]
        except IndexError:
            icao = "default"
        key = f'{icao}:{func.__name__}'
        print(key, end=" :: ")
        cached = json.loads(await client.get(key) or "null", object_hook=datetime_parser)
        if not cached:
            cached = await func(*args, **kargs)
            await client.set(key, json.dumps(cached, default=datetime_serializer), ex=3600)
            print("miss")
        else:
            print("hit")
        return cached            
    return wrapper