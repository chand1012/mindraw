import os
import asyncio
import base64
import io
import uuid

from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
from loguru import logger as log

from sdapi import SDAPIAsync

load_dotenv()

TESTING_GUILD_ID = int(os.getenv('TESTING_GUILD_ID', '0')
                       )  # Replace with your guild ID
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DEFAULT_NEGATIVE_PROMPT = 'ugly cartoon 3d disfigured bad art deformed poorly drawn extra limbs close up b&w weird colors blurry cropped out of frame'
# if no TESTING_GUILD_ID is set, then the bot will be global
FORCE_GLOBAL = TESTING_GUILD_ID == 0

bot = commands.Bot()
sd = SDAPIAsync(os.getenv('SD_API_URL', 'http://localhost:8000'))


@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user.name}#{bot.user.discriminator}")


@bot.slash_command(description="Generates 4 images with balanced options", guild_ids=[TESTING_GUILD_ID], force_global=FORCE_GLOBAL)
async def imagine(interaction: nextcord.Interaction, prompt: str):
    if len(prompt) == 0:
        raise commands.errors.MissingRequiredArgument(prompt)
    log.info(f"Generating image with prompt: {prompt}")
    # send a message that the images are being generated
    m = await interaction.response.send_message("Generating images...")
    # async generate 4 images
    # need to call sd.generate_image() 4 times
    # then send the images
    opts = {
        'height': 512,
        'width': 512,
    }
    if 'portrait' in prompt:
        opts['height'] = 768
    elif 'landscape' in prompt or 'background' in prompt:
        opts['width'] = 768
    if 'background' in prompt:
        prompt.replace('background', '')
    tasks = []
    for _ in range(4):
        tasks.append(sd.generate_image(model="ssd-1b", prompt=prompt,
                     guidance_scale=9, negative_prompt=DEFAULT_NEGATIVE_PROMPT, num_inference_steps=30, **opts))

    files = []
    results = await asyncio.gather(*tasks)
    for img_resp in results:
        data = io.BytesIO(base64.b64decode(img_resp['b64_json']))
        files.append(nextcord.File(data, filename=f'{uuid.uuid4()}.jpg'))
    await interaction.channel.send(files=files)
    await m.edit(f'Generated images for prompt: `{prompt}`')
    log.info(f'Finished.')


@imagine.error
async def imagine_error(ctx, error):
    log.error(f"Error in imagine: {error}")
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("Missing required argument: `prompt`")
    else:
        await ctx.send("Error generating image. Please try again later.")


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
