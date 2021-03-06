'''
Integration tests for remote.
TODO: Replace mock-ssh-server with some other alternatives.
'''

import os
from boss.core import remote, fs


def test_put(server):
    ''' Test put() transfers file to the remote end. '''
    for uid in server.users:
        source_file = os.path.join(server.ROOT_DIR, 'foo_src')
        target_file = os.path.join(server.ROOT_DIR, 'foo_dest')

        fs.write(source_file, 'Test put operation')
        assert not fs.exists(target_file)

        with server.client(uid) as client:
            sftp = client.open_sftp()
            remote.put(
                sftp,
                local_path=source_file,
                remote_path=target_file,
                confirm=True
            )
            assert fs.read(target_file) == 'Test put operation'


def test_get(server):
    ''' Test get() transfers remote file to the local. '''
    for uid in server.users:
        source_file = os.path.join(server.ROOT_DIR, 'foo_src')
        target_file = os.path.join(server.ROOT_DIR, 'foo_dest')

        fs.write(source_file, 'Test get operation')
        assert not fs.exists(target_file)

        with server.client(uid) as client:
            sftp = client.open_sftp()
            remote.get(
                sftp,
                remote_path=source_file,
                local_path=target_file
            )
            assert fs.read(target_file) == 'Test get operation'


def test_run(server):
    ''' Test run() executes a command over ssh. '''
    for uid in server.users:
        with server.client(uid) as client:
            (_, stdout, _) = remote.run(client, 'python --version')

            assert stdout.read() is not None


def test_read(server):
    ''' Test read() returns remote file contents. '''
    for uid in server.users:
        path = os.path.join(server.ROOT_DIR, 'foo_src')

        fs.write(path, 'Hello World')

        with server.client(uid) as client:
            sftp = client.open_sftp()
            result = remote.read(sftp, path)

            assert result == 'Hello World'


def test_write(server):
    ''' Test write() writes data to a remote file. '''
    for uid in server.users:
        path = os.path.join(server.ROOT_DIR, 'foo_src')

        with server.client(uid) as client:
            sftp = client.open_sftp()
            remote.write(sftp, path, data='Hello World!')

            assert fs.read(path) == 'Hello World!'


def test_write_overwrites_existing_file(server):
    ''' Test write() writes and overwrites data on a remote file. '''
    for uid in server.users:
        path = os.path.join(server.ROOT_DIR, 'foo_src')

        fs.write(path, 'Hello!')

        assert fs.read(path) == 'Hello!'

        with server.client(uid) as client:
            sftp = client.open_sftp()
            remote.write(sftp, path, data='Hello World!')

            assert fs.read(path) == 'Hello World!'


def test_cwd(server):
    ''' Test cwd() returns remote current. '''
    for uid in server.users:
        with server.client(uid) as client:
            cwd = remote.cwd(client)

            assert cwd is not None
            assert fs.exists(cwd)
