import requests

main_link = "https://www.goodreads.com/author/show/"
author_id = "3389"
params = {
    'format': "xml",
    'key': "P01YdaZOFOdCDwpfaHQ6Pg"
}
response = requests.get(main_link + author_id, params)
with open('author.xml', 'w') as f:
    f.writelines(response.text)
