from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Enrollment, SavedCourse, EnrolledCourse, AcceptedEnrollment, RejectedEnrollment
from .forms import CoursePostingForm, EnrollmentForm

def is_instructor(user):
    return user.is_authenticated and user.user_type == 'I'

def is_student(user):
    return user.is_authenticated and user.user_type == 'S'

@login_required
def course_create(request):
    if not is_instructor(request.user):
        messages.error(request, "Only instructors can create courses.")
        return redirect('home')
    
    if request.method == 'POST':
        form = CoursePostingForm(request.POST, request.FILES)  # Add request.FILES
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, "Course created successfully!")
            return redirect('my_courses')
    else:
        form = CoursePostingForm()
    return render(request, 'courses/course_create.html', {'form': form})


@login_required
def my_courses(request):
    if not is_instructor(request.user):
        messages.error(request, "Only instructors can view their courses.")
        return redirect('home')
    
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/my_courses.html', {'courses': courses})

@login_required
def view_enrollments(request, course_id):
    if not is_instructor(request.user):
        messages.error(request, "Only instructors can view enrollments.")
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    enrollments = Enrollment.objects.filter(course=course)
    
    context = {
        'course': course,
        'enrollments': enrollments
    }
    return render(request, 'courses/view_enrollments.html', context)

@login_required
def enrollment_details(request, enrollment_id):
    if not is_instructor(request.user):
        messages.error(request, "Only instructors can view enrollment details.")
        return redirect('home')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if enrollment.course.instructor != request.user:
        messages.error(request, "You can only view enrollments for your own courses.")
        return redirect('my_courses')
    
    context = {
        'enrollment': enrollment
    }
    return render(request, 'courses/enrollment_details.html', context)

@login_required
def accept_enrollment(request, enrollment_id):
    if not is_instructor(request.user):
        messages.error(request, "Only instructors can accept enrollments.")
        return redirect('home')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if enrollment.course.instructor != request.user:
        messages.error(request, "You can only manage enrollments for your own courses.")
        return redirect('my_courses')
    
    AcceptedEnrollment.objects.create(enrollment=enrollment)
    EnrolledCourse.objects.create(
        student=enrollment.student,
        course=enrollment.course
    )
    messages.success(request, f"Enrollment accepted for {enrollment.student.username}")
    return redirect('view_enrollments', course_id=enrollment.course.id)

@login_required
def reject_enrollment(request, enrollment_id):
    if not is_instructor(request.user):
        messages.error(request, "Only instructors can reject enrollments.")
        return redirect('home')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if enrollment.course.instructor != request.user:
        messages.error(request, "You can only manage enrollments for your own courses.")
        return redirect('my_courses')
    
    
    RejectedEnrollment.objects.create(enrollment=enrollment)
    messages.success(request, f"Enrollment rejected for {enrollment.student.username}")
    return redirect('view_enrollments', course_id=enrollment.course.id)

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_saved = False
    
    if request.user.is_authenticated and request.user.user_type == 'S':
        is_saved = SavedCourse.objects.filter(student=request.user, course=course).exists()
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_saved': is_saved
    })

@login_required
def enroll_course(request, course_id):
    if not is_student(request.user):
        messages.error(request, "Only students can enroll in courses.")
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id)
    

    existing_enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
    if existing_enrollment:
        messages.warning(request, "You have already applied for this course!")
        return redirect('course_detail', course_id=course_id)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = request.user
            enrollment.course = course
            enrollment.save()
            messages.success(request, "Your enrollment request has been submitted!")
            return redirect('course_detail', course_id=course.id)
        else:
            messages.error(request, "Error submitting enrollment. Please check the form.")
    else:
        form = EnrollmentForm()
    
    return render(request, 'courses/enroll_course.html', {'course': course, 'form': form})

@login_required
def my_enrolled_courses(request):
    if not is_student(request.user):
        messages.error(request, "Only students can view enrolled courses.")
        return redirect('home')
    
    enrolled_courses = EnrolledCourse.objects.filter(student=request.user)
    return render(request, 'courses/my_enrolled_courses.html', {'enrolled_courses': enrolled_courses})

@login_required
def saved_courses(request):
    if not is_student(request.user):
        messages.error(request, "Only students can view saved courses.")
        return redirect('home')
    
    saved_courses = SavedCourse.objects.filter(student=request.user)
    return render(request, 'courses/saved_courses.html', {'saved_courses': saved_courses})

@login_required
def toggle_save_course(request, course_id):
    if request.user.user_type != 'S':
        messages.error(request, "Only students can save courses.")
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id)
    saved_course, created = SavedCourse.objects.get_or_create(
        student=request.user,
        course=course
    )
    
    if not created:
        saved_course.delete()
        messages.info(request, "Course removed from saved list.")
    else:
        messages.success(request, "Course saved successfully!")
    
    return redirect('course_detail', course_id=course_id)

@login_required
def accept_enrollment(request, enrollment_id):
    if not is_instructor(request.user):
        messages.error(request, "Only instructors can accept enrollments.")
        return redirect('home')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if enrollment.course.instructor != request.user:
        messages.error(request, "You can only manage enrollments for your own courses.")
        return redirect('my_courses')
    
 
    enrollment.status = 'accepted'
    enrollment.save()
    
  
    EnrolledCourse.objects.get_or_create(student=enrollment.student, course=enrollment.course)
    
    messages.success(request, f"Enrollment accepted for {enrollment.student.username}")
    return redirect('view_enrollments', course_id=enrollment.course.id)

@login_required
def reject_enrollment(request, enrollment_id):
    if not is_instructor(request.user):
        messages.error(request, "Only instructors can reject enrollments.")
        return redirect('home')
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if enrollment.course.instructor != request.user:
        messages.error(request, "You can only manage enrollments for your own courses.")
        return redirect('my_courses')
    
    
    enrollment.status = 'rejected'
    enrollment.save()
    
    messages.success(request, f"Enrollment rejected for {enrollment.student.username}")
    return redirect('view_enrollments', course_id=enrollment.course.id)

