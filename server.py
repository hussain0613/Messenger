#if __name__ == '__main__':
#    from .app import create_app
#    app = create_app()
#    app.run(debug=True, threaded = True)
#else:
#    from app import create_app
#    app = create_app()

from app import create_app
app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
