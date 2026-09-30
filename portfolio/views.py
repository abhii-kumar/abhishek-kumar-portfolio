import json, math
from pathlib import Path
from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import ContactForm
from .models import Pulse

def home(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Thanks! Your message has been saved for the portfolio owner.')
        return redirect('/#contact')
    return render(request, 'index.html', {'form': form, 'projects': json.loads((Path(__file__).parent / 'content.json').read_text())})

@require_http_methods(['GET','POST'])
def pulses(request):
    cutoff = timezone.now() - timedelta(seconds=8)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            x,y = float(data['x']),float(data['y'])
            if not all(math.isfinite(v) and 0 <= v <= 1 for v in [x,y]): raise ValueError()
        except (ValueError,KeyError,TypeError): return JsonResponse({'error':'Invalid coordinates'}, status=400)
        last = request.session.get('last_pulse', 0)
        now = timezone.now().timestamp()
        if now-last < 0.25: return JsonResponse({'error':'Please slow down'},status=429)
        request.session['last_pulse'] = now
        Pulse.objects.create(x=x,y=y)
        Pulse.objects.filter(created__lt=cutoff).delete()
    return JsonResponse({'pulses':list(Pulse.objects.filter(created__gte=cutoff).order_by('-id').values('id','x','y')[:80])})
