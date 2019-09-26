from django.shortcuts import render, redirect
from clone.models import seller
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from rest_framework import viewsets
from clone.serializers import ItemSerializer, UserSerializer
from django.contrib.auth.models import User
from clone.permissions import MyUserPers, MyObjPer
import smtplib, ssl
from django.views.generic.base import View


smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "vaibhav.smtp.test@gmail.com"
password = "Vaibhav@12!"

def SendMail(message):
    context = ssl.create_default_context()
    server = smtplib.SMTP(smtp_server,port)
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail( sender_email, ["agrawalvaibhav12@gmail.com","vaibhav.smtp.test@gmail.com"], message)


def sendMail(message, target_email):
    context = ssl.create_default_context()
    server = smtplib.SMTP(smtp_server,port)
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail( sender_email, ["vaibhav.smtp.test@gmail.com", target_email], message)

def home(request):    
    return render(request, "base.html", {'actHome': 'active'})

def about(request):    
    return render(request, "about.html",  {'actAbt': 'active'})

def contact(request):
    if request.method == "POST":
        sendMail( "\n\nName:"+request.POST.get('uname','blank')+"\n\nPhone:"+request.POST.get('phone','blank')+"\n\nMessage:"+request.POST.get("msg", "blank"),"agrawalvaibhav12@gmail.com" )
    return render(request, "contact.html",  {'actCnt': 'active'})

def notallow(request):
    return render(request, "notallow.html")


@method_decorator(login_required, name='dispatch')
class ItemList(ListView):
        model = seller
        def get_queryset(self):
            si = self.request.GET.get('si')
            if si==None:
                si=''   
            return seller.objects.filter(Q(s_name__icontains = si) | Q(s_price__icontains = si)).order_by('-id')        
        def get_context_data(self, **kwargs):
            ctx = ListView.get_context_data(self, **kwargs)
            ctx['actseller'] = 'active'
            return ctx        

@method_decorator(login_required, name='dispatch')
class ItemDetails(DetailView):
        model = seller

# class ItemBuy(FormView):
#     model=seller
#     def send(self, request, *args, **kwargs):
#         return redirect("/clone/item/")
#         if request.method == "POST":
#             sendMail( "\n\nName:"+request.POST.get('uname','blank')+"\n\nPhone:"+request.POST.get('phone','blank')+"\n\nMessage:"+request.POST.get("msg", "blank"), {{object.s_mail}} )
#         return redirect("/clone/item/")

class ItemBuy(View):
    def get(self, request, pk):
        return render(request, 'buy.html', {"success": None})    
    def post(self, request, pk):
        success = True
        try:
            email = seller.objects.all().get(pk=pk).s_email
            sendMail( "\n\nName:"+request.POST.get('uname','blank')+"\n\nPhone:"+request.POST.get('phone','blank')+"\n\nEmail ID:"+request.POST.get('email','blank')+"\n\nMessage:"+request.POST.get("msg", "blank"), email )
        except Exception as e:
            print(e)
            success = False
        return render(request, 'buy.html', {"success": success})
    
def check_self_or_super(self, request, *args, **kwargs):
            if request.user.is_authenticated:
                self.object = self.get_object()
                if  (self.object.user != request.user) and not request.user.is_superuser:
                    return redirect("/clone/notallow/")
    
@method_decorator(login_required, name='dispatch')
class ItemCreate(CreateView):
        model = seller
        fields = ("s_name","user", "s_pn", "s_email", "item_name", "s_description", "s_img", "s_price","s_area")
        success_url ="/clone/item/"
        def form_valid(self, form):
#            https://www.youtube.com/watch?v=TcMBFSGVi1c
#            https://www.youtube.com/embed/TcMBFSGVi1c
#                 ulink = form.instance.ulink.replace(r"watch?v=", r"embed/")
#                 form.instance.ulink = ulink
#                 form.instance.user = self.request.user
                return super(ItemCreate, self).form_valid(form)        
        
        def get_context_data(self, **kwargs):
            ctx = CreateView.get_context_data(self, **kwargs)
            ctx['actCreate'] = 'active'
            return ctx        

@method_decorator(login_required, name='dispatch')
class ItemUpdate(UpdateView):        
        model = seller
        fields = "__all__"
        success_url ="/clone/"
        def form_valid(self, form):
#                 ulink = form.instance.ulink.replace(r"watch?v=", r"embed/")
#                 form.instance.ulink = ulink
                return super(ItemUpdate, self).form_valid(form)
        def dispatch(self, request, *args, **kwargs):
            ret = check_self_or_super(self, request, *args, **kwargs)
            if ret != None:
                return ret
            return UpdateView.dispatch(self, request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class ItemDelete(DeleteView):
        model = seller
        success_url ="/clone/"
        def dispatch(self, request, *args, **kwargs):
            ret = check_self_or_super(self, request, *args, **kwargs)
            if ret != None:
                return ret
            return DeleteView.dispatch(self, request, *args, **kwargs)

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = seller.objects.all().order_by('-id')
    serializer_class = ItemSerializer
    def get_queryset(self):
            si = self.request.GET.get('si')
            if si==None:
                si=''   
            return seller.objects.filter(Q(s_name__icontains = si) | Q(s_price__icontains = si)).order_by('-id')            
    permission_classes= (MyObjPer,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes= (MyUserPers,)

