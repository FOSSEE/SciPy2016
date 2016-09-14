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


from website.forms import ProposalForm, UserRegisterForm, UserLoginForm, WorkshopForm, CommentForm
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


def home(request):
    context = {}
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
        except:
            context['mailfailed'] = True
    return render_to_response('base.html', context)


def cfp(request):
    if request.method == "POST":
        context = {}
        context.update(csrf(request))
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user.is_superuser :
            login(request, user)
            print"in cfp view"
            proposals = Proposal.objects.all()
            context['proposals'] = proposals
            context['user'] = user
            return render_to_response('cfp.html', context)
        elif user is not None:
            login(request, user)
            if 'next' in request.GET:
                next = request.GET['next']
                return HttpResponseRedirect(next)
            if Proposal.objects.filter(user = user).exists :
                print "---------------------->>>>>>>>>>", user 
                proposals = Proposal.objects.filter(user = user)
                for p in proposals:
                    print "-------->", p
                context['proposals'] = proposals
                context['user'] = user
            return render_to_response('cfp.html', context)
        else:
            context['invalid'] = True
            context['form'] = UserLoginForm
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
        if request.method == 'POST':
            form = ProposalForm(request.POST, request.FILES)
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
                return render_to_response('submit-cfp.html', context)
        else:
            form = ProposalForm()
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
                return render_to_response('submit-cfw.html', context)
        else:
            form = WorkshopForm()
            context['proposal_form'] = form
        return render_to_response('submit-cfw.html', context)
    else:
        context['login_required'] = True
        return render_to_response('cfp.html', context)


def view_abstracts(request):
    user = request.user
    context = {}
    if user.is_authenticated():
        if user.is_superuser :
            proposals = Proposal.objects.all()
            context['proposals'] = proposals
            context['user'] = user
            return render(request, 'view-abstracts.html', context)
        elif user is not None:
            # if request.method == "POST":
            #     if request.POST.get('delete'):
            #         Proposal.objects.filter(id__in=request.POST.getlist('delete_proposal')).delete()
            #     # print "---------------------",request.POST
            #     # delete_proposal = request.POST.getlist('delete_proposal')
            #     # for propsal_id in delete_proposal:
            #     #     proposal = Proposal.objects.get(id = proposal_id)
            #     #     proposal.remove()
            #     context = RequestContext(request, {'request': request,
            #                            'user': request.user})
            #     context.update(csrf(request))
            #     return render(request, 'view-abstracts.html',context_instance=context)
            if Proposal.objects.filter(user = user).exists :
                print "in view-abstracts ---------------------->>>>>>>>>>", user 
                proposals = Proposal.objects.filter(user = user)
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
            subject = "SciPy India - Comment of Your Proposal"
            to = (proposal.user.email, )
            message = """Dear """+proposal.user.first_name+""",\n\nThank You ! \n\nRegards,\nSciPy India 2016,\nFOSSEE - IIT Bombay"""
            send_mail(subject, message, sender_email, to)
            context['proposal'] = proposal
            context['comments'] = comments
            # if request.GET.get("accept"):
            #     print "-----------user clicked list"
            context.update(csrf(request))
            return render(request, 'comment-abstract.html', context)
        # elif request.GET.get("accept"):
        #     print"----------------- accept"
        #     context.update(csrf(request))
        #     return render(request, 'comment-abstract.html', context)
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
            message = """Dear """+proposal.user.first_name+""",\n\nThank You ! \n\nRegards,\nSciPy India 2016,\nFOSSEE - IIT Bombay"""
            send_mail(subject, message, sender_email, to)
            context.update(csrf(request))
        elif 'reject' in request.POST:
            proposal.status="Rejected"
            proposal.save()
            sender_name = "SciPy India 2016"
            sender_email = "scipy@fossee.in"
            subject = "SciPy India - Proposal Rejected"
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
    proposals = Proposal.objects.all()
    context['proposals'] = proposals
    context['user'] = user
    return render(request, 'view-abstracts.html', context)  


