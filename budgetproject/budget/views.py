from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Project, Category, Expense
from django.views.generic import CreateView
from django.utils.text import slugify
from .form import ExpenseForm
import json

# Create your views here.

def project_list(request):
    project_list = Project.objects.all()

    return render(request, 'budget/project_list.html', { 'projects':project_list})


def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug = project_slug)
    if request.method == "GET":
        expense_list = project.expenses.all()
        categoryList = Category.objects.filter(project = project)
        return render(request, 'budget/project_detail.html', {'project':project, 'expense_list':expense_list, 'categoryList':categoryList})
    elif request.method == "POST":
        #validate form
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            category = get_object_or_404(Category, project = project, name = category_name)

            Expense.objects.create(
                project = project,
                title = title, 
                amount = amount,
                category = category
            ).save()
    elif request.method == "DELETE":
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id = id)
        expense.delete()
        return HttpResponseRedirect(project_slug)

    return HttpResponseRedirect(project_slug)

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'budget/add-project.html'
    fields = ('name', 'budget')

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for cat in categories:
            Category.objects.create(
                project = Project.objects.get(id = self.object.id),
                name = cat
            ).save()
        return HttpResponseRedirect(self.get_success_url(categories))
    
    def get_success_url(self, c):
        print(c)
        return slugify(self.request.POST['name'])
