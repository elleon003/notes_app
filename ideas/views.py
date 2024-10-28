from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Idea, Category, Tag
from .forms import IdeaForm, CategoryForm, TagForm


# Category views
@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'ideas/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            try:
                category.save()
                messages.success(request, 'Category created successfully!')
                return redirect('category_list')
            except IntegrityError:
                messages.error(request, 'A category with this name already exists.')
    else:
        form = CategoryForm()
    return render(request, 'ideas/category_form.html', {'form': form})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Category updated successfully!')
                return redirect('category_list')
            except IntegrityError:
                messages.error(request, 'A category with this name already exists.')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'ideas/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'ideas/category_confirm_delete.html', {'category': category})

@login_required
def category_ideas(request, slug):
    category = get_object_or_404(Category, slug=slug, user=request.user)
    ideas = Idea.objects.filter(user=request.user, category=category)
    return render(request, 'ideas/category_ideas.html', {
        'category': category,
        'ideas': ideas
    })


# Tag views
@login_required
def tag_list(request):
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'ideas/tag_list.html', {'tags': tags})

@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            try:
                tag.save()
                messages.success(request, 'Tag created successfully!')
                return redirect('tag_list')
            except IntegrityError:
                messages.error(request, 'A tag with this name already exists.')
    else:
        form = TagForm()
    return render(request, 'ideas/tag_form.html', {'form': form})

@login_required
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Tag updated successfully!')
                return redirect('tag_list')
            except IntegrityError:
                messages.error(request, 'A tag with this name already exists.')
                print("Message added:", list(messages.get_messages(request)))
    else:
        form = TagForm(instance=tag)
    return render(request, 'ideas/tag_form.html', {'form': form})

@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk, user=request.user)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
        return redirect('tag_list')
    return render(request, 'ideas/tag_confirm_delete.html', {'tag': tag})

@login_required
def tag_ideas(request, slug):
    tag = get_object_or_404(Tag, slug=slug, user=request.user)
    ideas = Idea.objects.filter(user=request.user, tags=tag)
    return render(request, 'ideas/tag_ideas.html', {
        'tag': tag,
        'ideas': ideas
    })


# Idea views
@login_required
def idea_list(request):
    ideas = Idea.objects.filter(user=request.user)
    return render(request, 'ideas/idea_list.html', {'ideas': ideas})


@login_required
def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk, user=request.user)
    return render(request, 'ideas/idea_detail.html', {'idea': idea})


@login_required
def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, user=request.user)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()
            form.save_m2m() # Save many-to-many relationships
            messages.success(request, 'Idea created successfully!')
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(user=request.user)
    return render(request, 'ideas/idea_form.html', {'form': form})


@login_required
def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IdeaForm(request.POST, instance=idea, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Idea updated successfully!')
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea, user=request.user)
    return render(request, 'ideas/idea_form.html', {'form': form})


@login_required
def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk, user=request.user)
    if request.method == 'POST':
        idea.delete()
        messages.success(request, 'Idea deleted successfully!')
        return redirect('idea_list')
    return render(request, 'ideas/idea_confirm_delete.html', {'idea': idea})
