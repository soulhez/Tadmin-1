from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import APIException
from rest_framework import status

# class BusinessValidationError(ValidationError):
#
#     def __init__(self, detail):
#         self.detail = {
#             "code":detail[0],
#             "msg":detail[1]
#         }
#         super(BusinessValidationError, self).__init__(self.detail)