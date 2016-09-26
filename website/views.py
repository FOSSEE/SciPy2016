# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.admin.models import CHANGE
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import F
import csv
from django.core.mail import EmailMultiAlternatives


from website.forms import ProposalForm, UserRegisterForm, UserLoginForm, WorkshopForm, ContactForm
from website.models import Proposal, Comments
from social.apps.django_app.default.models import UserSocialAuth
import random
import string


def userregister(request):
    context = {}
    context.update(csrf(request))
    registered_emails = []
    users = User.objects.all()
    for user in users:
        registered_emails.append(user.email)
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if data['email'] in registered_emails:
                    context['form'] = form
                    context['email_registered'] = True
                    return render_to_response('user-register.html', context)
                else:
                    form.save()
                    context['registration_complete'] = True
                    # form = UserLoginForm()
                    # context['form'] = form
                    return render_to_response('cfp.html', context)
            else:
                context.update(csrf(request))
                context['form'] = form
                return render_to_response('user-register.html', context)
        else:
            form = UserRegisterForm()
        context.update(csrf(request))
        context['form'] = form
        return render_to_response('user-register.html', context)
    else:
        context['user'] = request.user
        return render_to_response('cfp.html', context)

def contact_us(request,next_url):
    pass
    context = {}
    if request.method == "POST":
        form = ContactForm(request.POST)
        sender_name = request.POST['name']
        sender_email = request.POST['email']
        to = ('scipy@fossee.in',)
        subject = "Query from - "+sender_name
        message = request.POST['message']
        try:
            send_mail(subject, message, sender_email, to)
            context['mailsent'] = True
            context['user'] = user
        except:
            context['mailfailed'] = True
            context['user'] = user
    return redirect(next_url,context)


def home(request):
    #pass
    context = {}
    user = request.user
    context.update(csrf(request))
    if request.method == "POST":
        sender_name = request.POST['name']
        sender_email = request.POST['email']
        to = ('scipy@fossee.in',)
        subject = "Query from - "+sender_name
        message = request.POST['message']
        try:
            send_mail(subject, message, sender_email, to)
            context['mailsent'] = True
            if user.is_authenticated():
                context['user'] = user
        except:
            context['mailfailed'] = True
            if user.is_authenticated():
                context['user'] = user
    return render_to_response('base.html', context)


def cfp(request):
    if request.method == "POST":
        context = {}
        context.update(csrf(request))
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                next = request.GET['next']
                return HttpResponseRedirect(next)
            proposals = Proposal.objects.filter(user = request.user).count()
            context['user'] = user
            context['proposals'] = proposals
            return render_to_response('cfp.html', context)
        else:
            context['invalid'] = True
            context['form'] = UserLoginForm
            context['user'] = user
            return render_to_response('cfp.html', context)
    else:
        form = UserLoginForm()
        context = RequestContext(request, {'request': request,
                                           'user': request.user,
                                           'form': form})
        context.update(csrf(request))
        return render_to_response('cfp.html',
                             context_instance=context)


def submitcfp(request):
    context = {}
    if request.user.is_authenticated():
        social_user = request.user
        context.update(csrf(request))
        django_user = User.objects.get(username=social_user)
        context['user'] = django_user
        proposals_a = Proposal.objects.filter(user = request.user, proposal_type = 'ABSTRACT').count()
        if request.method == 'POST':
            form = ProposalForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = django_user
                data.save()
                context['proposal_submit'] = True
                sender_name = "SciPy India 2016"
                sender_email = "scipy@fossee.in"
                subject = "SciPy India - Proposal Submission Acknowledgment"
                to = (social_user.email, )
                message = """Dear """+django_user.first_name+""",\n\nThank you for showing interest & submitting a talk/workshop at SciPy India 2016 conference.We have received your proposal (abstract/workshop description)for the talk/workshop titled  '"""+request.POST['title']+"""'.\nReviewal of the proposals will start once the CFP closes.\nYou will be notified regarding selection/rejection of your talk via email.\n\nThank You ! \n\nRegards,\nSciPy India 2016,\nFOSSEE - IIT Bombay"""
                send_mail(subject, message, sender_email, to)
                return render_to_response('cfp.html', context)
            else:
                context['proposal_form'] =  form
                context['proposals_a'] = proposals_a
                return render_to_response('submit-cfp.html', context)
        else:
            form = ProposalForm()
            context['proposals_a'] = proposals_a 
            context['proposal_form'] = form
        return render_to_response('submit-cfp.html', context) #when link clicked
    else:
        context['login_required'] = True
        return render_to_response('cfp.html', context)

