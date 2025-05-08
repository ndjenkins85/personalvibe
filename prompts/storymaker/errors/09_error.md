Last login: Wed May  7 14:13:09 on ttys006
/Users/nicholasjenkins/.bash_profile set to ndj_ai_cookie poetry

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
MacBook-Air-3:~ nicholasjenkins$ cd Documents/
MacBook-Air-3:Documents nicholasjenkins$ cd personalvibe
MacBook-Air-3:personalvibe nicholasjenkins$ poetry shell
Spawning shell within /Users/nicholasjenkins/Documents/personalvibe/.venv

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
bash-3.2$ . /Users/nicholasjenkins/Documents/personalvibe/.venv/bin/activate
(personalvibe-py3.12) bash-3.2$ # Download and install nvm:
(personalvibe-py3.12) bash-3.2$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 16631  100 16631    0     0  54973      0 --:--:-- --:--:-- --:--:-- 55252
=> Downloading nvm from git to '/Users/nicholasjenkins/.nvm'
=> Cloning into '/Users/nicholasjenkins/.nvm'...
remote: Enumerating objects: 382, done.
remote: Counting objects: 100% (382/382), done.
remote: Compressing objects: 100% (325/325), done.
remote: Total 382 (delta 43), reused 179 (delta 29), pack-reused 0 (from 0)
Receiving objects: 100% (382/382), 385.06 KiB | 2.29 MiB/s, done.
Resolving deltas: 100% (43/43), done.
* (HEAD detached at FETCH_HEAD)
  master
=> Compressing and cleaning up git repository

=> Appending nvm source string to /Users/nicholasjenkins/.bash_profile
=> Appending bash_completion source string to /Users/nicholasjenkins/.bash_profile
=> Close and reopen your terminal to start using nvm or run the following to use it now:

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
(personalvibe-py3.12) bash-3.2$
(personalvibe-py3.12) bash-3.2$ # in lieu of restarting the shell
(personalvibe-py3.12) bash-3.2$ \. "$HOME/.nvm/nvm.sh"
(personalvibe-py3.12) bash-3.2$
(personalvibe-py3.12) bash-3.2$ # Download and install Node.js:
(personalvibe-py3.12) bash-3.2$ nvm install 22
Downloading and installing node v22.15.0...
Downloading https://nodejs.org/dist/v22.15.0/node-v22.15.0-darwin-x64.tar.xz...
################################################################################################################################################################################################### 100.0%
Computing checksum with sha256sum
Checksums matched!

# Verify the Node.js version:
node -v # Should print "v22.15.0".
nvm current # Should print "v22.15.0".

# Verify npm version:
npm -v # Should print "10.9.2".
Now using node v22.15.0 (npm v10.9.2)
Creating default alias: default -> 22 (-> v22.15.0)
(personalvibe-py3.12) bash-3.2$
(personalvibe-py3.12) bash-3.2$ # Verify the Node.js version:
(personalvibe-py3.12) bash-3.2$ node -v # Should print "v22.15.0".
v22.15.0
(personalvibe-py3.12) bash-3.2$ nvm current # Should print "v22.15.0".
v22.15.0
(personalvibe-py3.12) bash-3.2$
(personalvibe-py3.12) bash-3.2$ # Verify npm version:
(personalvibe-py3.12) bash-3.2$ npm -v # Should print "10.9.2".
10.9.2
(personalvibe-py3.12) bash-3.2$ npm
npm <command>

Usage:

npm install        install all the dependencies in your project
npm install <foo>  add the <foo> dependency to your project
npm test           run this project's tests
npm run <foo>      run the script named <foo>
npm <command> -h   quick help on <command>
npm -l             display usage info for all commands
npm help <term>    search for help on <term>
npm help npm       more involved overview

All commands:

    access, adduser, audit, bugs, cache, ci, completion,
    config, dedupe, deprecate, diff, dist-tag, docs, doctor,
    edit, exec, explain, explore, find-dupes, fund, get, help,
    help-search, hook, init, install, install-ci-test,
    install-test, link, ll, login, logout, ls, org, outdated,
    owner, pack, ping, pkg, prefix, profile, prune, publish,
    query, rebuild, repo, restart, root, run-script, sbom,
    search, set, shrinkwrap, star, stars, start, stop, team,
    test, token, uninstall, unpublish, unstar, update, version,
    view, whoami

Specify configs in the ini-formatted file:
    /Users/nicholasjenkins/.npmrc
or on the command line via: npm <command> --key=value

More configuration info: npm help config
Configuration fields: npm help 7 config

