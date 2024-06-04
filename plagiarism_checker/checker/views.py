from django.shortcuts import render, get_object_or_404
from .models import Document
from .forms import DocumentForm
from django.shortcuts import render, redirect
import spacy

nlp = spacy.load("en_core_web_sm")

def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the plagiarism check page
            return redirect('check_plagiarism')
    else:
        form = DocumentForm()
    return render(request, 'checker/index.html', {'form': form})

def compare_documents(doc1, doc2):
    doc1_nlp = nlp(doc1.content)
    doc2_nlp = nlp(doc2.content)
    return doc1_nlp.similarity(doc2_nlp)

def check_plagiarism(request):
    documents = Document.objects.all()
    if len(documents) < 2:
        return render(request, 'checker/plagiarism.html', {'message': 'Not enough documents to compare.'})
    
    results = []
    for i in range(len(documents)):
        for j in range(i + 1, len(documents)):
            similarity = compare_documents(documents[i], documents[j])
            results.append({
                'doc1': documents[i].title,
                'doc2': documents[j].title,
                'similarity': similarity,
            })
    return render(request, 'checker/plagiarism.html', {'results': results})