def submitcfw(request):
    context = {}
    if request.user.is_authenticated():
        social_user = request.user
        context.update(csrf(request))
        django_user = User.objects.get(username=social_user)
        context['user'] = django_user
        proposals_w = Proposal.objects.filter(user = request.user, proposal_type = 'WORKSHOP').count()
        if request.method == 'POST':
            form = WorkshopForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = django_user
                data.save()
                context['proposal_submit'] = True
                sender_name = "SciPy India 2016"
                sender_email = "scipy@fossee.in"
                subject = "SciPy India - Proposal Acknowledgment"
                to = (social_user.email, )
                message = """Dear """+django_user.first_name+""",\n\nThank you for showing interest & submitting a talk at SciPy India 2016 conference. We have received your proposal for the talk titled '"""+request.POST['title']+"""'.\nReviewal of the proposals will start once the CFP closes.\nYou will be notified regarding selection/rejection of your talk via email.\n\nThank You ! \n\nRegards,\nSciPy India 2016,\nFOSSEE - IIT Bombay"""
                send_mail(subject, message, sender_email, to)
                return render_to_response('cfp.html', context)
            else:
                context['proposal_form'] =  form
                context['proposals_w'] = proposals_w
                return render_to_response('submit-cfw.html', context)
        else:
            form = WorkshopForm()
            context['proposal_form'] = form
            context['proposals_w'] = proposals_w
        return render_to_response('submit-cfw.html', context)
    else:
        context['login_required'] = True
        return render_to_response('cfp.html', context)


def view_abstracts(request):
    user = request.user
    context = {}
    count_list =[]
    if user.is_authenticated():
        if user.is_superuser :
            proposals = Proposal.objects.all()
            context['proposals'] = proposals
            for proposal in proposals:
                count = Comments.objects.filter(proposal = proposal).count()
                # print "-----------count ", count
                count_list.append(count)
            print "-----------count ", count_list
            context['counts'] = count_list
            context['user'] = user
            return render(request, 'view-abstracts.html', context)
        elif user is not None:
            if Proposal.objects.filter(user = user).exists :
                proposals = Proposal.objects.filter(user = user)
                print "-----------count ", count_list
                context['counts'] = count_list
                context['proposals'] = proposals
                context['user'] = user
            return render(request, 'view-abstracts.html', context)
        else:
            return render(request, 'cfp.html')
    else:
        return render(request, 'cfp.html')


def abstract_details(request, proposal_id=None):
    user = request.user
    context = {}
    if user.is_authenticated():
        if user.is_superuser :
            proposals = Proposal.objects.all()
            context['proposals'] = proposals
            context['user'] = user
            return render(request, 'abstract_details.html', context)
        elif user is not None:
            print "---------------------->>>>>>>>>>", proposal_id
            proposal = Proposal.objects.get(id=proposal_id)
            comments = Comments.objects.filter(proposal=proposal)
            context['proposal'] = proposal
            context['user'] = user
            context['comments'] = comments
            return render(request, 'abstract-details.html', context)
        else:
            return render(request, 'cfp.html')
    else:
        return render(request, 'cfp.html')

def rate_proposal(request, proposal_id = None):
    user = request.user
    context = {}
    if user.is_authenticated():
        proposal = Proposal.objects.get(id=proposal_id)
        if request.method == 'POST':
            print"in rating"
            rate = request.POST.get('rating')
            print"rate-------" , rate
            proposal.rate = rate
            proposal.save()
            comments = Comments.objects.filter(proposal=proposal)
            context['proposal'] = proposal
            context['comments'] = comments
            context.update(csrf(request))
            return render(request, 'comment-abstract.html', context)
        else:
            comments = Comments.objects.filter(proposal=proposal)
            context['proposal'] = proposal
            context['comments'] = comments
            context.update(csrf(request))
            return render(request, 'comment-abstract.html', context)
    else:
        return render(request, 'comment-abstract.html', context)




def comment_abstract(request, proposal_id = None):
    user = request.user
    context = {}
    if user.is_authenticated():
        proposal = Proposal.objects.get(id=proposal_id)
        if request.method == 'POST':
            comment = Comments()
            comment.comment = request.POST['comment']
            comment.user = user
            comment.proposal = proposal
            comment.save()
            comments = Comments.objects.filter(proposal=proposal)
            print "proposal", proposal.title
            print "comment", comment.comment
            print "moderator", request.user
            print "proposal poster", proposal.user.email
            sender_name = "SciPy India 2016"
            sender_email = "scipy@fossee.in"
            subject = "SciPy India - Comment on Your Proposal"
            to = (proposal.user.email, )
            message = """
                Dear {0}, <br><br>
                There is a comment posted on your proposal for the talk/workshop titled {1}. 
                Please <a href = “”>login </a>to link and check the comment and do the needful.<br><br>
                Thank You ! <br><br>Regards,<br>SciPy India 2016,<br>FOSSEE - IIT Bombay.
                """.format(
                proposal.user.first_name,
                proposal.title, 
                )
            email = EmailMultiAlternatives(
                subject,'',
                sender_email, to,
                headers={"Content-type":"text/html;charset=iso-8859-1"}
            )
            email.attach_alternative(message, "text/html")
            email.send(fail_silently=True)

            # message = """Dear """+proposal.user.first_name+"""There is a comment posted on your proposal for the talk/workshop titled '"""+ proposal.title +"""'.Please login to link and check the comment and do the needful.\n\nThank You ! \n\nRegards,\nSciPy India 2016,\nFOSSEE - IIT Bombay"""
            # send_mail(subject, message, sender_email, to)
            proposal.status="Commented"
            proposal.save()
            context['proposal'] = proposal
            context['comments'] = comments
            context.update(csrf(request))
            return render(request, 'comment-abstract.html', context)
        else:
            comments = Comments.objects.filter(proposal=proposal)
            context['proposal'] = proposal
            context['comments'] = comments
            context.update(csrf(request))
            return render(request, 'comment-abstract.html', context)
    else:
        return render(request, 'comment-abstract.html', context)



