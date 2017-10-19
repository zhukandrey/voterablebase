from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from users.models import PUser
from django.contrib import messages

# from sellers.mixins import SellerAccountMixin

# class ProductManagerMixin(object):
#     def get_object(self, *args, **kwargs):
#         obj = super(ProductManagerMixin, self).get_object(*args, **kwargs)
#         user = self.request.user
#         if obj.user == user:
#             return obj
#         else:
#             raise Http404

class LoginRequiredMixin(object):
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class UserChangeManagerMixin(object):
		def get_object(self, *args, **kwargs):
				obj = super(UserChangeManagerMixin, self).get_object(*args, **kwargs)
				user = self.request.user
				if obj.user == user:
						return obj
				else:
						raise Http404
