from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
import os
from django.conf import settings

#define the txt file we're using as our wordlist as "dictionary"
dictionary = open(os.path.join(settings.BASE_DIR, 'wordlist.txt'))

#landing page server
def home(request):
	return render(request, 'home.html')

#spellchecked page server
def checked(request):
    if request.method == "POST":
        this_File = request.FILES['this_file'].read() # get our file that user uploaded
        thisFile = this_File.decode("utf-8")
        dictionary = 'wordlist.txt'

        d = [] #empty list of words to be later used as dictionary
        with open(dictionary) as f:
        	for word in f:
        		word = word[:-1] #format words
        		word = word.lower()
        		d.append(word) #add all words from wordlist file to dictionary

        #add these to dict so they don't come up as mispelled
        endlines = ["\n", "\t", '', "\n\n", "\n\n\n"]
        symbols = [".", "?", "_", "-", "!", "+", "=", "(", ")", "[", "]", ":", ";", "..."]

        for line in endlines:
        	d.append(line)
        for symbol in symbols:
        	d.append(symbol)

        words_list = [] #This is the empty list of words from the file user uploaded

        temp_list = thisFile.split(" ") #create a list of users words

        #check for capitals so we can check if base word is mispelled
        for l in temp_list:
        	if l.istitle():
        		lower_case = l.lower()
        		if lower_case in d:
        			d.append(l)
        		else:
        			pass
        	words_list.append(l)

        #check if words contain endlines or symbols so we can check if base word is mispelled
        for w in words_list:
        	char_count = 0
        	base_word = "zxzxxxx"
        	for char in w:
        		if char in symbols or char in endlines:
        			base_word = w[:-char_count]
        			char_count = char_count + 1
        		else:
        			char_count = char_count + 1
        	if base_word in d:
        		d.append(w)
        	else:
        		pass

        for n in words_list: #compare our user wordlist with our dictionary
        	if n in d:
        		print(n+" "),
        	else:
        		print(n+"(Mispelled)"),

        template = loader.get_template('checked.html')
        context = {
        	'n': n,
        	'words_list': words_list,
        	'd':d,
        }
        return HttpResponse(template.render(context, request))

    else:
    	return render(request, 'home.html')


