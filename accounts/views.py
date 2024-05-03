from urllib import request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView
from .form import CandidateSignUpForm, RecruiterSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, RecruiterPosting, Recruiter, CandidateApply, Candidate


class candidate_register(CreateView):
    model = User
    form_class = CandidateSignUpForm
    template_name = '../templates/candidate_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class candidate_update(UpdateView):
    model = Candidate
    fields = ['institute_name', 'phone', 'Experience', 'year_of_passing', 'Skills', 'profile_pic',
              'institute_certificate']
    exclude = ['user']

    template_name = '../templates/candidate_update.html'


class CandidateDetailView(DetailView):
    model = Candidate
    context_object_name = "profile"
    template_name = "profile.html"

    def get_object(self, queryset=None):
        return self.request.user.candidate


class recruiter_register(CreateView):
    model = User
    form_class = RecruiterSignUpForm
    template_name = '../templates/recruiter_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class recruiterDetailView(DetailView):
    model = Recruiter
    context_object_name = "profile"
    template_name = "recuiter_profile.html"

    def get_object(self, queryset=None):
        return self.request.user.recruiter


class recruiter_update(UpdateView):
    model = Recruiter
    fields = ['phone_number', 'company_name', 'company_description']

    template_name = '../templates/recruiter_update.html'


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('/admin')
            elif user is not None and user.is_candidate:
                login(request, user)
                return redirect('/jobs_result')
            elif user is not None and user.is_recruiter:
                login(request, user)
                return redirect('/application_view')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, '../templates/login.html',
                  context={'form': AuthenticationForm()})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('/')


def index(request):
    post = RecruiterPosting.objects.all()[:15]
    context = {
        'post': post
    }
    return render(request, '../templates/index.html', context)

@login_required(login_url='login')
def jobs_detail(request, pk):
    post = RecruiterPosting.objects.get(pk=pk)
    return render(request, '../templates/jobs_detail.html', {'post': post})


# @login_required(login_url='login')
# def recruiter_posting2(request):
#     if request.method == "POST":
#         job_title = request.POST.get('job_title')
#         job_description = request.POST.get('job_description')
#         location = request.POST.get('location')
#         skills = request.POST.get('skills')
#         job_type = request.POST.get('job_type')
#         ctc = request.POST.get('ctc')
#         company_name = request.POST.get('company_name')
#         posting = RecruiterPosting.objects.create(job_title=job_title, job_description=job_description,
#                                                   location=location, skills=skills, job_type=job_type, ctc=ctc,
#                                                   company_name=company_name)
#
#         posting.save()
#         return redirect('/application_view')


#    return render(request, '../templates/recruiter_posting.html')


class recruiter_posting(CreateView):
    model = RecruiterPosting
    fields = ['job_title', 'location', 'job_description', 'job_type', 'ctc', 'skills']
    template_name = '../templates/recruiter_posting2.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user.recruiter
        self.object.company_name = self.request.user.recruiter.company_name
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required(login_url='login')
def jobs_result(request):
    posts = RecruiterPosting.objects.all()
    post = Recruiter.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'post': post,
    }
    return render(request, '../templates/jobs_result.html', context=context)


@login_required(login_url='login')
def Applied_For(request):
    # posts = RecruiterPosting.objects.all()
    # post = Recruiter.objects.all()
    applicand = CandidateApply.objects.filter(cand=request.user.candidate)
    paginator = Paginator(applicand, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'post': applicand,
    }
    return render(request, '../templates/apply_for.html', context=context)


@login_required(login_url='login')
def full_time(request):
    posts = RecruiterPosting.objects.all().order_by('job_type')
    post = Recruiter.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'post': post,
    }
    return render(request, '../templates/jobs_result.html', context=context)


@login_required(login_url='login')
def internship(request):
    posts = RecruiterPosting.objects.all().order_by('-job_type')
    post = Recruiter.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'post': post,
    }
    return render(request, '../templates/jobs_result.html', context=context)


@login_required(login_url='login')
def search(request):
    query = request.GET['query']
    posts = RecruiterPosting.objects.filter(job_description__icontains=query)
    params = {'posts': posts}
    return render(request, '../templates/search.html', params)


# @login_required(login_url='login')
# def candidate_apply(request):
#     user = Candidate.objects.get(user=request.user)
#     applying = CandidateApply.objects.create(mobile_number=user.phone, applicant_name=user.first_name,
#                                              user=request.user)
#
#     applying.save()
#     return redirect('/jobs_result')


@property
def resume_url(self):
    if self.resume and hasattr(self.resume, 'url'):
        return self.resume.url


@login_required(login_url='login')
def application_view(request):
    post = CandidateApply.objects.filter(apply__user=request.user.recruiter, status__in=['pending', 'Approved'])
    print(post)
    paginator = Paginator(post, 5)
    page = request.GET.get('page')
    post = paginator.get_page(page)

    context = {
        'post': post,
    }

    return render(request, '../templates/application_view.html', context=context)


def contact(request):
    return render(request, '../templates/contact.html')


class UpdateCandidate(UpdateView):
    model = Candidate
    fields = '__all__'
    template_name = "candidate_update.html"

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def candidate_apply(req, pk):
    app = RecruiterPosting.objects.get(pk=pk)
    if req.user.is_candidate:
        CandidateApply.objects.create(apply=app, cand=req.user.candidate)
        # CandidateApply.objects.filter(pk=pk).update(status="Accepted")
        return HttpResponseRedirect(redirect_to="/applied_for")
    return HttpResponseRedirect(redirect_to="/applied_for")


def cand_status(req, pk):

    CandidateApply.objects.filter(pk=pk).update(status="Approved")

    return HttpResponseRedirect(redirect_to="/application_view")

def cand_reject(req, pk):

    CandidateApply.objects.filter(pk=pk).update(status="Rejected")
    # CandidateApply.objects.filter(pk=pk).delete()

    return HttpResponseRedirect(redirect_to="/application_view")


def all_posting(request):
    return render(request, '../templates/all_posting.html')