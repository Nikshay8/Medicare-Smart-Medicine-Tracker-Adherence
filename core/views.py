from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Medicine, MedicineLog, Caregiver, UserProfile
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from django.utils import timezone
import re

# ── Phone number validator ──
def is_valid_phone(phone):
    # Accepts +91XXXXXXXXXX or 10-digit number
    return bool(re.match(r'^\+?[0-9]{10,15}$', phone.replace(' ', '').replace('-', '')))

def signup_page(request):
    error = ""

    if request.method == "POST":
        username  = request.POST['username'].strip()
        email     = request.POST['email'].strip()
        password  = request.POST['password']
        confirm   = request.POST['confirm_password']
        phone     = request.POST.get('phone', '').strip()
        first     = request.POST.get('first_name', '').strip()
        last      = request.POST.get('last_name', '').strip()

        if not all([username, email, password, confirm, phone]):
            error = "All fields are required."
        elif len(username) < 3 or len(username) > 20:
            error = "Username must be between 3 and 20 characters."
        elif not username.replace("_", "").isalnum():
            error = "Username can contain only letters, numbers, and underscore."
        elif User.objects.filter(username=username).exists():
            error = "Username already taken."
        elif User.objects.filter(email=email).exists():
            error = "Email already registered."
        elif "@" not in email or "." not in email:
            error = "Enter a valid email address."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            error = "Password must contain both letters and numbers."
        elif password != confirm:
            error = "Passwords do not match."
        elif not is_valid_phone(phone):
            error = "Enter a valid phone number (10–15 digits, optionally starting with +)."
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first
            user.last_name  = last
            user.save()
            UserProfile.objects.create(user=user, phone=phone)
            return redirect('/login/')

    return render(request, 'signup.html', {'error': error})


def login_page(request):
    error = ""

    if request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password']

        if not username or not password:
            error = "All fields are required."
        elif len(username) < 3 or len(username) > 20:
            error = "Username must be between 3 and 20 characters."
        elif not username.replace("_", "").isalnum():
            error = "Invalid username format."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/dashboard/')
            else:
                error = "Invalid username or password."

    return render(request, 'login.html', {'error': error})


@login_required
def dashboard(request):
    medicines = Medicine.objects.filter(user=request.user)

    for medicine in medicines:
        logs = MedicineLog.objects.filter(medicine=medicine).order_by('-id')
        latest_log = logs.first()
        medicine.latest_status = latest_log.status if latest_log else "No status yet"

        missed_streak = 0
        for log in logs:
            if log.status == 'missed':
                missed_streak += 1
            else:
                break
        medicine.missed_streak  = missed_streak
        medicine.total_taken    = logs.filter(status='taken').count()
        medicine.total_missed   = logs.filter(status='missed').count()

    taken_count  = MedicineLog.objects.filter(medicine__user=request.user, status='taken').count()
    missed_count = MedicineLog.objects.filter(medicine__user=request.user, status='missed').count()

    alert_message        = ""
    caregiver_alert_sent = False
    caregiver = Caregiver.objects.filter(user=request.user).first()

    for medicine in medicines:
        logs = MedicineLog.objects.filter(medicine=medicine).order_by('-id')
        missed_streak     = 0
        latest_missed_log = None

        for log in logs:
            if log.status == 'missed':
                missed_streak += 1
                if latest_missed_log is None:
                    latest_missed_log = log
            else:
                break

        threshold = 3 if missed_streak >= 3 else (2 if missed_streak == 2 else 0)
        if threshold and latest_missed_log and not latest_missed_log.alert_sent:
            level   = "High Alert" if threshold >= 3 else "Alert"
            subject = f"MediCare {level}"
            alert_message = f"{level}: {medicine.name} has been missed {missed_streak} time(s) in a row."

            if caregiver:
                send_mail(
                    subject,
                    f'Dear {caregiver.name},\n\n{alert_message}\n\nPlease check on the patient.',
                    settings.EMAIL_HOST_USER,
                    [caregiver.email],
                    fail_silently=True,
                )
                caregiver_alert_sent = True

            latest_missed_log.alert_sent = True
            latest_missed_log.save()
            break
        elif missed_streak >= 3:
            alert_message = f"High Alert: {medicine.name} missed {missed_streak} times in a row."
        elif missed_streak == 2:
            alert_message = f"Alert: {medicine.name} missed 2 times in a row."

    today = timezone.localdate()
    now   = timezone.localtime(timezone.now())

    def medicine_time_passed(medicine):
        try:
            from datetime import datetime as dt
            scheduled = dt.strptime(medicine.time.strip(), "%I:%M %p")
            scheduled_today = now.replace(
                hour=scheduled.hour,
                minute=scheduled.minute,
                second=0,
                microsecond=0,
            )
            return now >= scheduled_today
        except ValueError:
            return False

    unlogged_medicines = [
        m for m in medicines
        if not MedicineLog.objects.filter(medicine=m, date=today).exists()
        and medicine_time_passed(m)
    ]

    # ── Recent activity (last 8 logs) ──
    from datetime import timedelta
    recent_logs = MedicineLog.objects.filter(
        medicine__user=request.user
    ).select_related('medicine').order_by('-id')[:8]

    recent_activity = []
    for log in recent_logs:
        if log.date == today:
            day_label = "Today"
        elif log.date == today - timedelta(days=1):
            day_label = "Yesterday"
        else:
            day_label = log.date.strftime('%d %b')
        recent_activity.append({
            'medicine_name': log.medicine.name,
            'status':        log.status,
            'time':          log.medicine.time,
            'day':           day_label,
        })

    context = {
        'medicines':           medicines,
        'taken_count':         taken_count,
        'missed_count':        missed_count,
        'alert_message':       alert_message,
        'caregiver_alert_sent':caregiver_alert_sent,
        'reminder_medicines':  list(medicines),
        'recent_activity':     recent_activity,
        'unlogged_medicines':  unlogged_medicines,
    }
    return render(request, 'dashboard.html', context)