npm@10.9.2 /Users/nicholasjenkins/.nvm/versions/node/v22.15.0/lib/node_modules/npm
(personalvibe-py3.12) bash-3.2$ cd storymaker_spa/
(personalvibe-py3.12) bash-3.2$ npm install
npm error code ETARGET
npm error notarget No matching version found for @types/react-router-dom@^6.23.1.
npm error notarget In most cases you or one of your dependencies are requesting
npm error notarget a package version that doesn't exist.
npm notice
npm notice New major version of npm available! 10.9.2 -> 11.3.0
npm notice Changelog: https://github.com/npm/cli/releases/tag/v11.3.0
npm notice To update run: npm install -g npm@11.3.0
npm notice
npm error A complete log of this run can be found in: /Users/nicholasjenkins/.npm/_logs/2025-05-08T17_22_10_203Z-debug-0.log
(personalvibe-py3.12) bash-3.2$ subl storymaker_spa/package.json
(personalvibe-py3.12) bash-3.2$ cd ..
(personalvibe-py3.12) bash-3.2$ ls
CONTRIBUTING.md		README.md		docker-compose.yml	notebooks		prompts			src
Dockerfile		data			docs			noxfile.py		pyproject.toml		storymaker_spa
LICENSE			dist			logs			poetry.lock		run.py			tests
(personalvibe-py3.12) bash-3.2$ cd storymaker_spa/storymaker_spa/package.json
(personalvibe-py3.12) bash-3.2$ pwd
/Users/nicholasjenkins/Documents/personalvibe
(personalvibe-py3.12) bash-3.2$ subl storymaker_spa/package.json
(personalvibe-py3.12) bash-3.2$ cd storymaker_spa
(personalvibe-py3.12) bash-3.2$ rm -rf node_modules package-lock.json
(personalvibe-py3.12) bash-3.2$ npm install

added 69 packages, and audited 70 packages in 27s

7 packages are looking for funding
  run `npm fund` for details

2 moderate severity vulnerabilities

To address all issues (including breaking changes), run:
  npm audit fix --force

Run `npm audit` for details.
(personalvibe-py3.12) bash-3.2$ npm run dev

> storymaker-spa@0.0.1 dev
> vite


  VITE v5.4.19  ready in 1187 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
10:26:45 am [vite] Pre-transform error: Transform failed with 1 error:
/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/src/api/client.ts:5:27: ERROR: Syntax error "`"
10:26:45 am [vite] Pre-transform error: Transform failed with 1 error:
/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/src/api/client.ts:5:27: ERROR: Syntax error "`" (x2)
Error:   Failed to scan for dependencies from entries:
  /Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/index.html

  ✘ [ERROR] Syntax error "`"

    src/api/client.ts:5:27:
      5 │   const res = await fetch(\`\${API_BASE}\${path}\`, {
        ╵                            ^


    at failureErrorWithLog (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:1472:15)
    at /Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:945:25
    at runOnEndCallbacks (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:1315:45)
    at buildResponseToResult (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:943:7)
    at /Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:955:9
    at new Promise (<anonymous>)
    at requestCallbacks.on-end (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:954:54)
    at handleRequest (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:647:17)
    at handleIncomingPacket (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:672:7)
    at Socket.readFromStdout (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:600:7)
    at Socket.emit (node:events:518:28)
    at addChunk (node:internal/streams/readable:561:12)
    at readableAddChunkPushByteMode (node:internal/streams/readable:512:3)
    at Readable.push (node:internal/streams/readable:392:5)
    at Pipe.onStreamRead (node:internal/stream_base_commons:189:23)
10:26:49 am [vite] Internal server error: Transform failed with 1 error:
/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/src/api/client.ts:5:27: ERROR: Syntax error "`"
  Plugin: vite:esbuild
  File: /Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/src/api/client.ts:5:27

  Syntax error "`"
  3  |
  4  |  async function apiFetch<T>(path: string, opts: RequestInit = {}): Promise<T> {
  5  |    const res = await fetch(\`\${API_BASE}\${path}\`, {
     |                             ^
  6  |      headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
  7  |      ...opts,

      at failureErrorWithLog (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:1472:15)
      at /Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:755:50
      at responseCallbacks.<computed> (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:622:9)
      at handleIncomingPacket (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:677:12)
      at Socket.readFromStdout (/Users/nicholasjenkins/Documents/personalvibe/storymaker_spa/node_modules/esbuild/lib/main.js:600:7)
      at Socket.emit (node:events:518:28)
      at addChunk (node:internal/streams/readable:561:12)
      at readableAddChunkPushByteMode (node:internal/streams/readable:512:3)
      at Readable.push (node:internal/streams/readable:392:5)
      at Pipe.onStreamRead (node:internal/stream_base_commons:189:23)
