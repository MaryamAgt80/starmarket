from django.shortcuts import redirect, render
from django.views import View
from .forms import RecordFormUser, LoginFormUser, ChangePassForm, FormEmail,EditProfileForm
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest,JsonResponse
from django.utils.decorators import method_decorator
from .jsonfile import data_json
from Order.models import Address
from utils.servise_email import send_email_text
from Site_App.models import MessageToAdmin,AdminToUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
#########################################
@login_required(login_url='login')
def RemoveAddres(request:HttpRequest):
    status=False
    try:
        id=int(request.GET.get('id'))
        address:Address=Address.objects.filter(id=id,user_id=request.user.id).first()
        if address is not None:
            address.delete()
            status=True
    except:
        pass
    return JsonResponse({'status':status})


###########################################
@login_required(login_url='login')
def AllAddress(request:HttpRequest):
    all_address=Address.objects.filter(user_id=request.user.id)
    return render(request,'pages/address_page.html',{'Address':all_address})
############################
@method_decorator(login_required(login_url='login'),name='dispatch')
class EditAddress(View):
    def get(self,request:HttpRequest,id):
        addres:Address=Address.objects.filter(user_id=request.user.id,id=id).first()
        state=addres.state
        city=addres.city
        address_text=addres.address
        post_code=addres.post_code
        ListState = []

        for statee in data_json.keys():
            ListState.append(statee)
        ListCity=[]
        for cityy in data_json.get(state):
            ListCity.append(cityy)
        return render(request,'pages/edit_address.html',{'States':ListState,'statee':state,'cityy':city,'address_text':address_text,'post_code':post_code,'Cities':ListCity})
    def post(self,request:HttpRequest,id):
        status=False
        addres: Address = Address.objects.filter(user_id=request.user.id, id=id).first()
        state = addres.state
        city = addres.city
        address_text = addres.address
        post_code = addres.post_code
        message='لطفا تمام فیلد های مورد نظر را وارد کنید.'
        if request.POST['state'] and request.POST['address'] and request.POST['post_code'] and request.POST['city']:
            city=request.POST['city']
            state=request.POST['state']
            address=request.POST['address']
            post_code=request.POST['post_code']
            addres.city=city
            addres.state=state
            addres.address=address
            addres.post_code=post_code
            addres.save()
            status=True
            message='ادرس مورد نظر با موفقیت ویرایش شد'
        ListState = []
        for statee in data_json.keys():
            ListState.append(statee)
        ListCity = []
        for cityy in data_json.get(state):
            ListCity.append(cityy)
        return render(request, 'pages/edit_address.html', {'States': ListState,'message':message,'status':status,'state':state,'city':city,'address_text':address_text,'post_code':post_code})
########################
@method_decorator(login_required(login_url='login'),name='dispatch')
class AddAddress(View):
    def get(self,request:HttpRequest):
        ListState = []
        for state in data_json.keys():
            ListState.append(state)
        return render(request,'pages/add_address.html',{'States':ListState})
    def post(self,request:HttpRequest):
        status=False

        message='لطفا تمام فیلد های مورد نظر را وارد کنید.'
        if request.POST['city'] and request.POST['state'] and request.POST['address'] and request.POST['post_code']:
            city=request.POST['city']
            state=request.POST['state']
            address=request.POST['address']
            post_code=request.POST['post_code']
            address_user:Address=Address.objects.create(user_id=request.user.id,state=state,city=city,address=address,post_code=post_code)
            address_user.save()
            status=True
            message='ادرس مورد نظر با موفقیت ثبت شد'
        ListState = []
        for state in data_json.keys():
            ListState.append(state)
        return render(request, 'pages/add_address.html', {'States': ListState,'message':message,'status':status})
####################### show cities #########
def Show_Cities(request):
    state=request.GET.get('state')
    list_city=[]
    for city in data_json.get(state):
        list_city.append(city)
    return render(request,'pages/cities.html',{'Cities':list_city})


####################### SIGN ############################################################
class RcordUser(View):

    def get(self, request):
        form = RecordFormUser()
        return render(request, 'pages/login.html',
                      {'form': form, 'caption_button': 'ثبت نام', 'caption': 'ثبت نام حساب جدید'})

    def post(self, request):
        form = RecordFormUser(request.POST)
        if form.is_valid():
            exist_user_name: bool = User.objects.filter(username=form.cleaned_data.get('username')).exists()
            if exist_user_name:
                form.add_error('username', 'نام کاربری دیگری وارد کنید')
                return render(request, 'pages/login.html', {'form': form})
        exist_email: bool = User.objects.filter(email=form.cleaned_data.get('email')).exists()
        if exist_email:
            form.add_error('email', 'ایمیل وارد شده از قبل موجود است')
            return render(request, 'pages/login.html', {'form': form})
        if (form.cleaned_data.get('password') == form.cleaned_data.get('passwordAgain')):
            NewUser = User(username=form.cleaned_data.get('username'),
                           email=form.cleaned_data.get('email'),
                           active_code=get_random_string(100),
                           name=form.cleaned_data.get('name')
                           )
            NewUser.set_password(form.cleaned_data.get('password'))
            NewUser.save()

            send_email_text('لینک فعال ساز سایت استارمارکت', NewUser.email, {'key': NewUser.active_code},
                            'pages/email_active_account.html')
            return render(request, 'pages/message.html',
                          {'message': 'حساب کاربری با موفقیت ثبت شد لینک فعالسازی به ایمیل شما فرستاده شد.'})
        else:
            form.add_error('password', 'رمز نامعتبر')
            return render(request, 'pages/login.html',
                          {'form': form, 'caption_button': 'ثبت نام', 'caption': 'ثبت نام حساب جدید'})


