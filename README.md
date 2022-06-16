# Manhattan
Server powering Venera.

If you want to get development updates, ask questions or get support you can contact us via our Discord Server or IRC Channel.

- Discord: [discord.gg/V7n95jcX2U](https://discord.gg/V7n95jcX2U).
- IRC Channel: #venera on irc.libera.chat.

# design
Feature Design Document for Manhattan.

Manhattan is written in Python and JavaScript.
Manhattan uses FastAPI for HTTP Handling, Mako for HTML Templating, Cassandra for DB Storage and many other tools.

## Venerette/Subera
A Subera (or, "Venerette") is a Place where you can create posts, label those posts, add admins, and many more things.

Users can join Venerettes and interact with them using `/v/{venerette_name}` in the API and Website(soon).

These Venerettes and ones with similar topics and likings would be put together to curate multiple recommendation feeds.
Some being:

- Newest Joined Venerette Posts
- Hot Posts
- Official Posts (`/v/blog`, `/v/wiki`, etc.)
- From your Followers
- From people your following

## Users
Users are the base venera entity and have control over many things.

Users can join Venerettes, Become Moderators and more.
