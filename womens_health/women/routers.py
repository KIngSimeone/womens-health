from .views import createCycles, cycleEvent

def cycle_router(request):
    return createCycles(request)

def cycle_event_router(request):
    return cycleEvent(request)