from server import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0', # 모든 ip가 나에게 접속 가능
        port="6789",
        debug=True,
    )