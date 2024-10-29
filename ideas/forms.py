from django import forms
from .models import Idea, Category, Tag


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-white dark:bg-slate-700 text-slate-900 dark:text-white'})
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-white dark:bg-slate-700 text-slate-900 dark:text-white'})
        }


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['content', 'side_notes', 'start_date', 'due_date', 'category', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-white dark:bg-slate-700 text-slate-900 dark:text-white'}),
            'side_notes': forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-white dark:bg-slate-700 text-slate-900 dark:text-white'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-white dark:bg-slate-700 text-slate-900 dark:text-white'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-white dark:bg-slate-700 text-slate-900 dark:text-white'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-white dark:bg-slate-700 text-slate-900 dark:text-white'}),
            'tags': forms.SelectMultiple(attrs={'class': 'w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent bg-white dark:bg-slate-700 text-slate-900 dark:text-white'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(IdeaForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
            self.fields['tags'].queryset = Tag.objects.filter(user=user)