def logout_page(request):
    logout(request)
    return redirect('/login/')


@login_required
def add_medicine(request):
    error = ""
    if request.method == "POST":
        name   = request.POST['name'].strip()
        hour   = request.POST['hour'].strip()
        minute = request.POST['minute'].strip()
        period = request.POST['period'].strip()

        if not all([name, hour, minute, period]):
            error = "All fields are required."
        elif len(name) < 2 or len(name) > 50:
            error = "Medicine name must be 2–50 characters."
        elif not name.replace(" ", "").replace("-", "").isalnum():
            error = "Medicine name can contain only letters, numbers, spaces, and hyphens."
        else:
            time_str = f"{hour}:{minute} {period}"
            if Medicine.objects.filter(user=request.user, name=name, time=time_str).exists():
                error = "This medicine at the same time already exists."
            else:
                Medicine.objects.create(user=request.user, name=name, time=time_str)
                return redirect('/dashboard/')

    return render(request, 'add_medicine.html', {'error': error})


@login_required
def edit_medicine(request, id):
    medicine = Medicine.objects.get(id=id, user=request.user)
    error    = ""

    time_parts = medicine.time.split(" ")
    clock_time = time_parts[0]
    period     = time_parts[1]
    hour, minute = clock_time.split(":")

    if request.method == "POST":
        name       = request.POST['name'].strip()
        new_hour   = request.POST['hour'].strip()
        new_minute = request.POST['minute'].strip()
        new_period = request.POST['period'].strip()

        if not all([name, new_hour, new_minute, new_period]):
            error = "All fields are required."
        elif len(name) < 2 or len(name) > 50:
            error = "Medicine name must be 2–50 characters."
        elif not name.replace(" ", "").replace("-", "").isalnum():
            error = "Medicine name can contain only letters, numbers, spaces, and hyphens."
        else:
            new_time = f"{new_hour}:{new_minute} {new_period}"
            if Medicine.objects.filter(user=request.user, name=name, time=new_time).exclude(id=medicine.id).exists():
                error = "This medicine at the same time already exists."
            else:
                medicine.name = name
                medicine.time = new_time
                medicine.save()
                return redirect('/dashboard/')

        hour, minute, period = new_hour, new_minute, new_period

    return render(request, 'edit_medicine.html', {
        'medicine': medicine, 'error': error,
        'hour': hour, 'minute': minute, 'period': period,
    })


