import http.client

conn = http.client.HTTPSConnection("www.carmax.com")
payload = ''
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'KmxVisitor_0=StoreId=6140&Zip=30606&Lat=33.9447&Lon=-83.4263&ZipConfirmed=True&ZipDate=2/5/2023 8:42:58 PM&VisitorID=fb4f4065-d9d5-41e6-99e0-e231c887bf4f&IsFirstVisit=False&UsingStoreProxy=false&LastSearch=638014808934299471&sRadius=radius-nationwide&Sort=nearest-distance&Shipping=-1&AdCodeDate=9/21/2022 1:44:09 AM&ShippingRestrictions=true&CookieDate=2/4/2023 2:06:50 AM; _abck=F6EB8FD77C732B0502D9270798CA59C1~0~YAAQ5NoHYFgXeh+GAQAAy7xQIwni/2Z6vtrfCgQHycfl+GT2wbUQN3qXQ5KzYG6zyVroEwWVFAwB7Vk4FEbrcGZFSURc7pJP…bm_sv=B81452128A306D0132B2D6ACCF640F80~YAAQ5NoHYFxueh+GAQAAKvhTIxJEHalI8gUOP/red0woxmYb+o5HOXzIe7L+C0DiEzFsHFmXI31WooJ7XBxE5mkOFyr1J3ma97isB06Q85wGiAUkXxP8DeLdYW1PCUj+IEd6cT0ooce+PmZnAMQBAGO6ZR4ji6SgymMW5zZsMlfklout3yCljMiBvEYLLSDsHWNZ0750Ydpyk4sImU//SIE9htl2ckLTLFX8xjGa57vABve/GXSpGercpD3PUanAgQ==~1; AKA_A2=A; KmxSession_0=logOdds=0.20163299999999995&logOddsA=-1.3442179159999998&logOddsI=1.4917898&SessionId=2b25e75a-6adf-4aca-8ed2-30fdffe4d3fd; ai_session=R29dsrap1CIyVxJpXsd3ge|1675629956834|1675629956834',
    'Host': 'www.carmax.com',
    'Referer': 'https://www.carmax.com/cars/ford/f150/4d-crew-cab/xlt/4wdawd?includenontransferables=true&year=2016-2023&price=50000',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',
}
conn.request("GET", "/cars/api/search/run?uri=/cars/ford/f150/4d-crew-cab/xlt/4wdawd?includenontransferables=true&year=2016-2023&price=50000&skip=48&take=24&zipCode=30606&radius=radius-nationwide&shipping=-1&sort=nearest-distance&scoringProfile=BestMatchScoreVariant3&visitorID=fb4f4065-d9d5-41e6-99e0-e231c887bf4f", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))