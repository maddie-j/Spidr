import wikipedia

#input is spider name
name = "huntsman spider"

#get the summary
summary = wikipedia.summary(name)

#get the url
url = wikipedia.page(name).url

print(wikipedia.summary(name))
print(url)