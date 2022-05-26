from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action
from .forms import LoginForm, UserRegistrationForm,UserEditForm, ProfileEditForm, ProfileCreateForm
from .models import Profile, Contact, Exams_resultsItems
from cart.cart import Cart
from .task import exams_results_create
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


@login_required
def profile_create(request):
    cart = Cart(request)
    if request.method == "POST":
        #name = request.POST.get('name')
        form = ProfileCreateForm(instance=request.user.profile ,data=request.POST)
        if form.is_valid():
            profile = form.save()
            for item in cart:
                Exams_resultsItems.objects.create(profile = profile,
                                                  test = item['test'],
                                                  value= item['value'],
                                                  correct = item['correct'])
            cart.clear()
            exams_results_create.delay(profile.id)
            return render(request, 'account/user/exams_results.html', {'profile':profile})
    else:
        form = ProfileCreateForm()
    return render(request,'account/user/exams_results_create.html',{'cart':cart, 'form':form})




@staff_member_required
def admin_profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'account/admin/profile/profile.html', {'profile':profile})

@staff_member_required
def admin_profile_pdf(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    html = render_to_string('account/admin/profile/pdf.html', {'profile':profile})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf"'.format(profile.id)
    weasyprint.HTML(string=html,  base_url=request.build_absolute_uri() ).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')], presentational_hints=True)
    return response





def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]

    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
