def get_ip(request):
    ip = None
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
    else:
        ip = request.META['REMOTE_ADDR']
    return ip