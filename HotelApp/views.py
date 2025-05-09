from django.shortcuts import render,redirect
import sqlite3
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .import models
from .forms import Online_Booking_form,offline_Booking_form,Add_Employee_form,Add_Room_form,Add_salary_form
from django.http import HttpResponse

# Create your views here.
def Home(request):
    return render(request,'Home.html')
def all(request):
    return render(request,'allinclude.html')
def OnlineBooking(request):
    from .models import Add_Room
    if request.method == 'POST':
        upload_image = request.FILES.get('Img')
        MyData = models.Online_Booking()
        MyData.Id = request.POST.get('Id')
        MyData.Check_in = request.POST.get('Check_in')
        MyData.Check_out = request.POST.get('Check_out')
        MyData.ADULT = request.POST.get('ADULT')
        MyData.CHILDREN = request.POST.get('CHILDREN')
        MyData.Name = request.POST.get('Name')
        MyData.Surname = request.POST.get('Surname')
        MyData.Email = request.POST.get('Email')
        MyData.Phone_Number = request.POST.get('Phone_Number')
        MyData.Nid_No = request.POST.get('Nid_No')
        MyData.City = request.POST.get('City')
        MyData.Country = request.POST.get('Country')
        MyData.Img =  upload_image
        MyData.Address = request.POST.get('Address')
        MyData.Date = request.POST.get('Date')
        MyData.Time = request.POST.get('Time')
        MyData.save()
        messages.success(request, "Booking confirmed! Thank you for your reservation.")
        return redirect('OnlineBooking')
    # Get room_type and price from GET params
    room_type = request.GET.get('room_type', '')
    price = request.GET.get('price', '')
    # Get all rooms for dropdown
    all_rooms = Add_Room.objects.all()
    return render(request,'online_booking_page.html', {'room_type': room_type, 'price': price, 'all_rooms': all_rooms})
def Aothur_login(request):
    if request.method == 'POST':
        username = request.POST.get('Email')
        password = request.POST.get('Password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request,'Athur_login_page.html')
def auth_logout(request):
    logout(request)
    return redirect('Home')
def Aothur_Reg(request):
    if request.method == 'POST':
        username = request.POST.get('Email')
        password = request.POST.get('Password')
        confirm_password = request.POST.get('Con_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'Athur_Register_Page.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'Athur_Register_Page.html')
            
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=request.POST.get('Fname'),
            last_name=request.POST.get('Lname'),
            email=username
        )
        user.save()
        messages.success(request, 'Registration successful! Please login.')
        return redirect('Aothur_login')
        
    return render(request,'Athur_Register_Page.html')
def Aothur_Fotpass(request):
    return render(request,'Author_forgetpass_page.html')
def all_admin(request):
    return render(request,'admin/AdminAllinclude.html')
def Admin(request):
    data = models.Online_Booking.objects.all().order_by('-Id')
    return render(request,'admin/Admin.html',{'data':data})
