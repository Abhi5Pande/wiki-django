
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
import random
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", required=True, widget= forms.TextInput(attrs={"class":"form-control"}),)
    content = forms.CharField(label="content",required=True,widget = forms.Textarea(attrs = {"class":"form-control"}),)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request,title):
    content = util.get_entry(title)
    return render(request, "encyclopedia/page.html", {
        "content": Markdown().convert(content) ,
        "title":title
        })

def edit(request,entry):
    if request.method== "GET":
        title = entry
        content = util.get_entry(title)
        form = NewPageForm({"title":title,"content":content})
        return render(request,"encyclopedia/edit.html",{
            "form":form,
            "title":title
    })
    form = NewPageForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("encyclopedia:title",args=[title]))

def add(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            return render(request,"encyclopedia/add.html",{
                "form": form
            })
    return render(request,"encyclopedia/add.html",{
        "form": NewPageForm()
    })

def random(request):
    entries = util.list_entries()
    rand_entry = random.choice(entries)
    #return redirect("encyclopedia:title",rand_entry)
    return HttpResponse(rand_entry)
    
def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    if query is None or query == "":
        return render(request,"encyclopedia/index.html")
    else:
        if query in entries:
            return redirect("encyclopedia:title",query)
        found_entries = [
            valid_entries
            for valid_entries in entries
            if query.lower() in valid_entries.lower()
        ]
        return render(request, "encyclopedia/search.html",{
            "query": query,
            "found_entries":found_entries
        })
        


    



