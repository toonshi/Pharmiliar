from django.db import models


class Insurance(models.Model):
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='insurances')
    insurance_name = models.CharField(verbose_name="InsuranceName", max_length=255)
    # Add other insurance-related fields as needed

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'hospitals'


class Institution(models.Model):
   

    user_profile = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE,  default=None, null=True)

    institution_id = models.AutoField(primary_key=True, verbose_name="InstitutionId", unique=True)
    institution_name = models.CharField(verbose_name="InstitutionName", max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    address = models.CharField(verbose_name="Address", max_length=100, null=True, blank=True)
    town = models.CharField(verbose_name="Town/City", max_length=100, null=True, blank=True)
    county = models.CharField(verbose_name="County", max_length=100, null=True, blank=True)
    postal_code = models.CharField(verbose_name="Post Code", max_length=8, null=True, blank=True)
    country = models.CharField(verbose_name="Country", max_length=100, null=True, blank=True)
    longitude = models.CharField(verbose_name="Longitude", max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude", max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    phone_number =  models.CharField(verbose_name="Post Code", max_length=16, null=True, blank=True)
    
    def __str__(self):
        return self.institution_name


class Service(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, related_name='services')
    service_name = models.CharField(max_length=255)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.service_name} - {self.institution.institution_name}"


class UserReview(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE,related_name='hospitals_user_reviews')
    review = models.TextField()
    review_image = models.ImageField(upload_to='review_images/')

    def __str__(self):
        return f"{self.review} - {self.institution.institution_name}"
