import httplib2
def test_connection():
    conn = httplib2.Http(".cache")
    (resp_headers, content) = conn.request("http://localhost:80", "GET")
    print('response status: %s' % resp_headers.status)
    print ('HTTP connection closed successfully')
    if resp_headers.status in [200, 301]:
        return True
    else:            
        return False

print(test_connection())