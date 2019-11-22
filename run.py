from app import create_app, BaseConfig

app = create_app(BaseConfig)

if __name__ == '__main__':
    app.run()
