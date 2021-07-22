from .views import createCycles

def cycle_router(request):
    return createCycles(request)