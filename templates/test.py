import requests
r=requests.head('http://www.sexx2015.com/get_file/1/45b4a70a371ea09091fdbb8960bf3bb2/32000/32028/32028.mp4/?download=true&download_filename=4b38517243255a9281477dcfed57da83.mp4')

r=requests.head('http://www.sexx2015.com/get_file/1/4de481cd8c17291fd7f987402b87c343/18000/18266/18266.mp4')
print(r)
local = r.headers.get('Location')
print(local)
l = requests.head(local)
print(l)

