import discord


def get_server_info(guild: discord.Guild) -> str:
    if guild is None:
        return "No server."

    info = []

    info.append(f"Server: {guild.name}")
    info.append(f"Server ID: {guild.id}")

    info.append("\nCategories:")
    for category in guild.categories:
        info.append(f"- {category.name} ({category.id})")

    info.append("\nChannels:")
    for channel in guild.channels:
        info.append(f"- {channel.name} ({channel.id})")

    info.append("\nRoles:")
    for role in guild.roles:
        info.append(
            f"- Pos: {role.position} | {role.name} ({role.id})"
        )

    return "\n".join(info)
