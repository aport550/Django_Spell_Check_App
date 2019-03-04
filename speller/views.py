from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
import os
from django.conf import settings

dictionary = open(os.path.join(settings.BASE_DIR, 'wordlist.txt'))

def home(request):
	return render(request, 'home.html')

def checked(request):
    if request.method == "POST":
        this_File = request.FILES['this_file'].read() # get the uploaded file
        thisFile = this_File.decode("utf-8")
        dictionary = 'wordlist.txt'

        d = []
        with open(dictionary) as f:
        	for word in f:
        		word = word[:-1]
        		word = word.lower()
        		d.append(word)
        words_list = []

        	#g = g.read() 
        line = thisFile.split(" ")

        capital_words = []
        for l in line:
        	first_char = (l[0])
        	if first_char.isupper():
        		l = l.lower()
        		capital_words.append(l)
        	words_list.append(l)

        count = 0
        lwos = []

        for w in words_list:
        	if w[len(w)-1] == ".":
        		this_word = words_list[count]
        		words_list[count] = this_word[:-1]
        		lwos.append(words_list[count])
        		count = count+1
        	else:
        		count = count+1
        def neither_in(a,b,c):
        	e = b+c
        	if(a not in e):
        		return True
        	else:
        		return False
        neither = []
        for n in words_list:
        	if n in d:
        		if neither_in(n, lwos, capital_words):
        			neither.append(n),
        		if(n in capital_words):
        			n = n.capitalize()
        			print(n)
        		if(n in lwos):
        			print(n+"."),
        	else:
        		print(n+"(Mispelled)"),

        template = loader.get_template('checked.html')
        context = {
        	'n': n,
        	'words_list': words_list,
        	'd':d,
        	'lwos':lwos,
        	'capital_words':capital_words,
        	'neither':neither,
        }
        return HttpResponse(template.render(context, request))

    else:
    	return render(request, 'home.html')