@login_required
def delete_medicine(request, id):
    medicine = Medicine.objects.get(id=id, user=request.user)
    MedicineLog.objects.filter(medicine=medicine).delete()
    medicine.delete()
    return redirect('/dashboard/')


@login_required
def mark_status(request, id, status):
    medicine     = Medicine.objects.get(id=id, user=request.user)
    today        = timezone.localdate()
    existing_log = MedicineLog.objects.filter(medicine=medicine, date=today).last()

    if existing_log:
        if existing_log.status == status:
            return redirect(f'/dashboard/?info=already_{status}&med={medicine.name}')
        if request.method == 'POST' and request.POST.get('confirmed') == '1':
            existing_log.status = status
            existing_log.save()
            return redirect(f'/dashboard/?undo_id={existing_log.id}&undo_status={existing_log.status}&med={medicine.name}')
        return render(request, 'confirm_status.html', {
            'medicine': medicine,
            'existing_status': existing_log.status,
            'new_status': status,
        })

    new_log = MedicineLog.objects.create(medicine=medicine, status=status)
    return redirect(f'/dashboard/?undo_id={new_log.id}&undo_status={new_log.status}&med={medicine.name}')


@login_required
def undo_last_log(request, log_id):
    today = timezone.localdate()
    try:
        log = MedicineLog.objects.get(id=log_id, medicine__user=request.user, date=today)
        log.delete()
    except MedicineLog.DoesNotExist:
        pass
    return redirect('/dashboard/')


@login_required
def add_caregiver(request):
    error = ""
    if request.method == "POST":
        name  = request.POST['name'].strip()
        email = request.POST['email'].strip()
        phone = request.POST.get('phone', '').strip()

        if not all([name, email, phone]):
            error = "All fields are required."
        elif len(name) < 2 or len(name) > 50:
            error = "Name must be 2–50 characters."
        elif not all(c.isalpha() or c.isspace() for c in name):
            error = "Name can contain only letters and spaces."
        elif "@" not in email or "." not in email:
            error = "Enter a valid email address."
        elif not is_valid_phone(phone):
            error = "Enter a valid phone number (10–15 digits, optionally starting with +)."
        else:
            Caregiver.objects.update_or_create(
                user=request.user,
                defaults={'name': name, 'email': email, 'phone': phone}
            )
            return redirect('/dashboard/')

    return render(request, 'add_caregiver.html', {'error': error})


@login_required
def view_caregiver(request):
    caregiver = Caregiver.objects.filter(user=request.user).first()
    return render(request, 'view_caregiver.html', {'caregiver': caregiver})


@login_required
def delete_caregiver(request):
    Caregiver.objects.filter(user=request.user).delete()
    return redirect('/dashboard/')


@login_required
def medicine_history(request):
    from datetime import timedelta
    medicines = Medicine.objects.filter(user=request.user)
    today     = timezone.localdate()
    days      = [today - timedelta(days=i) for i in range(29, -1, -1)]

    history_data = []
    for medicine in medicines:
        logs_qs = MedicineLog.objects.filter(
            medicine=medicine,
            date__gte=days[0],
            date__lte=today
        )
        log_map      = {log.date: log.status for log in logs_qs}
        row          = []
        taken_count  = 0
        missed_count = 0
        for d in days:
            status = log_map.get(d, 'none')
            if status == 'taken':
                taken_count += 1
            elif status == 'missed':
                missed_count += 1
            row.append({'date': d, 'status': status})

        history_data.append({
            'medicine':     medicine,
            'row':          row,
            'taken_count':  taken_count,
            'missed_count': missed_count,
        })

    return render(request, 'medicine_history.html', {
        'history_data': history_data,
        'days':         days,
    })