############################### RENDER PANEL ####################################################
@login_required(login_url='login')
def render_panel(request):
    return render(request, 'base/renderpanel.html')


############################## LOGIN #####################################################
class LogUser(View):
    def get(self, request):
        form = LoginFormUser()
        return render(request, 'pages/login.html', {'form': form, 'caption_button': 'ورود', 'caption': 'ورود به حساب'})

    def post(self, request):
        form = LoginFormUser(request.POST)
        if form.is_valid():
            UserLOg: User = User.objects.filter(username=form.cleaned_data.get('username')).first()
            if UserLOg is not None:
                if UserLOg.is_active:
                    if (UserLOg.check_password(form.cleaned_data.get('password'))):

                        login(request, UserLOg)
                        return render(request, 'pages/message.html',
                                      {'message': 'کاربر مورد نظر با موفقیت وارد حساب خود شدید.'})
                    else:
                        form.add_error('password', 'رمز وارد شده صحیح نیست')
                else:
                    form.add_error('username', 'کاربر وارد شده فعال نیست')
            else:
                form.add_error('username', 'نام کاربری وارد شده معتبر نیست')
        return render(request, 'pages/login.html', {'form': form, 'caption_button': 'ورود', 'caption': 'ورود به حساب'})


#################################### Forgot Password ###############################################
class ForgotPass(View):
    def get(self, request, pk):
        user: User = User.objects.filter(active_code=pk).first()
        if user is not None:
            form = ChangePassForm()
            return render(request, 'pages/login.html',
                          {'form': form, 'user': user, 'caption_button': 'تغییر', 'caption': 'تغییر پسورد'})
        else:
            return render(request, 'pages/message.html', {'message': 'کد نامعتبر'})

    def post(self, request, pk):
        form = ChangePassForm(request.POST)
        user: User = User.objects.filter(active_code=pk).first()
        if form.is_valid():
            if user is not None:
                if (form.cleaned_data.get('password') == form.cleaned_data.get('passwordAgain')):
                    password = form.cleaned_data.get('password')
                    user.set_password(password)
                    user.save()
                    return render(request, 'pages/message.html', {'message': 'تغییر رمز شما با موفقیت انجام شد.'})
                else:
                    form.add_error('passwordAgain', 'عدم همخوانی رمز ها با یک دیگر')
                    return render(request, 'pages/login.html',
                                  {'form': form, 'user': user, 'caption_button': 'تغییر', 'caption': 'تغییر پسورد'})
            else:
                return render(request, 'pages/message.html', {'message': 'کد نامعتبر'})

        else:
            form.add_error('passwordAgain', 'لطفا تمام فیلد های مورد نظر را وارد کنید.')
            return render(request, 'pages/login.html',
                          {'form': form, 'user': user, 'caption_button': 'تغییر', 'caption': 'تغییر پسورد'})


############################################# logout ##################################
@login_required(login_url='login')
def LogOut(request):
    logout(request)
    return render(request, 'pages/message.html', {'message': 'شما از حساب خود خارج شوید.'})


###################################### Active Code ###############3
def ActiveAccount(request, pk):
    user: User = User.objects.filter(active_code=pk).first()
    if user is not None:
        user.active_code = get_random_string(100)
        user.is_active = True
        user.save()
        return render(request, 'pages/message.html', {'message': 'کاربر مورد نظر شما فعال شد'})
    return render(request, 'pages/message.html', {'message': 'کد نامعتبر'})
##############  Panel Account #####################

@login_required(login_url='login')
def PanelAccount(request):
    return render(request, 'pages/panel_account.html')

##############################################

@login_required(login_url='login')
def partial_view(request):
    return render(request, 'pages/render_partial.html')

###################### Change Pass  ############

# @login_required(login_url='login')
class ChangePass(View):
    def get(self, request: HttpRequest):
        form = ChangePassForm()
        return render(request,'pages/change_pass_panel.html', {'form':form})

    def post(self, request: HttpRequest):
        status=False
        user: User = User.objects.filter(id=request.user.id).first()
        form = ChangePassForm(request.POST)
        if form.is_valid():
            if user is not None:
                if (form.cleaned_data.get('password') == form.cleaned_data.get('passwordAgain')):
                    password = form.cleaned_data.get('password')
                    user.set_password(password)
                    user.save()
                    status=True
                    return render(request,'pages/change_pass_panel.html', {'form': form,'status':status})
                else:
                    form.add_error('passwordAgain', 'عدم همخوانی رمز ها با یک دیگر')
                    return render(request, 'pages/change_pass_panel.html', {'form': form})
            else:
                return render(request, 'pages/change_pass_panel.html', {'message': 'کد نامعتبر'})
        else:
            form.add_error('passwordAgain', 'لطفا تمام فیلد های مورد نظر را وارد کنید.')
            return render(request, 'pages/change_pass_panel.html',  {'form': form})

