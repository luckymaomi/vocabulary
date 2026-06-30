import main


def test_main_app_is_fastapi_application():
    routes = {route.path for route in main.app.routes}

    assert "/" in routes
    assert "/health" in routes
    assert "/api/lookup" in routes
