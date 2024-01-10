<div align="center">
  <h1>@kyvejs</h1>
</div>

![banner](https://arweave.net/RkC-azeak1eOQGOLSaPNzHo-ORc-cWgnmdJnSScedFE)

<p align="center">
<strong>Tools for building applications on KYVE</strong>
</p>

<br/>

<div align="center">
  <img alt="License: Apache-2.0" src="https://badgen.net/github/license/KYVENetwork/kyvejs?color=green" />

  <img alt="License: Apache-2.0" src="https://badgen.net/github/stars/KYVENetwork/kyvejs?color=green" />

  <img alt="License: Apache-2.0" src="https://badgen.net/github/contributors/KYVENetwork/kyvejs?color=green" />

  <img alt="License: Apache-2.0" src="https://badgen.net/github/releases/KYVENetwork/kyvejs?color=green" />
</div>

<div align="center">
  <a href="https://twitter.com/KYVENetwork" target="_blank">
    <img alt="Twitter" src="https://badgen.net/badge/icon/twitter?icon=twitter&label" />
  </a>
  <a href="https://discord.com/invite/kyve" target="_blank">
    <img alt="Discord" src="https://badgen.net/badge/icon/discord?icon=discord&label" />
  </a>
  <a href="https://t.me/kyvenet" target="_blank">
    <img alt="Telegram" src="https://badgen.net/badge/icon/telegram?icon=telegram&label" />
  </a>
</div>

<br/>

KYVE, the Web3 data lake solution, is a protocol that enables data providers to standardize, validate, and permanently store blockchain data streams. By leveraging permanent data storage solutions like Arweave, KYVE’s Cosmos SDK chain creates permanent backups and ensures the scalability, immutability, and availability of these resources over time.

## Project Overview

**Common:**

- [@kyvejs/types](common/types/README.md) - holds all types for the KYVE application in typescript
- [@kyvejs/sdk](common/sdk/README.md) - development kit for communicating with the KYVE blockchain
- [@kyvejs/protocol](common/protocol/README.md) - core functionality for running validators on the KYVE network

**Tools:**

- [@kyvejs/kysor](tools/kysor/README.md) - The Cosmovisor of KYVE

**Integrations:**

- [@kyvejs/tendermint](integrations/tendermint/README.md) - The official KYVE Tendermint sync integration
- [@kyvejs/tendermint-ssync](integrations/tendermint-ssync/README.md) - The official KYVE Tendermint state-sync integration
- [@kyvejs/tendermint-bsync](integrations/tendermint-bsync/README.md) - The official KYVE Tendermint block sync integration

## Build Integration Binaries

Clone and checkout repository:

```bash
git clone git@github.com:KYVENetwork/kyvejs.git
cd kyvejs
```

Checkout desired version:

```
git checkout tags/@kyvejs/<integration>@x.x.x -b @kyvejs/<integration>@x.x.x
```

Example: `git checkout tags/@kyvejs/tendermint-bsync@1.0.0 -b @kyvejs/tendermint-bsync@1.0.0`

Install dependencies and setup project:

```
yarn setup
```

Checkout integration and build binaries:

```
cd integrations/<integration>
yarn build:binaries
```

The binaries can then be found in the `/out` folder

## Dockerized Execution (alpha)

**This is still in alpha and not recommended for production use!**

The easiest way to run a KYVE integration is by using the provided Docker images via docker compose. 

**Prerequisites**
- Copy the `docker-compose.yml.template` as `docker-compose.yml` and fill in the required environment variables.
- Instead of environment variables, you can also provide a `.env` file in the root directory of the repository. Just copy the `.env.template` file as `.env` and fill in the required environment variables.

```bash
cp docker-compose.yml.template docker-compose.yml
cp .env.template .env
```

**Execution**
```bash
docker compose up # add -d to run in background; add --build to rebuild images
```


## How to contribute

Checkout new branch to implement new features/fixes there

```bash
git checkout -b [feat/fix]/[my-branch-name]
```

Install dependencies and setup project:

```bash
yarn setup
```

Apply your changes and create a Pull Request to `main`. Once the team has
reviewed and approved your PR it can be merged and used.

**NOTE**: The usage of [Conventional Commits](https://conventionalcommits.org) is required when creating PRs and committing to this repository

### How to write a KYVE integration

**Prerequisites:**
- Docker
- yarn (optional)

#### Bootstrap a new integration

Run the following command to start the integration wizard:

```bash
# with yarn
yarn bootstrap:integration
```
```bash
# or without yarn
sh ./tools/kystrap/start.sh
```

Follow the instructions to create a new integration.
The wizard will create a new folder in `integrations` with the integration name you provided.

## How to release

In order to release new changes which got merged into `main` lerna can be used. Lerna will look into every change and create a new release tag if necessary. After the user has approved the new version tags (bumped according to [Semantic Versioning](https://semver.org/)) lerna will push those new tags to `main`, starting the CI/CD pipeline and creating the releases.

Release with lerna:

```
yarn lerna version
```
