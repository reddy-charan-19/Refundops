import sys
sys.stdout.reconfigure(line_buffering=True)
import bot

print("Starting Indigo test...", flush=True)
bot.start_indigo_process("TEST99")
print("Test complete!", flush=True)
