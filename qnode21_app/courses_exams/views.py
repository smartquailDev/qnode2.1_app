from django.shortcuts import render, get_object_or_404
from .models import SubjectTest, Test, Instrucciones
from card_test.forms import CartAddTestForm


def instruc(request):
    intruciones=Instrucciones.objects.all()
    return render(request,
                  'courses_exams/instructions.html',
                  {'intruciones': intruciones})


def test_list(request, subject_test_slug=None):
    subject_test = None
    subject_tests= SubjectTest.objects.all()
    tests = Test.objects.filter(available=True)
    if subject_test_slug:
        subject_test = get_object_or_404(SubjectTest, slug=subject_test_slug)
        tests = tests.filter(subject_test=subject_test)
    return render(request,
                  'courses_exams/list.html',
                  {'subject_test': subject_test,
                   'subject_tests': subject_tests,
                   'tests': tests})


def test_detail(request, id, slug):
    test = get_object_or_404(Test,
                                id=id,
                                slug=slug,
                                available=True)
    cart_test_form = CartAddTestForm()
    return render(request,
                  'courses_exams/detail.html',
                  {'test': test,
                   'cart_test_form': cart_test_form})
