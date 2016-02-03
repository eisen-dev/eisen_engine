from bin import api

app = api.create_app()
test_app = app.test_client()