def status(request, proposal_id= None):
    user = request.user
    context = {}
    if user.is_authenticated():
        proposal = Proposal.objects.get(id=proposal_id)
        if 'accept' in request.POST:
            proposal.status="Accepted"
            proposal.save()
            sender_name = "SciPy India 2016"
            sender_email = "scipy@fossee.in"
            subject = "SciPy India - Proposal Accepted"
            to = (proposal.user.email, )
            message = """Dear """+proposal.user.first_name+"""Congratulations your proposal for the talk/workshop titled '"""+ proposal.title+ """'is accepted you shall present the talk/ conduct the workshop at the conference.\n\nYou will be notified regarding instructions of your talk/workshop via email.\n\nThank You ! \n\nRegards,\nSciPy India 2016,\nFOSSEE - IIT Bombay"""
            send_mail(subject, message, sender_email, to)
            context.update(csrf(request))
        elif 'reject' in request.POST:
            proposal.status="Rejected"
            proposal.save()
            sender_name = "SciPy India 2016"
            sender_email = "scipy@fossee.in"
            subject = "SciPy India - Proposal Rejected"
            to = (proposal.user.email, )
            message = """Dear """+proposal.user.first_name+"""We regret to inform you that your proposal for the talk/workshop titled '"""+ proposal.title +"""'.\n\nThank You ! \n\nRegards,\nSciPy India 2016,\nFOSSEE - IIT Bombay"""
            send_mail(subject, message, sender_email, to)
            context.update(csrf(request))  
        elif 'resubmit' in request.POST:
            proposal.status="Resubmit"
            proposal.save()
            sender_name = "SciPy India 2016"
            sender_email = "scipy@fossee.in"
            subject = "SciPy India - Resubmit"
            to = (proposal.user.email, )
            message = """Dear """+proposal.user.first_name+""",\n\nThank You ! \n\nRegards,\nSciPy India 2016,\nFOSSEE - IIT Bombay"""
            send_mail(subject, message, sender_email, to)
            context.update(csrf(request)) 
    proposals = Proposal.objects.all()
    context['proposals'] = proposals
    context['user'] = user
    return render(request, 'view-abstracts.html', context)  
    


def delete(request):
    user = request.user
    context = {}
    if user.is_authenticated():
        if 'delete' in request.POST:
            delete_proposal = request.POST.getlist('delete_proposal')
            print"-------------- in delete", delete_proposal
            for proposal_id in delete_proposal:
                print proposal_id
                proposal = Proposal.objects.get(id = proposal_id)
                proposal.delete()
            context.update(csrf(request)) 
        elif 'dump' in request.POST:
            print" in dump"
            delete_proposal = request.POST.getlist('delete_proposal')
            try:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="Proposals.csv"'
                writer = csv.writer(response)
                header = [
                            'name',
                            'username',
                            'email',
                            'about_me',
                            'phone',
                            'title',
                            'abstract',
                            'prerequisite',
                            'duration',
                            'attachment',
                            'date_created',
                            'status',
                            'proposal_type',
                            'tags',
                            'rate',
                      ]
                writer.writerow(header)
                for proposal_id in delete_proposal:
                    proposal = Proposal.objects.get(id = proposal_id)
                    print"proposal", proposal
                    row = [
                            '{0} {1}'.format(proposal.user.first_name, proposal.user.last_name),
                            proposal.user.username,
                            proposal.user.email,
                            proposal.about_me,
                            proposal.phone,
                            proposal.title,
                            proposal.abstract,
                            proposal.prerequisite,
                            proposal.duration,
                            proposal.attachment,
                            proposal.date_created,
                            proposal.status,
                            proposal.proposal_type,
                            proposal.tags,
                            proposal.rate
                            ]
                    writer.writerow(row)
                return response
            except:
                proposals = Proposal.objects.all()
                context['proposals'] = proposals
                context['user'] = user
                return render(request, 'view-abstracts.html', context) 
        else:
            proposals = Proposal.objects.all()
            context['proposals'] = proposals
            context['user'] = user
            return render(request, 'view-abstracts.html', context) 
    else:
        return render(request, 'view-abstracts.html', context) 


