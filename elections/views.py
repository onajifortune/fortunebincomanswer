# Create your views here.
from datetime import datetime
from sqlite3 import IntegrityError

from django.shortcuts import HttpResponse, get_object_or_404, render

from .models import AnnouncedPuResults, Lga, Party, PollingUnit


def list_polling_units(request):
    polling_units = PollingUnit.objects.all()
    context = {
        'polling_units': polling_units
    }
    return render(request, 'polling_units.html', context)



def retrieve_polling_unit(request, uniqueid):
    unit = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=str(uniqueid))
    poll_unit = get_object_or_404(PollingUnit, uniqueid=uniqueid)
    return render(request, 'each_polling_unit.html', { 'poll_unit':poll_unit, 'unit': unit })



def local_government(request):
    lg = Lga.objects.all()
    if request.method == 'POST':
        try:
            num = request.POST['choice']
            lgfind = Lga.objects.get(lga_id=int(num))
        except:
            return render(request, 'local_govt_results.html', { 'lg': lg})
        local_gov_name = lgfind.lga_name
        pu = PollingUnit.objects.filter(lga_id=lgfind.lga_id)
        results = []
        errs = []
        pairs = {}
        print(len(pu))
        for i in pu:
            result = AnnouncedPuResults.objects.filter(polling_unit_uniqueid=i.uniqueid)
            if result:
                for r in result:
                    if r:
                        results.append(r)
                    else:
                        errs.append("These results aren't available")
        print(len(results))
        
        pdp_sum = []
        dpp_sum = []
        acn_sum = []
        ppa_sum = []
        cdc_sum = []
        jp_sum = []
        labo_sum = []
        anpp_sum = []
        cpp_sum = []

        for i in results:
            if i.party_abbreviation == 'PDP':
                pdp_sum.append(i.party_score)
                pdp = sum(pdp_sum)
                pairs['pdp'] = pdp

            if i.party_abbreviation == 'DPP':
                dpp_sum.append(i.party_score)
                dpp = sum(dpp_sum)
                pairs['dpp'] = dpp

            if i.party_abbreviation == 'ACN':
                acn_sum.append(i.party_score)
                acn = sum(acn_sum)
                pairs['acn'] = acn

            if i.party_abbreviation == 'PPA':
                ppa_sum.append(i.party_score)
                ppa = sum(ppa_sum)
                pairs['ppa'] = ppa

            if i.party_abbreviation == 'CDC':
                cdc_sum.append(i.party_score)
                cdc = sum(cdc_sum)
                pairs['cdc'] = cdc

            if i.party_abbreviation == 'JP':
                jp_sum.append(i.party_score)
                jp = sum(jp_sum)
                pairs['jp'] = jp

            if i.party_abbreviation == 'LABO':
                labo_sum.append(i.party_score)
                labo = sum(labo_sum)
                pairs['labo'] = labo

            if i.party_abbreviation == 'ANPP':
                anpp_sum.append(i.party_score)
                anpp = sum(anpp_sum)
                pairs['anpp'] = anpp

            if i.party_abbreviation == 'CPP':
                cpp_sum.append(i.party_score)
                cpp = sum(cpp_sum)
                pairs['cpp'] = cpp

        if len(results) == 0:
            return render(request, 'local_govt_results.html', {'local_gov_name': local_gov_name, "message": "This local government has no polls"})

        return render(request, 'local_govt_results.html', { 'local_gov_name': local_gov_name, 'pairs': pairs})
    
    return render(request, 'local_govt_results.html', { 'lg': lg})


def result_for_new_polling_unit(request):
    parties = Party.objects.all()
    polling_unit_names = PollingUnit.objects.all()
    polls_unit_names = []
    admin = "ADMIN"
    for pu in polling_unit_names:
        if pu.polling_unit_id != 0:
            polls_unit_names.append(pu)
    if request.method == 'POST':
        pu_uniqueid = request.POST['choice']

        for p in parties:
            pname = p.partyname
            print(pname)
            result = request.POST[pname.lower()]
            if pname=='LABOUR':
                pname = 'LABO'
            if result == '0':
                print('yeah')
                continue
            try:
                new_result = AnnouncedPuResults.objects.create(polling_unit_uniqueid=str(int(pu_uniqueid)), party_abbreviation=pname, party_score=result , entered_by_user=admin, date_entered=datetime.now())
                new_result.save()
            except (ValueError, TypeError, IntegrityError, Exception) as er:
                message = 'The Polling Unit or Party vote count is invalid!'
                return render(request, 'add_results.html', {"message": message , 'parties': parties, 'polling_unit_names': polls_unit_names })
        return render(request,'add_results.html',{'message': 'Successful!', 'parties': parties, 'polling_unit_names': polls_unit_names})

    return render(request, 'add_results.html', { 'parties': parties, 'polling_unit_names': polls_unit_names })