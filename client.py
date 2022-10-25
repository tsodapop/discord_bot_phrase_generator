import os

import discord
from discord import Member, VoiceState


class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f"{self.user} is running!")

    async def on_message(self, message):
        if message.content == "ping":
            await message.channel.send("pong")

    async def on_voice_state_update(self, member: Member, before: VoiceState,
                                    after: VoiceState):
        """
        when a user has their "voice state" updated - when they enter/exit a voice channel
        """
        def joined_channel(voice_state: VoiceState = after):
            """
            when the voice state update is that a user has joined a channel

            args:
                voice_state - the VoiceState to test against
            returns:
                bool - true if the VoiceState has a channel
            """
            if voice_state.channel is not None:
                return True
            return False

        def left_channel(voice_state: VoiceState = after):
            """
            when the voice state update is that a user has left a channel

            args:
                voice_state - the VoiceState to test against
            returns:
                bool - true if the VoiceState has a channel
            """
            if voice_state.channel is not None:
                return False
            return True

        if joined_channel():
            await after.channel.send(f"send message here for entering")

        elif left_channel():
            await before.channel.send(f"Send message here for leaving")


def create_client(intents=discord.Intents.default()):
    """
    creates a Discord client and returns the object back

    args:
        intents: set to default intents. can be modified to different permissions
    returns:
        a client object
    """
    def update_intents(intents: discord.Intents, message_content: bool = True):
        """
        updates intents with specified params
        """
        intents.message_content = message_content
        return intents

    intents = update_intents(intents)
    client = DiscordClient(intents=intents)
    return client


def fetch_token(token_name="discord_token"):
    """
    fetches and returns the local discord bot token under the set environment variable. 
    this needs to be set beforehand.
    
    if it cannot find the token, throws an exception
    """
    # token = os.environ.get(token_name)
    token = os.environ.get("discord_token")
    token = "INSERTTOKENHERE"
    if token is None:
        raise Exception(
            f"Could not find token under variable name '{token_name}'")
    return token


def run_discord_bot():
    """
    fetches the discord client token and begins running the client
    """
    token = fetch_token("discord_token")
    print(token)
    client = create_client()

    client.run(token)


if __name__ == "__main__":
    run_discord_bot()
