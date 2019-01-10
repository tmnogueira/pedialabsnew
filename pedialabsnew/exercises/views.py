from .models import Lab, Test
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from pagetree.helpers import get_hierarchy
import csv
from io import StringIO
from django.core.urlresolvers import reverse


def edit_lab(request, id):
    lab = get_object_or_404(Lab, id=id)
    section = lab.pageblock().section
    h = get_hierarchy()
    return render(request, 'exercises/edit_lab.html',
                  dict(lab=lab, section=section,
                       root=h.get_root()))


def delete_test(request, id):
    test = get_object_or_404(Test, id=id)
    if request.method == "POST":
        lab = test.lab
        test.delete()
        return HttpResponseRedirect(
            reverse("edit-lab", args=[lab.id]))
    return HttpResponse("""
<html><body><form action="." method="post">Are you Sure?
<input type="submit" value="Yes, delete it" /></form></body></html>
""")


def reorder_tests(request, id):
    if request.method != "POST":
        return HttpResponse("only use POST for this")
    lab = get_object_or_404(Lab, id=id)
    keys = list(request.GET.keys())
    keys.sort()
    tests = [int(request.GET[k]) for k in keys if k.startswith('test_')]
    lab.update_tests_order(tests)
    return HttpResponse("ok")


def add_test_to_lab(request, id):
    lab = get_object_or_404(Lab, id=id)
    form = lab.add_test_form(request.POST)
    if form.is_valid():
        test = form.save(commit=False)
        test.lab = lab
        test.ordinality = lab.test_set.count() + 1
        test.save()
    return HttpResponseRedirect(reverse("edit-lab",
                                        args=[lab.id]))


def add_csv_to_lab(request, id):
    lab = get_object_or_404(Lab, id=id)
    if 'csv' in request.FILES:
        if request.POST.get('replace', None):
            for t in lab.test_set.all():
                t.delete()
        csv_data = request.FILES["csv"].read().strip()
        # normalize to unix line endings
        csv_data = csv_data.replace('\r\n', '\n').replace('\r', '\n')
        s = StringIO()
        s.write(csv_data)
        s.seek(0)
        r = csv.reader(s)
        ordinality = lab.test_set.count() + 1
        for (name, result, normal_range, unit, result_level, abnormality) in r:
            t = Test.objects.create(lab=lab, name=name,
                                    result=result,
                                    normal_range=normal_range,
                                    unit=unit, result_level=result_level,
                                    abnormality=abnormality,
                                    ordinality=ordinality,
                                    )
            ordinality += 1

    return HttpResponseRedirect(reverse("edit-lab", args=[lab.id]))


def edit_test(request, id):
    test = get_object_or_404(Test, id=id)
    if request.method == "POST":
        form = test.edit_form(request.POST)
        if form.is_valid():
            test = form.save()
            test.save()
        return HttpResponseRedirect(reverse("edit-test", args=[test.id]))
    return render(request, 'exercises/edit_test.html', dict(test=test))
