def detect_redirect(user):
    if user.role == 1:
        redirectUrl = 'vendordashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerdashboard'
        return redirectUrl
    elif user.role == None and user.is_superuser:
        redirectUrl = '/admin'
        return redirectUrl