@login_required
def reports(request):
    from datetime import timedelta
    medicines = Medicine.objects.filter(user=request.user)
    today     = timezone.localdate()
    days_30   = [today - timedelta(days=i) for i in range(29, -1, -1)]
    days_7    = [today - timedelta(days=i) for i in range(6, -1, -1)]

    report_data  = []
    total_taken  = 0
    total_missed = 0

    for medicine in medicines:
        first_log  = MedicineLog.objects.filter(medicine=medicine).order_by('date').first()
        start_date = first_log.date if first_log else today

        logs_qs  = MedicineLog.objects.filter(medicine=medicine, date__gte=days_30[0], date__lte=today)
        log_map  = {log.date: log.status for log in logs_qs}

        relevant_days = [d for d in days_30 if d >= start_date]
        taken      = sum(1 for d in relevant_days if log_map.get(d) == 'taken')
        missed     = sum(1 for d in relevant_days if log_map.get(d) == 'missed')
        not_logged = len(relevant_days) - taken - missed

        total_taken  += taken
        total_missed += missed

        last7 = []
        for d in days_7:
            last7.append({
                'date':      d.strftime('%d %b'),
                'day_short': d.strftime('%a')[:1],
                'status':    log_map.get(d, 'none'),
            })

        report_data.append({
            'medicine':   medicine,
            'taken':      taken,
            'missed':     missed,
            'not_logged': not_logged,
            'total':      taken + missed,
            'last7':      last7,
        })

    grand_total = total_taken + total_missed
    overall_adherence = round((total_taken / grand_total) * 100) if grand_total > 0 else 0

    return render(request, 'reports.html', {
        'report_data':        report_data,
        'total_taken':        total_taken,
        'total_missed':       total_missed,
        'overall_adherence':  overall_adherence,
    })


@login_required
def profile(request):
    from django.contrib.auth import update_session_auth_hash
    user    = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    taken_count  = MedicineLog.objects.filter(medicine__user=user, status='taken').count()
    missed_count = MedicineLog.objects.filter(medicine__user=user, status='missed').count()

    success = pwd_success = error = pwd_error = ""

    if request.method == "POST":
        # Password change form
        if request.POST.get('change_password'):
            current  = request.POST.get('current_password', '')
            new_pwd  = request.POST.get('new_password', '')
            confirm  = request.POST.get('confirm_password', '')

            if not user.check_password(current):
                pwd_error = "Current password is incorrect."
            elif len(new_pwd) < 8:
                pwd_error = "New password must be at least 8 characters."
            elif not any(c.isalpha() for c in new_pwd) or not any(c.isdigit() for c in new_pwd):
                pwd_error = "Password must contain both letters and numbers."
            elif new_pwd != confirm:
                pwd_error = "Passwords do not match."
            else:
                user.set_password(new_pwd)
                user.save()
                update_session_auth_hash(request, user)
                pwd_success = "Password updated successfully."

        # Profile update form
        else:
            first_name = request.POST.get('first_name', '').strip()
            last_name  = request.POST.get('last_name', '').strip()
            username   = request.POST.get('username', '').strip()
            email      = request.POST.get('email', '').strip()
            phone      = request.POST.get('phone', '').strip()

            if not username or not email:
                error = "Username and email are required."
            elif len(username) < 3 or len(username) > 20:
                error = "Username must be 3–20 characters."
            elif not username.replace("_", "").isalnum():
                error = "Username can only contain letters, numbers, underscore."
            elif "@" not in email or "." not in email:
                error = "Enter a valid email address."
            elif phone and not is_valid_phone(phone):
                error = "Enter a valid phone number."
            elif User.objects.filter(username=username).exclude(pk=user.pk).exists():
                error = "That username is already taken."
            elif User.objects.filter(email=email).exclude(pk=user.pk).exists():
                error = "That email is already registered."
            else:
                user.first_name = first_name
                user.last_name  = last_name
                user.username   = username
                user.email      = email
                user.save()
                profile.phone = phone
                profile.save()
                success = "Profile updated successfully."

    return render(request, 'profile.html', {
        'profile':      profile,
        'taken_count':  taken_count,
        'missed_count': missed_count,
        'success':      success,
        'error':        error,
        'pwd_success':  pwd_success,
        'pwd_error':    pwd_error,
    })
