#coding:utf-8
from django.shortcuts import render,redirect, resolve_url
from todolist.models import Item
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage

# Create your views here.
def index(request):
    try:
        item_list = Item.objects.all().order_by("-pub_date")
        paginator = Paginator(item_list, 6)
        try:
            page = int(request.GET.get("page",1))
            item_list = paginator.page(page)
        except (PageNotAnInteger, InvalidPage, EmptyPage):
            item_list = paginator.page(1)
    except Exception as e:
        print(e)
    return render(request, "index.html", locals())

def add(request):
    try:
        content = request.GET.get("item", None)
        if len(content) > 0:
            obj = Item.objects.create(content=content)
            if obj:
                return redirect(resolve_url("index"))
    except Exception as e:
        print(e)
    return render(request, "message.html", {"message": u"待办事项添加失败"})

def edit(request):
    try:
        item_id = request.GET.get("item_id", None)
        content = request.GET.get("item", None)
        if len(item_id) > 0 and len(content) > 0:
            obj = Item.objects.get(pk=item_id)
            obj.content = content
            obj.save()
        return redirect(resolve_url("index"))
    except Exception as e:
        print(e)
    return render(request, "message.html", {"message": u"待办事项修改失败"})

def delete(request):
    try:
        item_id = request.GET.get("item_id", None)
        if len(item_id) > 0:
            obj = Item.objects.get(pk=item_id)
            obj.delete()
        return redirect(resolve_url("index"))
    except Exception as e:
        print(e)
    return render(request, "message.html", {"message": u"待办事项删除失败"})

def done(request):
    try:
        item_id = request.GET.get("item_id", None)
        if len(item_id) > 0:
            obj = Item.objects.get(pk=item_id)
            obj.is_done = False if obj.is_done else True
            obj.save()
        return redirect(resolve_url("index"))
    except Exception as e:
        print(e)
    return render(request, "message.html", {"message": u"待办事项状态修改失败"})