############## Edit Profile ##############
@method_decorator(login_required(login_url='login'), name='dispatch')
class EditProfile(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileForm(instance=current_user)
        return render(request, 'pages/edit_profile.html', {'form':edit_form})

    def post(self, request: HttpRequest):
        status=False
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            status=True



        return render(request, 'pages/edit_profile.html', {'form':edit_form,'status':status})

################################ Edit Email ##############################
@method_decorator(login_required(login_url='login'), name='dispatch')
class EditEmail(View):
    def get(self, request: HttpRequest):
        email_form=FormEmail()
        current_user = User.objects.filter(id=request.user.id).first()
        email = current_user.email

        #######send active code###############
        return render(request, 'pages/edit_email.html', {'form':email_form,'email':email})

    def post(self, request: HttpRequest):
        status=False
        current_user = User.objects.filter(id=request.user.id).first()
        email=current_user.email
        email_form=FormEmail(request.POST)
        if email_form.is_valid():
            re_email=email_form.cleaned_data.get('Email')
            if re_email != current_user.email:
                email_check=User.objects.filter(email=re_email).exists()
                if email_check:
                    email_form.add_error('Email','ایمیل از قبل موجود است')
                else:
                    current_user.re_email=re_email
                    current_user.save()
                    send_email_text('لینک فعال ساز ایمیل در استارمارکت', current_user.re_email, {'key': current_user.active_code},
                            'pages/active_reemail.html')
                    status=True
                    return render(request, 'pages/edit_email.html', {'form':email_form,'email':email,'status':status})
            else:
                email_form.add_error('Email','مشابهت با ایمیل ثبت شده')
        return render(request, 'pages/edit_email.html', {'form':email_form,'email':email})
######################## active_email #########
def Active_Email(request:HttpRequest,code):
    user:User=User.objects.filter(active_code=code).first()
    message='بروز خطا'
    if user is not None:
        if user.re_email is not None and user.email != user.re_email:
            user.email=user.re_email
            user.re_email=''
            user.active_code=get_random_string(100)
            user.save()
            message='ایمیل شما با موفقیت فعال شد'
    return render(request,'pages/message.html',{'message':message})
#########################################################
class send_email_pass(View):
    def get(self,request):
        form=FormEmail()
        return render(request,'pages/login.html',{'form':form,'caption_button':'بازنشانی رمز عبور','caption':"فراموشی رمز عبور"})
    def post(self,request):
        form=FormEmail(request.POST)
        if form.is_valid():
            user:User=User.objects.filter(email=form.cleaned_data.get('Email'),is_active=True).first()
            if user is not None:

                send_email_text('بازنشانی رمز عبور در استارمارکت', user.email,
                                {'key': user.active_code},
                                'pages/forgot_email.html')

                return render(request,'pages/message.html',{'message':'لینک رست رمز برای ایمیل شما فرستاده شد'})
            else:
                form.add_error('Email','ایمیل مورد نظر موجود نیست')


        return render(request, 'pages/login.html',
                      {'form': form, 'caption_button': 'بازنشانی رمز عبور', 'caption': "فراموشی رمز عبور"})



@permission_required('polls.add_choice')
def panel_admin(request):
    return render(request,'admin/base_panel.html')
@permission_required('polls.add_choice')
def render_panel_admin(request):
    return render(request,'admin/render_admin.html')
@permission_required('polls.add_choice')
def CommentToAdmin(request):
    Comments=MessageToAdmin.objects.filter(is_ready=False)
    return render(request,'admin/commnts.html',{'Comments':Comments})
@permission_required('polls.add_choice')
def chango_to_ready(request):
    try:
        id=int(request.GET.get('id'))
        comment:MessageToAdmin=MessageToAdmin.objects.filter(id=id).first()
        comment.delete()
    except:
        pass
    return JsonResponse({})


class CommentSingleAdmin(SuperUserRequiredMixin,View):
    def get(self,request,id):
         Comments:MessageToAdmin=MessageToAdmin.objects.filter(id=id).first()
         return render(request,'admin/single_comment.html',{'comment':Comments})
    def post(self,request:HttpRequest,id):
        message=request.POST['message']
        status=False
        if message:
            Comments: MessageToAdmin = MessageToAdmin.objects.filter(id=id).first()
            Model_reply=AdminToUser.objects.create(user_id=Comments.user.id,message=message,admin_po_id=request.user.id,message_user_id=Comments.id)
            Model_reply.save()
            send_email_text('استارمارکتینگ',Comments.user.email,
                            {'key':Model_reply.message},
                            'admin/email_reply.html')
            status=True
        return render(request, 'admin/single_comment.html', {'comment': Comments,'status':status})


