#  (c)2020 Telebot
#
# You may not use this plugin without proper authorship and consent from @TelebotSupport
#
import asyncio
import os

from userbot.utils import admin_cmd

FBAN_GROUP_ID = os.environ.get("FBAN_GROUP_ID", None)
if FBAN_GROUP_ID:
    FBAN_GROUP_ID = int(FBAN_GROUP_ID)
EXCLUDE_FED = os.environ.get("EXCLUDE_FED", None)

# By @HeisenbergTheDanger, @its_xditya
@bot.on(admin_cmd("superfban ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Starting a Mass-FedBan...")
    fedList = []
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await event.client.download_media(
                previous_message, "fedlist"
            )
            await asyncio.sleep(6)
            file = open(downloaded_file_name, "r")
            lines = file.readlines()
            for line in lines:
                try:
                    fedList.append(line[:36])
                except:
                    pass
            arg = event.pattern_match.group(1)
            args = arg.split()
            if len(args) > 1:
                FBAN = args[0]
                REASON = ""
                for a in args[1:]:
                    REASON += a + " "
            else:
                FBAN = arg
                REASON = " #MassBanned "
        else:
            FBAN = previous_message.sender_id
            REASON = event.pattern_match.group(1)
            if REASON.strip() == "":
                REASON = " #MassBanned "
    else:
        arg = event.pattern_match.group(1)
        args = arg.split()
        if len(args) > 1:
            FBAN = args[0]
            REASON = ""
            for a in args[1:]:
                REASON += a + " "
        else:
            FBAN = arg
            REASON = " #MassBanned "
    try:
        int(FBAN)
        if int(FBAN) == 1118936839:
            await event.edit("Something went wrong.")
            return
    except:
        if FBAN == "@Surv_ivor" or FBAN == "@Sur_ivor":
            await event.edit("Something went wrong.")
            return
    if FBAN_GROUP_ID:
        chat = FBAN_GROUP_ID
    else:
        chat = await event.get_chat()
    if not len(fedList):
        for a in range(3):
            async with event.client.conversation("@MissRose_bot") as bot_conv:
                await bot_conv.send_message("/start")
                await bot_conv.send_message("/myfeds")
                await asyncio.sleep(3)
                response = await bot_conv.get_response()
                await asyncio.sleep(3)
                if "make a file" in response.text:
                    await asyncio.sleep(6)
                    await response.click(0)
                    await asyncio.sleep(6)
                    fedfile = await bot_conv.get_response()
                    await asyncio.sleep(3)
                    if fedfile.media:
                        downloaded_file_name = await event.client.download_media(
                            fedfile, "fedlist"
                        )
                        await asyncio.sleep(6)
                        file = open(downloaded_file_name, "r")
                        lines = file.readlines()
                        for line in lines:
                            try:
                                fedList.append(line[:36])
                            except:
                                pass
                    else:
                        return
                if len(fedList) == 0:
                    await event.edit(f"Something went wrong. Retrying ({a+1}/3)...")
                else:
                    break
        else:
            await event.edit(f"Error")
        if "You can only use fed commands once every 5 minutes" in response.text:
            await event.edit("Try again after 5 mins.")
            return
        In = False
        tempFedId = ""
        for x in response.text:
            if x == "`":
                if In:
                    In = False
                    fedList.append(tempFedId)
                    tempFedId = ""
                else:
                    In = True

            elif In:
                tempFedId += x
        if len(fedList) == 0:
            await event.edit("Something went wrong.")
            return
    await event.edit(f"Fbaning in {len(fedList)} feds.")
    try:
        await event.client.send_message(chat, f"/start")
    except:
        await event.edit("FBAN_GROUP_ID is incorrect.")
        return
    await asyncio.sleep(3)
    if EXCLUDE_FED:
        excludeFed = EXCLUDE_FED.split("|")
        for n in range(len(excludeFed)):
            excludeFed[n] = excludeFed[n].strip()
    exCount = 0
    for fed in fedList:
        if EXCLUDE_FED and fed in excludeFed:
            await event.client.send_message(chat, f"{fed} Excluded.")
            exCount += 1
            continue
        await event.client.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await event.client.send_message(chat, f"/fban {FBAN} {REASON}")
        await asyncio.sleep(3)
    await event.edit(f"SuperFBan Completed. Affected {len(fedList) - exCount} feds.")


# By @HeisenbergTheDanger, @its_xditya
@bot.on(admin_cmd("superunfban ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Starting a Mass-UnFedBan...")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        FBAN = previous_message.sender_id
    else:
        FBAN = event.pattern_match.group(1)

    if FBAN_GROUP_ID:
        chat = FBAN_GROUP_ID
    else:
        chat = await event.get_chat()
    fedList = []
    for a in range(3):
        async with event.client.conversation("@MissRose_bot") as bot_conv:
            await bot_conv.send_message("/start")
            await bot_conv.send_message("/myfeds")
            response = await bot_conv.get_response()
            if "make a file" in response.text:
                await asyncio.sleep(1)
                await response.click(0)
                fedfile = await bot_conv.get_response()
                if fedfile.media:
                    downloaded_file_name = await event.client.download_media(
                        fedfile, "fedlist"
                    )
                    file = open(downloaded_file_name, "r")
                    lines = file.readlines()
                    for line in lines:
                        fedList.append(line[: line.index(":")])
                else:
                    return
                if len(fedList) == 0:
                    await event.edit(f"Something went wrong. Retrying ({a+1}/3)...")
                else:
                    break
    else:
        await event.edit(f"Error")
    if "You can only use fed commands once every 5 minutes" in response.text:
        await event.edit("Try again after 5 mins.")
        return
    In = False
    tempFedId = ""
    for x in response.text:
        if x == "`":
            if In:
                In = False
                fedList.append(tempFedId)
                tempFedId = ""
            else:
                In = True

        elif In:
            tempFedId += x

    await event.edit(f"UnFbaning in {len(fedList)} feds.")
    try:
        await event.client.send_message(chat, f"/start")
    except:
        await event.edit("FBAN_GROUP_ID is incorrect.")
        return
    await asyncio.sleep(3)
    for fed in fedList:
        await event.client.send_message(chat, f"/joinfed {fed}")
        await asyncio.sleep(3)
        await event.client.send_message(chat, f"/unfban {FBAN}")
        await asyncio.sleep(3)
    await event.edit(f"SuperUnFBan Completed. Affected {len(fedList)} feds.")
