[![License: MIT](https://img.shields.io/github/license/marcelovicentegc/mypersonalmachine)](LICENSE)

<p align="center">
  <img alt="mypersonalmachine profile" src="https://avatars.githubusercontent.com/u/92038903?v=4" height="300" />
  <h3 align="center">mypersonalmachine:merger</h3>
  <p align="center">Source code from @mypersonalmachine's merger application.</p>
</p>

---

## Configuration

| Variable     | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| GITHUB_TOKEN | The Github token to allow your user to execute actions via API. |
| TARGET_USER  | The owner of the repositories you're targetting.                |
| TARGET_REPOS | The targetted repositories, separated by `,`.                   |
| SENTRY_DSN   | Your Sentry instance DSN.                                       |

The Merger expects these variables to live within a `.env.` file. You can derive it from the [`.env.example`](./.env.example) file.

## Development

```bash
yarn setup && yarn start
```
