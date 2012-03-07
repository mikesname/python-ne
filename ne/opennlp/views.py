# Create your views here.

import json
import os
import re
import subprocess as sp
import tempfile

from django.shortcuts import render
from django.http import HttpResponse

from . import forms

OPENNLP = "/opt/opennlp"
JAVA_HOME = "/usr/lib/jvm/java-6-sun/jre"
ENTITYRE = re.compile("<START:(?P<type>\w+)>\s*(?P<payload>[^<]+?)\s*<END>")


def get_opennlp_command(entities):
    entlist = ["%s/data/namefind/en-ner-%s.bin" % (OPENNLP, ent) for ent in entities]
    return ["%s/bin/opennlp" % OPENNLP, "TokenNameFinder"] + entlist


def extract_entity_text(text, entities):
    cmd = get_opennlp_command(entities)
    os.environ["JAVA_HOME"] = JAVA_HOME
    proc = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE)
    proc.stdin.write(text.encode("utf8"))
    proc.stdin.flush()
    return proc.communicate()[0]


def extract_entity_data(text, entities):
    text = extract_entity_text(text, entities)
    data = {}
    for type, payload in ENTITYRE.findall(text):
        print type, payload
        vals = data.get(type)
        if vals is None:
            data[type] = []
        data[type] = list(set(data[type]) | set([payload]))
    return data


def home(request):
    template = "home.html"
    form = forms.OpenNLPForm()
    context = dict(form=form)
    if request.method == "POST":
        form = forms.OpenNLPForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data["text"]
            entities = form.cleaned_data["entity"]
            data = extract_entity_data(text, entities)
            return HttpResponse(json.dumps(data), mimetype="application/json")
        context.update(form=form)
    return render(request, template, context)
