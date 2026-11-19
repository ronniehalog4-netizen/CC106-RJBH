from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import student


def student_registration(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record created successfully.')
            return redirect('registration_success')
    else:
        form = StudentForm()
    return render(request, 'registration/student_registration.html', {'form': form})

def registration_success(request):
    return render(request, 'registration/success.html')


def student_list(request):
    query = request.GET.get('q', '').strip()
    students = student.objects.all().order_by('last_name', 'first_name')
    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
    return render(
        request,
        'registration/student_list.html',
        {'students': students, 'query': query},
    )


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record created successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(
        request,
        'registration/student_form.html',
        {'form': form, 'page_title': 'Register Student'},
    )


def student_detail(request, pk):
    student_record = get_object_or_404(student, pk=pk)
    return render(
        request,
        'registration/student_detail.html',
        {'student': student_record},
    )


def student_update(request, pk):
    student_record = get_object_or_404(student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record updated successfully.')
            return redirect('student_detail', pk=student_record.pk)
    else:
        form = StudentForm(instance=student_record)
    return render(
        request,
        'registration/student_form.html',
        {
            'form': form,
            'page_title': 'Update Student',
            'student': student_record,
        },
    )


def student_delete(request, pk):
    student_record = get_object_or_404(student, pk=pk)
    if request.method == 'POST':
        student_record.delete()
        messages.success(request, 'Student record deleted successfully.')
        return redirect('student_list')
    return render(
        request,
        'registration/student_confirm_delete.html',
        {'student': student_record},
    )
