from django.shortcuts import render, redirect

from todo.models import ToDoItem


def index(request):
    items = ToDoItem.objects.order_by('-text') #.order_by('-created_on')
    context = {'items': items}
    return render(request, 'todo/index.html', context)


def create(request):
    item = ToDoItem(text=request.POST["text"])
    item.completed = False
    item.save()
    return redirect("todo:list")


def delete(request):
    ToDoItem.objects.filter(pk=request.POST["id"]).delete()
    return redirect("todo:list")


def update(request):
    item = ToDoItem.objects.get(pk=request.POST["id"])
    item.completed = request.POST.get("completed") == 'on'
    item.text = request.POST["text"]
    item.save()
    return redirect("todo:list")

