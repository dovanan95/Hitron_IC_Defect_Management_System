from django.shortcuts import render
from django.shortcuts import (get_object_or_404, HttpResponseRedirect)
import json
from django.http import HttpResponse
from django.http import JsonResponse
from PE.models import MasterData
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db import connection, transaction
from django.core import serializers
import os
from django.core.files.storage import FileSystemStorage
from PE.form import MasterForm
from django import forms
from .form import MasterForm
from django.db.models import Max
from datetime import date

@csrf_protect
# Create your views here.
def input_data(request):
    master = MasterForm()
    return render(request, 'input_form.html', {'form': master})

@csrf_exempt
def Submit_master(request):
    if(request.POST):
        cusname = request.POST.get('cus_name', None)
        pe = request.POST.get('pe', None)
        pn = request.POST.get('pn', None)
        model = request.POST.get('model', None)
        ICPN = request.POST.get('icpn', None)
        icspec = request.POST.get('icspec_sub', None)
        pnburn = request.POST.get('pnburn_sub', None)
        fwver = request.POST.get ('fwver_sub', None)
        icpos = request.POST.get ('ICPos_sub', None)
        chksum = request.POST.get('chksum_sub', None)
        prog = request.POST.get('program_sub', None)
        dotcolor = request.POST.get('dotcolor_sub', None)
        dot_pos = request.POST.get('dotposition', None)
        #dot_pos = "/media/" + ICPN + ".jpg"
        #dot_pos_file = request.FILES['dotposition']
        date = request.POST.get('date_sub', None)
        fwnote = request.POST.get('fwnote_sub', None)

        arr_item = [cusname, pe, pn, model, ICPN, icspec, pnburn, fwver,
         icpos, chksum, prog, dotcolor, dot_pos, date, fwnote]
        for item_ in arr_item:
            if(item_ == ""):
                item_ = "N/A"


        M = MasterData(Cus_name = cusname, PE = pe, PN = pn, 
        Model = model, ICPN = ICPN, ICSpec = icspec,
        Part_burn = pnburn, FwVer = fwver, ICPos = icpos, 
        CheckSum = chksum, Prog_name = prog, dot_color = dotcolor, 
        dot_pos = dot_pos, Change_date = date, Fw_note = fwnote)
       
        M.save()

    res = MasterData.objects.filter(Cus_name = cusname)
    res_json = serializers.serialize('json', res)
    data = ({'data': res_json})
    return JsonResponse(data)
@csrf_exempt
def Submit_form(request):
    #pass
    if request.method == 'POST':
        form = MasterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            res = ({'response': 'success' })
            #return JsonResponse(res)
            code = request.POST.get('Code', None)
            cusname = request.POST.get('Cus_name', None)
            pe = request.POST.get('PE', None)
            pn = request.POST.get('PN', None)
            model = request.POST.get('Model', None)
            icpn = request.POST.get('ICPN', None)
            icspec = request.POST.get('ICSpec', None)
            pnburn = request.POST.get('Part_burn', None)
            fwv = request.POST.get('FwVer', None)
            icpos = request.POST.get('ICPos', None)
            chksum = request.POST.get('CheckSum', None)
            prog = request.POST.get('Prog_name', None)
            dotcol = request.POST.get('dot_color', None)
            dotpos = request.POST.get('dot_pos', None)
            date = request.POST.get('Change_date', None)
            fwnote = request.POST.get('Fw_note', None)

            res = MasterData.objects.filter(Code = code, Cus_name = cusname, PE = pe, PN = pn, Model = model,
                                            ICPN = icpn, ICSpec = icspec, Part_burn = pnburn,
                                            FwVer = fwv, ICPos = icpos, CheckSum = chksum,
                                            Prog_name = prog, dot_color = dotcol, Fw_note = fwnote)
            #res_json = serializers.serialize('json', res)
            return render(request, 'submit_result.html', {'res': res})
    else:
        form = MasterForm()
    return render(request, 'input_form.html', {'form': form})

@csrf_exempt
def Update_Confirm(request, code):
    context = {}
    obj = get_object_or_404(MasterData, Code = code)
    form = MasterForm(request.POST or None, instance= obj)
    if request.method == 'POST':
        form_post = MasterForm(request.POST, request.FILES)
        if form_post.is_valid():
            MasterData.objects.filter(Code = code).delete()
            form_post.save()
            return HttpResponseRedirect('/detail/' + code)
    context['form'] = form
    return render(request, 'Update.html', context)

@csrf_exempt
def NoneImageUpdate(request, code):
    context = {}
    obj = get_object_or_404(MasterData, Code = code)
    form = MasterForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/detail/' + code)
    context['form'] = form
    return render(request, 'Update.html', context)

@csrf_exempt
def DetailForm(request, code):
    context = {}
    context['res'] = MasterData.objects.filter(Code = code)
    return render(request, 'submit_result.html', context)


@csrf_exempt
def Trace_Data(request):
    return render(request, 'Trace.html')

@csrf_exempt
def code_render(request):
    return render(request, 'Code_trace.html')

@csrf_exempt
def Query(request):
    if request.method == 'POST':
        pn = request.POST.get('pn', None)
        model = request.POST.get('model', None)

        if pn == "" and model != "":
            data = MasterData.objects.filter(Model = model)
            out = serializers.serialize('json', data)
            data_out = ({'dtout': out})
            return JsonResponse(data_out, safe=False)
        elif model == "" and pn != "":
            data = MasterData.objects.filter(PN = pn)
            out = serializers.serialize('json',data)
            data_out = ({'dtout': out})
            return JsonResponse(data_out, safe=False)
        else:
            data = MasterData.objects.filter(PN = pn, Model = model)
            out = serializers.serialize('json',data)
            data_out = ({'dtout': out})
            return JsonResponse(data_out, safe=False)

@csrf_exempt
def GetCode(request):
    if request.method == 'GET':
        csr = connection.cursor()
        csr.execute("select max(code)  from icpe_defect.pe_masterdata")
        row = csr.fetchone()

        date_str = date.today()
        date_code = date_str.strftime('%Y%m%d')
        prefix = "000"
        
        if row:
            if str(row)[2:10] == date_code:
                index = int(str(row)[10:14])
                if index < 9:
                    res = date_code + prefix + str(index + 1)
                elif index >=9 and index <99:
                    res = date_code + "00" + str(index +1)
                elif  index >= 99 and index <999:
                    res = date_code + "0" + str(index +1)
                else:
                    res = date_code + str(index +1)

            elif str(row)[2:10] != date_code:
                res = date_code + prefix + "1"
        else:
             res = date_code + prefix + "1"
            

        return HttpResponse(res)

@csrf_exempt
def TrackingCode(request):
    if request.method == 'POST':
        code_req = request.POST.get('code', None)
        data = MasterData.objects.filter(Code = code_req)
        out = serializers.serialize('json', data)
        data_out = ({'dtout': out})
        return JsonResponse(data_out, safe=False)
        






