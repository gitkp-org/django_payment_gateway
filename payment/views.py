from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView
from django.contrib import messages
from payment.models import Payment
import braintree
# Create your views here.

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Sandbox,
    merchant_id='MERCHANT ID',
    public_key='PUBLIC KEY',
    private_key='PRIVATE KEY'
  )
)


def payment_form(request):
    template_name = 'index.html'
    # context = {"braintree_client_token":gateway.client_token.generate()}
    return render(request,template_name)


def generate_token(request):
    if request.method == 'POST':
        braintree_client_token = gateway.client_token.generate()
        return JsonResponse({"braintree_client_token": braintree_client_token, "ammount": request.POST['ammount']})


def process_payment(request):
    nonce_from_the_client = request.POST['paymentMethodNonce']
    ammount_from_the_client = request.POST['ammount']

    result = gateway.transaction.sale({
        "amount": ammount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
          "submit_for_settlement": True
        }
    })

    Payment.objects.create(user_id=request.user.id , ammount=ammount_from_the_client, transaction_id=result.transaction.id, status=result.is_success)

    if result.is_success:
        messages.add_message(request, messages.SUCCESS, 'Your Payment of {ammount_from_the_client} INR is successful, You transaction ID is {result.transaction.id}')
        
    else:
        messages.add_message(request, messages.ERROR, 'Your Payment of {ammount_from_the_client} INR is failed, You transaction ID is {result.transaction.id}')

    return redirect('',request)