def Addemployee(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')
        # fname = upload_image.name
        # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
        #     for ch in upload_image.chunks():
        #         location.write(ch)
        if request.method == 'POST':
            Data = models.Add_Employee()
            Data.Employee_Id = request.POST.get('Employee_Id')
            Data.First_Name = request.POST.get('First_Name')
            Data.Last_Name = request.POST.get('Last_Name')
            Data.Email = request.POST.get('Email')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.Joining_Date = request.POST.get('Joining_Date')
            Data.Dateof_Birth = request.POST.get('Dateof_Birth')
            Data.Departments = request.POST.get('Departments')
            Data.Gender = request.POST.get('Gender')
            Data.Blood_Group = request.POST.get('Blood_Group')
            Data.Education = request.POST.get('Education')
            Data.Personal_Identity = request.POST.get('Personal_Identity')
            Data.Guardian = request.POST.get('Guardian')
            Data.Guardian_Number = request.POST.get('Guardian_Number')
            Data.Upload_Image = upload_image
            Data.Address = request.POST.get('Address')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('Addemployee')
        else:
            return HttpResponse("Failed")

    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/addemployee.html',{'data':data})
def Editemployee(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    if request.method == 'POST':
        data = Add_Employee_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Upload_Image')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('Allemployee')
        else:
            return HttpResponse("Failed")

    select = data.Departments
    if select == 'Departments':
        select = 1
    elif select == 'Housekeeping':
        select = 2
    elif select == 'Manager':
        select = 3
    elif select == 'Chef':
        select = 4
    elif select == 'Food and Beverage':
        select = 5
    elif select == 'Kitchen':
        select = 6
    elif select == 'Security':
        select = 7
    else:
        select = 8

    select = data.Gender
    if select == 'Gender':
        select = 1
    elif select == 'MALE':
        select = 2
    else:
        select = 3

    return render(request,'admin/Editemployee.html',{'data': data,"select": select})
def Allemployee(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        return render(request, 'admin/allemployee.html', {"data": data})
    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/allemployee.html',{'data': data})
def online_Booking_info(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        show = models.Online_Booking.objects.filter(Country =Serch) or models.Online_Booking.objects.filter(Name=Serch)
        return render(request,'admin/Online_Booking.html',{"data":show})

    data = models.Online_Booking.objects.all().order_by('-Id')
    return render(request,'admin/Online_Booking.html',{'data':data})
def Edit_online_Booking(request,id):
    data = models.Online_Booking.objects.get(Id=id)
    if request.method == 'POST':
        data = Online_Booking_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Img')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('online_Booking_info')
        else:
            return HttpResponse("Failed")

    select = data.ADULT
    if select == 'ADULT':
        select = 1
    elif select == '1 ADULT':
        select = 2
    elif select == '2 ADULT':
        select = 3
    elif select == '3 ADULT':
        select = 4
    else:
        select = 5

    select = data.CHILDREN
    if select == 'CHILDREN':
        select = 1
    elif select == '1 CHILDREN':
        select = 2
    elif select == '2 CHILDREN':
        select = 3
    elif select == '3 CHILDREN':
        select = 4
    else:
        select = 5
    return render(request,'admin/EditonlineBooking.html',{'data': data,"select":select})
def AddCustomer(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')
        # fname = upload_image.name
        # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
        #     for ch in upload_image.chunks():
        #         location.write(ch)
        if request.method == 'POST':
            Data = models.Offline_Booking()
            Data.Customer_Id = request.POST.get('Customer_Id')
            Data.Check_in = request.POST.get('Check_in')
            Data.Check_out = request.POST.get('Check_out')
            Data.First_Name = request.POST.get('First_Name')
            Data.Last_Name = request.POST.get('Last_Name')
            Data.Email = request.POST.get('Email')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.ADULT = request.POST.get('ADULT')
            Data.CHILDREN = request.POST.get('CHILDREN')
            Data.Total_Person = request.POST.get('Total_Person')
            Data.Select_Room = request.POST.get('Select_Room')
            Data.Room_Number = request.POST.get('Room_Number')
            Data.Gender = request.POST.get('Gender')
            Data.Personal_Identity = request.POST.get('Personal_Identity')
            Data.Upload_Image = upload_image
            Data.Country = request.POST.get('Country')
            Data.Address = request.POST.get('Address')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('AddCustomer')
        else:
            return HttpResponse("Failed")

    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request,'admin/AddCustomer.html',{'data': data})
def AllCustomer(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        print(Serch)
        data = models.Offline_Booking.objects.filter(First_Name=Serch) or models.Offline_Booking.objects.filter( Email=Serch)
        return render(request, 'admin/AllCustomer.html', {"data": data})
    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request,'admin/AllCustomer.html',{'data': data})
def EditCustomer(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    if request.method == 'POST':
        data = offline_Booking_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Upload_Image')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('AllCustomer')
        else:
            return HttpResponse("Failed")

    select = data.ADULT
    if select == 'ADULT':
        select = 1
    elif select == '1 ADULT':
        select = 2
    elif select == '2 ADULT':
        select = 3
    elif select == '3 ADULT':
        select = 4
    else:
        select = 5

    select = data.CHILDREN
    if select == 'CHILDREN':
        select = 0
    elif select == '1 CHILDREN':
        select = 1
    elif select == '2 CHILDREN':
        select = 2
    elif select == '3 CHILDREN':
        select = 3
    else:
        select = 4

    select = data.Select_Room
    if select == 'Select Room':
        select = 1
    elif select == 'Delux':
        select = 2
    elif select == 'Super Delux':
        select = 3
    elif select == 'Single':
        select = 4
    else:
        select = 5

    select = data.Room_Number
    if select == 'Room Number':
        select = 1
    elif select == 'Room101':
        select = 2
    elif select == 'Room102':
        select = 3
    elif select == 'Room103':
        select = 4
    else:
        select = 5

    select = data.Gender
    if select == 'Gender':
        select = 1
    elif select == 'MALE':
        select = 2
    else:
        select = 3

    return render(request,'admin/EditCustomer.html',{'data': data,"select": select})
def Delete(request,id):
    data = models.Online_Booking.objects.get(Id=id)
    data.delete()
    return redirect('online_Booking_info')

def Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        data = models.Offline_Booking.objects.filter(First_Name=Serch) or models.Offline_Booking.objects.filter(Email=Serch)
        return render(request, 'admin/AddCustomer.html', {"data": data})

def AddCustpage_Delete(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    data.delete()
    return redirect('AddCustomer')
def AllCustpage_Delete(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    data.delete()
    return redirect('AllCustomer')

def AddEmplopage_Delete(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    data.delete()
    return redirect('Addemployee')

def Add_Employee_Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        return render(request,'admin/addemployee.html', {"data": data})

def AllEmployee_Delete(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    data.delete()
    return redirect('Allemployee')

@login_required
def Add_room(request):
    if request.method == 'POST':
        form = Add_Room_form(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Room added successfully!')
                return redirect('Add_room')
            except Exception as e:
                messages.error(request, f'Error adding room: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = Add_Room_form()
    
    data = models.Add_Room.objects.all().order_by('-Id')
    return render(request, 'admin/AddRoom.html', {'form': form, 'data': data})

def All_Room(request):
    try:
        data = models.Add_Room.objects.all().order_by('-Id')
        return render(request, 'admin/AllRooms.html', {'data': data})
    except Exception as e:
        messages.error(request, f'Error loading rooms: {str(e)}')
        return render(request, 'admin/AllRooms.html', {'data': []})

def Add_Room_Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        print(Serch)
        data = models.Add_Room.objects.filter(Room_Number=Serch) or models.Add_Rooms.objects.filter(Room_Type=Serch)
        return render(request, 'admin/AddRoom.html',{"data": data})

def AddRooms_Delete(request,id):
    data = models.Add_Room.objects.get(Id=id)
    data.delete()
    return redirect('Add_room')

def EditRooms(request,id):
    data = models.Add_Room.objects.get(Id=id)
    if request.method == 'POST':
        data = Add_Room_form(request.POST, request.FILES, instance=data)
        if data.is_valid():
            # upload_image = request.FILES.get('Room_Image')
            # fname = upload_image.name
            # with open('E:/Project2/HotelManagementSystem/static/Allfiles/Media/' + fname, 'wb+') as location:
            #     for ch in upload_image.chunks():
            #         location.write(ch)
            data.save()
            return redirect('All_Room')
        else:
            return HttpResponse("Failed")


    select = data.Room_Type
    if select == 'Select Room':
        select = 1
    elif select == 'Delux':
        select = 2
    elif select == 'Super Delux':
        select = 3
    elif select == 'Single':
        select = 4
    else:
        select = 5

    select = data.Room_Number
    if select == 'Room Number':
        select = 1
    elif select == 'Room101':
        select = 2
    elif select == 'Room102':
        select = 3
    elif select == 'Room103':
        select = 4
    else:
        select = 5

    select = data.Room_Floor
    if select == 'Room Floor':
        select = 1
    elif select == 'Floor_G':
        select = 2
    elif select == 'Floor_First':
        select = 3
    elif select == 'Floor_Second':
        select = 4
    else:
        select = 5

    return render(request,'admin/EditRooms.html',{'data': data,"select": select})

def AllRooms_Delete(request,id):
    data = models.Add_Room.objects.get(Id=id)
    data.delete()
    return redirect('All_Room')

def AddEmployeeSalary(request):
    if request.method == 'POST':
        if request.method == 'POST':
            Data = models.Add_Salarys()
            Data.Employee_Id = request.POST.get('Employee_Id')
            Data.Employee_Name = request.POST.get('Employee_Name')
            Data.Email = request.POST.get('Email ')
            Data.Mobile_Number = request.POST.get('Mobile_Number')
            Data.Departments = request.POST.get('Departments')
            Data.Salary = request.POST.get('Salary')
            Data.Date = request.POST.get('Date')
            Data.Time = request.POST.get('Time')
            Data.save()
            return redirect('AddEmployeeSalary')
        else:
            return HttpResponse("Failed")

    return render(request, 'admin/AddEmployeeSalary.html')

def EmployeeShow(request):

    return render(request, 'admin/EmployeeShow.html')

def roomrate(request):
    return render(request, 'roomrate.html')
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact_us')
        
    return render(request, 'contact_us.html')

def gallery(request):
    return render(request, 'gallery.html')

def location(request):
    return render(request, 'location.html')

def about_us(request):
    return render(request, 'about_us.html')

def explore(request):
    return render(request, 'explore.html')