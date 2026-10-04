from django.http import request


def get_request_data(request, **kwargs):
    body = request.data.copy()
    params = request.GET.dict()

    # Convert body to a normal dict as well
    if hasattr(body, 'dict'):
        body = body.dict()

    # Combine request body, query params, and kwargs
    combined_data = {
        **body,
        **params,
        **kwargs,
    }

    print(combined_data)

    return combined_data
