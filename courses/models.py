from django.db import models
from accounts.models import User 

class Course(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ), default='pending')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} ({self.status})"



class SavedCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')
    
    def __str__(self):
        return f"{self.student.username} saved {self.course.title}"


class EnrolledCourse(models.Model): 
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.student.username} successfully enrolled in {self.course.title}"


class AcceptedEnrollment(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='accepted_status')
    accepted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Accepted: {self.enrollment.student.username} for {self.enrollment.course.title}"


class RejectedEnrollment(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='rejected_status')
    rejected_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rejected: {self.enrollment.student.username} for {self.enrollment.course.title}"
