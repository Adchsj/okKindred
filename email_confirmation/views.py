from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation

from axes.attempts import is_already_locked
from  axes.signals import log_user_login_failed

from email_confirmation.models import EmailConfirmation
from custom_user.models import User
from family_tree.decorators import same_family_required

@login_required
@same_family_required
def invite_person(request, person_id = 0, person = None):
    '''
    Creates an invite to join
    '''
    if request.method != 'POST':
        raise Http404

    #ensure user does not already exist
    if person.user_id:
        raise Http404

    #Ensure that an email address exists
    if not person.email:
        raise Http404

    #Check a pending invite does not already exist to the email address
    try:
        pending_invite = EmailConfirmation.objects.get(person_id = person_id)
    except:
        pending_invite = None

    if pending_invite and pending_invite.email_address == person.email:
        raise Http404

    elif pending_invite:
        #Delete pending invite if email has changed
        pending_invite.delete()

    #create a new invite
    EmailConfirmation.objects.create(email_address=person.email,person_id=person_id,user_who_invited_person=request.user)
    return HttpResponseRedirect('/profile={0}/'.format(person_id))


def confirm_invite(request, confirmation_key):
    '''
    View that confirms an email invite and allows the user to choose a password
    '''

    #Check ip has not been locked
    if is_already_locked(request):
        raise Http404

    try:
        invite = EmailConfirmation.objects.get(confirmation_key=confirmation_key)

    except:
        log_user_login_failed(confirm_invite, {'username': confirmation_key}, request)

        return invalid_expired(request)

    if request.method != 'POST':

        #Ensure user is logged out
        auth.logout(request)

        language = invite.person.language
        translation.activate(language)

        return render(request, 'email_confirmation/confirm_invite.html' ,{
                                    'invite' : invite,
                                    'person' : invite.person,
                                    'user_who_invited_person' : invite.user_who_invited_person,
                                })

    else:
        return confirm_invite_post(request, invite)


def confirm_invite_post(request, invite):
    '''
    Handles the confirmation of invite and :
    1. Creates a user correctly
    2. Assigns the user to a person
    3. Deletes the invite
    4. Logs in and displays home page
    '''
    password = request.POST.get("password")

    #Invalid password should be checked bu UI
    if len(password) < 8:
        raise Http404

    #Do all the checks
    if invite.person.family is None:
        raise Http404
    if invite.person.language is None:
        raise Http404
    if invite.email_address != invite.person.email:
        raise Http404
    if invite.email_address is None:
        raise Http404


    user = User.objects.create_user(email=invite.email_address, password=password, name=invite.person.name, family_id=invite.person.family_id, language=invite.person.language)
    invite.person.user_id = user.id
    invite.person.save()
    invite.delete()

    user = auth.authenticate(username=user.email, password=password, request=request)
    auth.login(request, user)
    return HttpResponseRedirect('/')


def invalid_expired(request):
    '''
    Shows invalid or expired confirmation
    '''
    return render(request, 'email_confirmation/invalid_expired.html')


