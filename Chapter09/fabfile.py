# Code Listing #2

# Fablic は SSH によるシェルコマンドをリモート実行するための
# サードパーティー製パッケージ。
from fabric.api import run

# したがって次のコードはパッケージ application を
# pip でインストールするという処理を意味する。
def remote_install(application):

    print('Installing', application)
    run('sudo pip install ' + application)
