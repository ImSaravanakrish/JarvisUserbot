"""Get the info your system. Using .neofetch then .sysd"""

# .spc command is ported from  alfianandaa/ProjectAlf
import platform
import sys
from datetime import datetime

import psutil
from telethon import __version__

from jarvis import ALIVE_NAME, CMD_HELP
from jarvis.utils import admin_cmd, edit_or_reply, sudo_cmd

import asyncio
import os
import shlex
from os import getcwd
from os.path import basename, join
from textwrap import wrap
from typing import Optional, Tuple

import numpy as np

try:
    from colour import Color as asciiColor
except:
    os.system("pip install colour")
from PIL import Image, ImageDraw, ImageFont
from telethon.errors.rpcerrorlist import YouBlockedUserError
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image as jimage


MARGINS = [50, 150, 250, 350, 450]

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
# ============================================

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

@jarvis.on(admin_cmd(outgoing=True, pattern=r"spc$"))
async def psu(event):
    uname = platform.uname()
    softw = "**System Information**\n"
    softw += f"`System   : {uname.system}`\n"
    softw += f"`Release  : {uname.release}`\n"
    softw += f"`Version  : {uname.version}`\n"
    softw += f"`Machine  : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Boot Time: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**CPU Info**\n"
    cpuu += "`Physical cores   : " + str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores      : " + str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "**Total CPU Usage**\n"
    cpuu += f"`All Core: {psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**Memory Usage**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)}`\n"
    memm += f"`Percentage: {svmem.percent}%`\n"
    # Bandwidth Usage
    bw = "**Bandwith Usage**\n"
    bw += f"`Upload  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "**Engine Info**\n"
    help_string += f"`Python {sys.version}`\n"
    help_string += f"`Telethon {__version__}`"
    await event.edit(help_string)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@jarvis.on(admin_cmd(pattern="cpu$"))
@jarvis.on(sudo_cmd(pattern="cpu$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    cmd = "cat /proc/cpuinfo | grep 'model name'"
    o = (await runcmd(cmd))[0]
    await edit_or_reply(
        event, f"**[Cat's](tg://need_update_for_some_feature/) CPU Model:**\n{o}"
    )


@jarvis.on(admin_cmd(pattern=f"sysd$", outgoing=True))
@jarvis.on(sudo_cmd(pattern=f"sysd$", allow_sudo=True))
async def sysdetails(sysd):
    cmd = "git clone https://github.com/dylanaraps/neofetch.git"
    await runcmd(cmd)
    neo = "neofetch/neofetch --off --color_blocks off --bold off --cpu_temp C \
                    --cpu_speed on --cpu_cores physical --kernel_shorthand off --stdout"
    a, b, c, d = await runcmd(neo)
    result = str(a) + str(b)
    await edit_or_reply(sysd, "Neofetch Result: `" + result + "`")


CMD_HELP.update(
    {
        "sysdetails": "**Plugin : **`sysdetails`\
        \n\n**Syntax : **`.spc`\
        \n**Function : **__Show system specification.__\
        \n\n**Syntax : **`.sysd`\
        \n**Function : **__Shows system information using neofetch.__\
        \n\n**Syntax : **`.cpu`\
        \n**Function : **__shows the cpu information__\
    "
    }
)
