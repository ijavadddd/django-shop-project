from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
	def create_user(self, phone_number, first_name, last_name, password, profile_img=None, date_of_birth=None, email=None):
		if not phone_number:
			raise ValueError('user must have phone number')

		user = self.model(
                        phone_number=phone_number,
                        email=self.normalize_email(email), 
                        first_name=first_name, 
                        last_name=last_name,
						date_of_birth=date_of_birth,
						profile_img=profile_img)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, first_name, last_name, password):
		user = self.create_user(phone_number, first_name, last_name, password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user
