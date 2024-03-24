import asyncio
import cowsay

clients = {}
cowslist = cowsay.list_cows()

async def chat(reader, writer):
    user_registered = False
    me = ""
    buf = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(buf.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                mes = q.result().decode().split()
                if (len(mes) < 1):
                    continue
                elif (mes[0] == 'who'):
                    users_string = ', '.join(clients.keys())
                    writer.write(f"Registered users: {users_string}\n".encode())
                    await writer.drain()
                elif (mes[0] == 'cows'):
                    cows_string = ', '.join(cowslist)
                    writer.write(f"Free cows names: {cows_string}\n".encode())
                    await writer.drain()
                elif (mes[0] == 'login' and not(user_registered)):
                    if (mes[1] in cowslist):
                        me = mes[1]
                        print("Registered user: ", me)
                        clients[me] = asyncio.Queue()
                        cowslist.remove(mes[1])
                        writer.write("User is registered!\n".encode())
                        await writer.drain()
                        user_registered = True
                        receive.cancel()
                        receive = asyncio.create_task(clients[me].get())
                    else:
                        writer.write("Wrong cow name!\n".encode())
                        await writer.drain()
                elif (mes[0] == "say"):
                    if (not(user_registered)):
                        writer.write("Register user, please!\n".encode())
                        await writer.drain()
                        continue
                    if (mes[1] in clients.keys()):
                        await clients[mes[1]].put(f"Message from: {me}\n {cowsay.cowsay((' '.join(mes[2:])).strip(), cow=me)}")
                        writer.write("Send!\n".encode())
                        await writer.drain()
                    else:
                        writer.write("User name is wrong!\n".encode())
                        await writer.drain()
                elif (mes[0] == 'yield'):
                    if (not(user_registered)):
                        writer.write("Register user, please!\n".encode())
                        await writer.drain()
                        continue
                    for out in clients.values():
                        if out is not clients[me]:
                            await out.put(f"Message from: {me}\n {cowsay.cowsay(' '.join(mes[1:]).strip(), cow=me)}")
                    writer.write("Send!\n".encode())
                    await writer.drain()
                elif (mes[0] == "quit"):
                    send.cancel()
                    receive.cancel()
                    if user_registered:
                        del clients[me]
                        print("Unregistered user: ", me)
                        cowslist.append(me)
                    writer.close()
                    await writer.wait_closed()
                    return
                else:
                    writer.write("Wrong command!\n".encode())
                    await writer.drain()
            elif q is receive and user_registered:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())