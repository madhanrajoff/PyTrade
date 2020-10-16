from app import AppFactory

app_config = AppFactory.create_app()

if app_config:
    # start the application.
    from py_trade_svc import PyTradeSvc
    PyTradeSvc.start()
