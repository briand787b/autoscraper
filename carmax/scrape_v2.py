import http.client

conn = http.client.HTTPSConnection("www.carmax.com")
payload = ''
headers = {
  'Cookie': 'KmxSession_0=SessionId=3d7794a6-ec07-45ac-a0c0-82e1621702bd&logOdds=0.42943299999999995&logOddsA=-1.409797916&logOddsI=0.7750897999999998; KmxStore=StoreId=6031; KmxVisitor_0=StoreId=6031&Zip=30523&Lat=34.6538&Lon=-83.5257&ZipConfirmed=True&ZipDate=2/5/2023 5:14:53 PM&VisitorID=813d3095-16d6-4bad-9287-0eb43afb7d3b&CookieDate=2/2/2023 3:20:27 AM&IsFirstVisit=False; _abck=8261582D852BF143C3DFDD6532142EA0~-1~YAAQXA3eFwQkxx+GAQAA59zSIQn3Phm3R3vABJi8Thi/gice6+itMcXrT+am6h95AWNHAz4c5TJZ74AyQzmRsRYrtM6g2IK9KuvG3Lf00j/BytVsbLD+6vKa4Zw3ZL+DwZ7ngDbSBrOHhIrSUrYcfhgb5YYXLOpWg1P/9MSCKE6Qc1I86ZkP442BJ6K6GP+BFXKrntPmDcHzzGArRG07c1aXDSMTjypXtFdTe8JnDjLolzlsr3m6ODvBWSGDn+gY0d5J7AVFlXGXM5H8+bxur56ANFROq0HbFLJO09dxsZR0QWzBnJnpqnXscjc4f9y7IbfXAYwPD0VnZxYLz3NIiKRjS/wAmBkBAyLeZ7npZ3wCFGvP5EpUuow6H8QL21KZdqPtCTzXUA==~-1~-1~1675311518; ak_bmsc=6CBB91F1FDEF53D22521F2EE56DE72FE~000000000000000000000000000000~YAAQucDOF9qENxaGAQAAtQ95IhKwXlq/IStLE+7/7OQ9dEgSWwJC/72C+fgm2ixHBPSr5yTV0jeoiMbqI5QvDZyb76g4TlX2B0WKQyGwo822AXqUbg3oTbAry/xeCaBXfEBfZsal1K9Z9GQfCVRI77xVEIb53kBQOVE/Y7jN2R0tz8+m7z+ceX4feq96vVqw6VdyiPww0ZLyfoJASdrEsrNrnrIwenXjhjk03vgTMwjIY6iNDtU6uTmJqWYw8n82KGRg+YtVApWk+NsIgB/wdVztVlTnPC01NmYNvbE6Kv+LRjxqggdVIJyMuLkNFkeHZT9lphPU4r7f+7tOKYx67jY+9jW8oIXmF5mkM4IWvZYQJBd05Ft8cD4hSnEiJTFzxJeBof0145tADwPQfuU=; bm_sv=09F9F95BA4CB0C0D1C30B5CA2F49636C~YAAQjMDOFzYgDtCFAQAANdaSIhJ73zqFEUNCqcs56G45ZKIIATxGrpNe310mNsKVN0QjSSnJNwa7utBNIwBHIXGqg+hYMc0GfuB4t9wn5NVdTVW0uvb3my1NcNzMc4p+FkJOMOIFVkNEH+UMMHFxrirAor1fTerCbdaFfLf8DXnlST7lYrwVtDN0a3bNmGVSXNoNamAza/+CoLtDbOqWCXRJGLO2n6Gfz+cln/exZoLHGu3hFJVhAGsVEgavyNJo~1; bm_sz=2C9A919667AFE729DFDA52949B3EAC7A~YAAQXA3eFwckxx+GAQAA59zSIRJwmml1wVoJkElYIAWi68tsjKgdOtlBr2hEJgYPzGpWRVCHRt/IMZSeLGKY//WvMcKJe7odkKqWoKbQprI3u2rK5Y9Frge281Wlfa57AdjCbpd9o0KJsVI/KNSvNLAhLtfaOchJsq4n0ZWpVgzNrvt5jmM6MjbvACBbJD6k6so3IhuRseh2mW7t8V6z8n4/fyoxJdSk/Nzjv1jlX2RRZIRfKP/jDFrGV9zq5PZ0hjaFqREmCGGj77kRRcSVf7INLHQ5sK/eJFmvwqcSqyIUdgE=~3294771~3359537'
}
conn.request("GET", "/cars/api/search/run?uri=/cars/chevrolet/tahoe?includenontransferables=true&skip=0&take=100&zipCode=30523&radius=radius-nationwide&shipping=-1&sort=lowest-price&scoringProfile=BestMatchScoreVariant3", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))