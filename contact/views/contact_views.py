from django.shortcuts import render, get_object_or_404, redirect
from contact.models import Contact
from django.db.models import Q

# Create your views here.

def index(request):

    contacts = Contact.objects.all()

    context = {
        'contacts' : contacts,
    }

    return render(
        request,
        'contact/index.html',
        context,
    )


def search(request):
    search_value = request.GET.get('q', '').strip()

    if search_value == '':
        return redirect('contact:index')

    contacts = (Contact.objects
    .filter(show=True)
    .filter(Q(first_name__icontains=search_value) | 
            Q(last_name__icontains=search_value) |
            Q(email__icontains=search_value) |
            Q(phone__icontains=search_value)
            )
        )


    context = {
        'contacts' : contacts,
        'web_title' : 'Search - ',
        'search_value' : search_value,
    }

    return render(
        request,
        'contact/index.html',
        context,
    )

def contact(request, contact_id):

    single_contact = get_object_or_404(Contact, pk=contact_id)

    web_title = f'{single_contact.first_name} {single_contact.last_name} -'
 
    context = {
        'contact' : single_contact,
        'web_title' : web_title,
    }

    return render(
        request,
        'contact/contact.html',
        context,
    )