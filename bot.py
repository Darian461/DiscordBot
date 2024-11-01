import interactions
import asyncio

bot = interactions.Client(
    intents=interactions.Intents.DEFAULT,
    token='',

)

@interactions.listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@interactions.listen()
async def on_message_create(event):
    # This event is called when a message is sent in a channel the bot can see
    print(f"message received: {event.message.jump_url}")

@interactions.slash_command(name="my_command", description="My first command :)")
async def my_command_function(ctx: interactions.SlashContext):
    await ctx.send("Hello World")



@interactions.slash_command(name = "record", description = "record some audio")
async def record(ctx: interactions.SlashContext):
    await ctx.defer()
    voice_state = await ctx.author.voice.channel.connect()

    # Reply with starting record and record for 5 seconds
    #await ctx.send("started Record")
    await voice_state.start_recording(
        output_dir='Voices',
        encoding="wav"
    )

    await asyncio.sleep(10)
    await voice_state.stop_recording()
    await ctx.send(files=[interactions.File(file, file_name=str(ctx.client.get_user(user_id)) + ".wav") for user_id, file in voice_state.recorder.output.items()])
    await ctx.author.voice.channel.disconnect()

bot.start()
