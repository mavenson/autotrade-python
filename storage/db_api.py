import asyncpg
import json

class DbApi:
    def __init__(self):
        self._rsp_msg = None
        self._conn = None

    async def connect(self):
        self._conn = await asyncpg.connect('postgresql://at_db:Kr3sa1!@localhost/at_db')

    def _encoder(self, value):
        return b'\x01' + json.dumps(value).encode('utf-8')

    def _decoder(self, value):
        return json.loads(value[1:].decode('utf-8'))

    async def save_to_repo(self, msg):
        try:
            await conn.set_type_codec\
                (
                'jsonb',
                schema='pg_catalog',
                encoder=self._encoder,
                decoder=self._decoder,
                format='binary'
                )
            self._rsp_msg = msg
            await conn.execute('INSERT INTO rsp_msg_repo VALUES (DEFAULT, $1, (SELECT now() FROM CURRENT_TIMESTAMP))',
                         msg)
            result = await conn.fetchval('SELECT $1::jsonb', dict(msg))
            print(result)

        finally:
            await conn.close()