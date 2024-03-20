from django.http import request

def get_request_data(request, **kwargs):
    body = request.data.copy()  # Assuming you're using form data
    params = request.GET.copy()

    # Combine request body, params, and additional kwargs into a single dictionary
    combined_data = {**body, **params, **kwargs}
    print(combined_data)
    return combined_data