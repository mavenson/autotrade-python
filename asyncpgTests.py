import asyncio
import asyncpg
import json

# async def run():
#     conn = await asyncpg.connect(user='mavenson', password='mast3rofdisast3r',
#                                  database='mavenson', host='127.0.0.1')
#     values = await conn.fetch('''SELECT * FROM mave_table''')
#     print(values)
#     await conn.close()

async def main():
    conn = await asyncpg.connect(user='mavenson', password='mast3rofdisast3r',
                                 database='mavenson', host='127.0.0.1')

    try:
        def _encoder(value):
            return b'\x01' + json.dumps(value).encode('utf-8')

        def _decoder(value):
            return json.loads(value[1:].decode('utf-8'))

        await conn.set_type_codec(
            'jsonb',
            schema='pg_catalog',
            encoder=_encoder,
            decoder=_decoder,
            format='binary'
            )

        msg = await conn.fetchrow('SELECT id, msg FROM rsp_msg_repo WHERE id = 1')
        result = await conn.fetchval('SELECT $1::jsonb', dict(msg))
        print(result['msg'])

    finally:
        await conn.close()



asyncio.get_event_loop().run_until_complete(main())