2026-02-28T19:08:17.2904861Z Current runner version: '2.331.0'
2026-02-28T19:08:17.2931525Z ##[group]Runner Image Provisioner
2026-02-28T19:08:17.2932756Z Hosted Compute Agent
2026-02-28T19:08:17.2933347Z Version: 20260213.493
2026-02-28T19:08:17.2933924Z Commit: 5c115507f6dd24b8de37d8bbe0bb4509d0cc0fa3
2026-02-28T19:08:17.2934778Z Build Date: 2026-02-13T00:28:41Z
2026-02-28T19:08:17.2935450Z Worker ID: {e2ad3d2b-7f1a-40d0-9855-a502844f6dca}
2026-02-28T19:08:17.2936112Z Azure Region: northcentralus
2026-02-28T19:08:17.2936758Z ##[endgroup]
2026-02-28T19:08:17.2938208Z ##[group]Operating System
2026-02-28T19:08:17.2938828Z Ubuntu
2026-02-28T19:08:17.2939367Z 24.04.3
2026-02-28T19:08:17.2939862Z LTS
2026-02-28T19:08:17.2940317Z ##[endgroup]
2026-02-28T19:08:17.2940914Z ##[group]Runner Image
2026-02-28T19:08:17.2941490Z Image: ubuntu-24.04
2026-02-28T19:08:17.2941966Z Version: 20260224.36.1
2026-02-28T19:08:17.2943733Z Included Software: https://github.com/actions/runner-images/blob/ubuntu24/20260224.36/images/ubuntu/Ubuntu2404-Readme.md
2026-02-28T19:08:17.2945289Z Image Release: https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20260224.36
2026-02-28T19:08:17.2946273Z ##[endgroup]
2026-02-28T19:08:17.2947435Z ##[group]GITHUB_TOKEN Permissions
2026-02-28T19:08:17.2949567Z Contents: read
2026-02-28T19:08:17.2950240Z Metadata: read
2026-02-28T19:08:17.2950716Z Packages: read
2026-02-28T19:08:17.2951195Z ##[endgroup]
2026-02-28T19:08:17.2953762Z Secret source: Actions
2026-02-28T19:08:17.2954765Z Prepare workflow directory
2026-02-28T19:08:17.3303810Z Prepare all required actions
2026-02-28T19:08:17.3343087Z Getting action download info
2026-02-28T19:08:17.6408565Z Download action repository 'actions/checkout@v4' (SHA:34e114876b0b11c390a56381ad16ebd13914f8d5)
2026-02-28T19:08:17.7864285Z Download action repository 'actions/setup-python@v5' (SHA:a26af69be951a213d495a4c3e4e4022e16d87065)
2026-02-28T19:08:17.9831702Z Complete job name: Run Tests
2026-02-28T19:08:18.0575353Z ##[group]Run actions/checkout@v4
2026-02-28T19:08:18.0576222Z with:
2026-02-28T19:08:18.0576637Z   repository: KnowOneActual/isobar-cli
2026-02-28T19:08:18.0577365Z   token: ***
2026-02-28T19:08:18.0577740Z   ssh-strict: true
2026-02-28T19:08:18.0578131Z   ssh-user: git
2026-02-28T19:08:18.0578514Z   persist-credentials: true
2026-02-28T19:08:18.0578952Z   clean: true
2026-02-28T19:08:18.0579338Z   sparse-checkout-cone-mode: true
2026-02-28T19:08:18.0579801Z   fetch-depth: 1
2026-02-28T19:08:18.0580179Z   fetch-tags: false
2026-02-28T19:08:18.0580573Z   show-progress: true
2026-02-28T19:08:18.0580968Z   lfs: false
2026-02-28T19:08:18.0581322Z   submodules: false
2026-02-28T19:08:18.0581725Z   set-safe-directory: true
2026-02-28T19:08:18.0582907Z ##[endgroup]
2026-02-28T19:08:18.1721964Z Syncing repository: KnowOneActual/isobar-cli
2026-02-28T19:08:18.1724583Z ##[group]Getting Git version info
2026-02-28T19:08:18.1725422Z Working directory is '/home/runner/work/isobar-cli/isobar-cli'
2026-02-28T19:08:18.1726400Z [command]/usr/bin/git version
2026-02-28T19:08:18.1810777Z git version 2.53.0
2026-02-28T19:08:18.1839118Z ##[endgroup]
2026-02-28T19:08:18.1854675Z Temporarily overriding HOME='/home/runner/work/_temp/34e403e1-49f3-4b9f-9c9a-4f70f32d8537' before making global git config changes
2026-02-28T19:08:18.1856077Z Adding repository directory to the temporary git global config as a safe directory
2026-02-28T19:08:18.1868974Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/isobar-cli/isobar-cli
2026-02-28T19:08:18.1914876Z Deleting the contents of '/home/runner/work/isobar-cli/isobar-cli'
2026-02-28T19:08:18.1918714Z ##[group]Initializing the repository
2026-02-28T19:08:18.1923654Z [command]/usr/bin/git init /home/runner/work/isobar-cli/isobar-cli
2026-02-28T19:08:18.2058374Z hint: Using 'master' as the name for the initial branch. This default branch name
2026-02-28T19:08:18.2059859Z hint: will change to "main" in Git 3.0. To configure the initial branch name
2026-02-28T19:08:18.2060955Z hint: to use in all of your new repositories, which will suppress this warning,
2026-02-28T19:08:18.2062537Z hint: call:
2026-02-28T19:08:18.2063287Z hint:
2026-02-28T19:08:18.2064594Z hint: 	git config --global init.defaultBranch <name>
2026-02-28T19:08:18.2065303Z hint:
2026-02-28T19:08:18.2065949Z hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
2026-02-28T19:08:18.2067025Z hint: 'development'. The just-created branch can be renamed via this command:
2026-02-28T19:08:18.2067860Z hint:
2026-02-28T19:08:18.2068299Z hint: 	git branch -m <name>
2026-02-28T19:08:18.2068887Z hint:
2026-02-28T19:08:18.2069699Z hint: Disable this message with "git config set advice.defaultBranchName false"
2026-02-28T19:08:18.2070726Z Initialized empty Git repository in /home/runner/work/isobar-cli/isobar-cli/.git/
2026-02-28T19:08:18.2076648Z [command]/usr/bin/git remote add origin https://github.com/KnowOneActual/isobar-cli
2026-02-28T19:08:18.2116397Z ##[endgroup]
2026-02-28T19:08:18.2117150Z ##[group]Disabling automatic garbage collection
2026-02-28T19:08:18.2120980Z [command]/usr/bin/git config --local gc.auto 0
2026-02-28T19:08:18.2151796Z ##[endgroup]
2026-02-28T19:08:18.2152800Z ##[group]Setting up auth
2026-02-28T19:08:18.2159677Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-02-28T19:08:18.2192453Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-02-28T19:08:18.2581109Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-02-28T19:08:18.2618930Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-02-28T19:08:18.2877827Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-02-28T19:08:18.2914594Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-02-28T19:08:18.3198311Z [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
2026-02-28T19:08:18.3239986Z ##[endgroup]
2026-02-28T19:08:18.3241228Z ##[group]Fetching the repository
2026-02-28T19:08:18.3251110Z [command]/usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +bce38bcb4af4276c44595a4ef2480fd2b0565448:refs/remotes/origin/main
2026-02-28T19:08:18.5797849Z From https://github.com/KnowOneActual/isobar-cli
2026-02-28T19:08:18.5800072Z  * [new ref]         bce38bcb4af4276c44595a4ef2480fd2b0565448 -> origin/main
2026-02-28T19:08:18.5843530Z ##[endgroup]
2026-02-28T19:08:18.5844896Z ##[group]Determining the checkout info
2026-02-28T19:08:18.5846458Z ##[endgroup]
2026-02-28T19:08:18.5850667Z [command]/usr/bin/git sparse-checkout disable
2026-02-28T19:08:18.5901591Z [command]/usr/bin/git config --local --unset-all extensions.worktreeConfig
2026-02-28T19:08:18.5934831Z ##[group]Checking out the ref
2026-02-28T19:08:18.5940352Z [command]/usr/bin/git checkout --progress --force -B main refs/remotes/origin/main
2026-02-28T19:08:18.6008732Z Switched to a new branch 'main'
2026-02-28T19:08:18.6010927Z branch 'main' set up to track 'origin/main'.
2026-02-28T19:08:18.6019822Z ##[endgroup]
2026-02-28T19:08:18.6061991Z [command]/usr/bin/git log -1 --format=%H
2026-02-28T19:08:18.6089361Z bce38bcb4af4276c44595a4ef2480fd2b0565448
2026-02-28T19:08:18.6404151Z ##[group]Run actions/setup-python@v5
2026-02-28T19:08:18.6404929Z with:
2026-02-28T19:08:18.6405353Z   python-version: 3.11
2026-02-28T19:08:18.6405913Z   check-latest: false
2026-02-28T19:08:18.6406681Z   token: ***
2026-02-28T19:08:18.6407151Z   update-environment: true
2026-02-28T19:08:18.6407762Z   allow-prereleases: false
2026-02-28T19:08:18.6408361Z   freethreaded: false
2026-02-28T19:08:18.6408863Z ##[endgroup]
2026-02-28T19:08:18.8250415Z ##[group]Installed versions
2026-02-28T19:08:18.8358830Z Successfully set up CPython (3.11.14)
2026-02-28T19:08:18.8361347Z ##[endgroup]
2026-02-28T19:08:18.8510247Z ##[group]Run pip install -e .[test]
2026-02-28T19:08:18.8511557Z [36;1mpip install -e .[test][0m
2026-02-28T19:08:18.8623871Z shell: /usr/bin/bash -e {0}
2026-02-28T19:08:18.8625009Z env:
2026-02-28T19:08:18.8626159Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.14/x64
2026-02-28T19:08:18.8627907Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.14/x64/lib/pkgconfig
2026-02-28T19:08:18.8629648Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.14/x64
2026-02-28T19:08:18.8631239Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.14/x64
2026-02-28T19:08:18.8633082Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.14/x64
2026-02-28T19:08:18.8634726Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.14/x64/lib
2026-02-28T19:08:18.8636122Z ##[endgroup]
2026-02-28T19:08:21.1774777Z Obtaining file:///home/runner/work/isobar-cli/isobar-cli
2026-02-28T19:08:21.1793434Z   Installing build dependencies: started
2026-02-28T19:08:21.9941468Z   Installing build dependencies: finished with status 'done'
2026-02-28T19:08:21.9948231Z   Checking if build backend supports build_editable: started
2026-02-28T19:08:22.3477586Z   Checking if build backend supports build_editable: finished with status 'done'
2026-02-28T19:08:22.3485105Z   Getting requirements to build editable: started
2026-02-28T19:08:22.6677507Z   Getting requirements to build editable: finished with status 'done'
2026-02-28T19:08:22.6686702Z   Preparing editable metadata (pyproject.toml): started
2026-02-28T19:08:22.8606135Z   Preparing editable metadata (pyproject.toml): finished with status 'done'
2026-02-28T19:08:22.9667534Z Collecting rich>=13.0.0 (from isobar-cli==0.5.1)
2026-02-28T19:08:23.0239780Z   Downloading rich-14.3.3-py3-none-any.whl.metadata (18 kB)
2026-02-28T19:08:23.0524752Z Collecting requests>=2.31.0 (from isobar-cli==0.5.1)
2026-02-28T19:08:23.0566757Z   Downloading requests-2.32.5-py3-none-any.whl.metadata (4.9 kB)
2026-02-28T19:08:23.0766101Z Collecting typer>=0.9.0 (from isobar-cli==0.5.1)
2026-02-28T19:08:23.0803555Z   Downloading typer-0.24.1-py3-none-any.whl.metadata (16 kB)
2026-02-28T19:08:23.1064229Z Collecting timezonefinder>=6.0.0 (from isobar-cli==0.5.1)
2026-02-28T19:08:23.1133227Z   Downloading timezonefinder-8.2.1-cp39-abi3-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.8 kB)
2026-02-28T19:08:23.1553628Z Collecting pytest>=7.0.0 (from isobar-cli==0.5.1)
2026-02-28T19:08:23.1609281Z   Downloading pytest-9.0.2-py3-none-any.whl.metadata (7.6 kB)
2026-02-28T19:08:23.1750665Z Collecting requests-mock>=1.11.0 (from isobar-cli==0.5.1)
2026-02-28T19:08:23.1813604Z   Downloading requests_mock-1.12.1-py2.py3-none-any.whl.metadata (4.1 kB)
2026-02-28T19:08:23.1965207Z Collecting pytest-cov>=4.1.0 (from isobar-cli==0.5.1)
2026-02-28T19:08:23.2026160Z   Downloading pytest_cov-7.0.0-py3-none-any.whl.metadata (31 kB)
2026-02-28T19:08:23.2175286Z Collecting iniconfig>=1.0.1 (from pytest>=7.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.2213949Z   Downloading iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)
2026-02-28T19:08:23.2366636Z Collecting packaging>=22 (from pytest>=7.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.2411601Z   Downloading packaging-26.0-py3-none-any.whl.metadata (3.3 kB)
2026-02-28T19:08:23.2538418Z Collecting pluggy<2,>=1.5 (from pytest>=7.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.2580522Z   Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
2026-02-28T19:08:23.2774665Z Collecting pygments>=2.7.2 (from pytest>=7.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.2812287Z   Downloading pygments-2.19.2-py3-none-any.whl.metadata (2.5 kB)
2026-02-28T19:08:23.6311223Z Collecting coverage>=7.10.6 (from coverage[toml]>=7.10.6->pytest-cov>=4.1.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.6353985Z   Downloading coverage-7.13.4-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (8.5 kB)
2026-02-28T19:08:23.7329818Z Collecting charset_normalizer<4,>=2 (from requests>=2.31.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.7371581Z   Downloading charset_normalizer-3.4.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (37 kB)
2026-02-28T19:08:23.7553488Z Collecting idna<4,>=2.5 (from requests>=2.31.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.7592937Z   Downloading idna-3.11-py3-none-any.whl.metadata (8.4 kB)
2026-02-28T19:08:23.7823935Z Collecting urllib3<3,>=1.21.1 (from requests>=2.31.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.7866027Z   Downloading urllib3-2.6.3-py3-none-any.whl.metadata (6.9 kB)
2026-02-28T19:08:23.8058521Z Collecting certifi>=2017.4.17 (from requests>=2.31.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.8099639Z   Downloading certifi-2026.2.25-py3-none-any.whl.metadata (2.5 kB)
2026-02-28T19:08:23.8278524Z Collecting markdown-it-py>=2.2.0 (from rich>=13.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.8322899Z   Downloading markdown_it_py-4.0.0-py3-none-any.whl.metadata (7.3 kB)
2026-02-28T19:08:23.8475861Z Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich>=13.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:23.8629042Z   Downloading mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
2026-02-28T19:08:24.0371569Z Collecting numpy>=2 (from timezonefinder>=6.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:24.0415819Z   Downloading numpy-2.4.2-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (6.6 kB)
2026-02-28T19:08:24.1017864Z Collecting h3>=4 (from timezonefinder>=6.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:24.1072810Z   Downloading h3-4.4.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (18 kB)
2026-02-28T19:08:24.2508421Z Collecting cffi<3,>=1.15.1 (from timezonefinder>=6.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:24.2549362Z   Downloading cffi-2.0.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (2.6 kB)
2026-02-28T19:08:24.2683404Z Collecting flatbuffers>=25.2.10 (from timezonefinder>=6.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:24.2719002Z   Downloading flatbuffers-25.12.19-py2.py3-none-any.whl.metadata (1.0 kB)
2026-02-28T19:08:24.2836155Z Collecting pycparser (from cffi<3,>=1.15.1->timezonefinder>=6.0.0->isobar-cli==0.5.1)
2026-02-28T19:08:24.2881820Z   Downloading pycparser-3.0-py3-none-any.whl.metadata (8.2 kB)
2026-02-28T19:08:24.3050015Z Collecting click>=8.2.1 (from typer>=0.9.0->isobar-cli==0.5.1)
2026-02-28T19:08:24.3088701Z   Downloading click-8.3.1-py3-none-any.whl.metadata (2.6 kB)
2026-02-28T19:08:24.3241840Z Collecting shellingham>=1.3.0 (from typer>=0.9.0->isobar-cli==0.5.1)
2026-02-28T19:08:24.3279577Z   Downloading shellingham-1.5.4-py2.py3-none-any.whl.metadata (3.5 kB)
2026-02-28T19:08:24.3415335Z Collecting annotated-doc>=0.0.2 (from typer>=0.9.0->isobar-cli==0.5.1)
2026-02-28T19:08:24.3453100Z   Downloading annotated_doc-0.0.4-py3-none-any.whl.metadata (6.6 kB)
2026-02-28T19:08:24.3542568Z Downloading pytest-9.0.2-py3-none-any.whl (374 kB)
2026-02-28T19:08:24.3745320Z Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
2026-02-28T19:08:24.3803977Z Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)
2026-02-28T19:08:24.3859832Z Downloading packaging-26.0-py3-none-any.whl (74 kB)
2026-02-28T19:08:24.3931030Z Downloading pygments-2.19.2-py3-none-any.whl (1.2 MB)
2026-02-28T19:08:24.4194942Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 52.3 MB/s  0:00:00
2026-02-28T19:08:24.4230351Z Downloading pytest_cov-7.0.0-py3-none-any.whl (22 kB)
2026-02-28T19:08:24.4293438Z Downloading coverage-7.13.4-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (252 kB)
2026-02-28T19:08:24.4376956Z Downloading requests-2.32.5-py3-none-any.whl (64 kB)
2026-02-28T19:08:24.4436745Z Downloading charset_normalizer-3.4.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (151 kB)
2026-02-28T19:08:24.4510593Z Downloading idna-3.11-py3-none-any.whl (71 kB)
2026-02-28T19:08:24.4567557Z Downloading urllib3-2.6.3-py3-none-any.whl (131 kB)
2026-02-28T19:08:24.4635056Z Downloading certifi-2026.2.25-py3-none-any.whl (153 kB)
2026-02-28T19:08:24.4717522Z Downloading requests_mock-1.12.1-py2.py3-none-any.whl (27 kB)
2026-02-28T19:08:24.4789723Z Downloading rich-14.3.3-py3-none-any.whl (310 kB)
2026-02-28T19:08:24.4904892Z Downloading markdown_it_py-4.0.0-py3-none-any.whl (87 kB)
2026-02-28T19:08:24.4966509Z Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)
2026-02-28T19:08:24.5033938Z Downloading timezonefinder-8.2.1-cp39-abi3-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (53.8 MB)
2026-02-28T19:08:24.7815296Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.8/53.8 MB 195.7 MB/s  0:00:00
2026-02-28T19:08:24.7859627Z Downloading cffi-2.0.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (215 kB)
2026-02-28T19:08:24.7926997Z Downloading flatbuffers-25.12.19-py2.py3-none-any.whl (26 kB)
2026-02-28T19:08:24.8003231Z Downloading h3-4.4.2-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (1.0 MB)
2026-02-28T19:08:24.8081488Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.0/1.0 MB 147.0 MB/s  0:00:00
2026-02-28T19:08:24.8122231Z Downloading numpy-2.4.2-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.9 MB)
2026-02-28T19:08:24.8767315Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.9/16.9 MB 269.4 MB/s  0:00:00
2026-02-28T19:08:24.8808136Z Downloading typer-0.24.1-py3-none-any.whl (56 kB)
2026-02-28T19:08:24.8870198Z Downloading annotated_doc-0.0.4-py3-none-any.whl (5.3 kB)
2026-02-28T19:08:24.8928962Z Downloading click-8.3.1-py3-none-any.whl (108 kB)
2026-02-28T19:08:24.8989820Z Downloading shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
2026-02-28T19:08:24.9046142Z Downloading pycparser-3.0-py3-none-any.whl (48 kB)
2026-02-28T19:08:24.9882459Z Building wheels for collected packages: isobar-cli
2026-02-28T19:08:24.9890500Z   Building editable for isobar-cli (pyproject.toml): started
2026-02-28T19:08:25.1888726Z   Building editable for isobar-cli (pyproject.toml): finished with status 'done'
2026-02-28T19:08:25.1894729Z   Created wheel for isobar-cli: filename=isobar_cli-0.5.1-0.editable-py3-none-any.whl size=2562 sha256=c5bd549d132e7a8b16e3e5a9465d6a3dd52f80d9199642c2c1535d0eb2213a5d
2026-02-28T19:08:25.1896435Z   Stored in directory: /tmp/pip-ephem-wheel-cache-sj4em0tg/wheels/dc/32/b9/82f5df22bb379071a72bedbfbae06b9f7db0e87ae100b058e9
2026-02-28T19:08:25.1911302Z Successfully built isobar-cli
2026-02-28T19:08:25.2362883Z Installing collected packages: flatbuffers, urllib3, shellingham, pygments, pycparser, pluggy, packaging, numpy, mdurl, iniconfig, idna, h3, coverage, click, charset_normalizer, certifi, annotated-doc, requests, pytest, markdown-it-py, cffi, timezonefinder, rich, requests-mock, pytest-cov, typer, isobar-cli
2026-02-28T19:08:29.8584670Z 
2026-02-28T19:08:29.8603647Z Successfully installed annotated-doc-0.0.4 certifi-2026.2.25 cffi-2.0.0 charset_normalizer-3.4.4 click-8.3.1 coverage-7.13.4 flatbuffers-25.12.19 h3-4.4.2 idna-3.11 iniconfig-2.3.0 isobar-cli-0.5.1 markdown-it-py-4.0.0 mdurl-0.1.2 numpy-2.4.2 packaging-26.0 pluggy-1.6.0 pycparser-3.0 pygments-2.19.2 pytest-9.0.2 pytest-cov-7.0.0 requests-2.32.5 requests-mock-1.12.1 rich-14.3.3 shellingham-1.5.4 timezonefinder-8.2.1 typer-0.24.1 urllib3-2.6.3
2026-02-28T19:08:30.2853676Z ##[group]Run pytest
2026-02-28T19:08:30.2854015Z [36;1mpytest[0m
2026-02-28T19:08:30.2907495Z shell: /usr/bin/bash -e {0}
2026-02-28T19:08:30.2907733Z env:
2026-02-28T19:08:30.2907997Z   pythonLocation: /opt/hostedtoolcache/Python/3.11.14/x64
2026-02-28T19:08:30.2908430Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.11.14/x64/lib/pkgconfig
2026-02-28T19:08:30.2908841Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.14/x64
2026-02-28T19:08:30.2909212Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.14/x64
2026-02-28T19:08:30.2909578Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.11.14/x64
2026-02-28T19:08:30.2909952Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.11.14/x64/lib
2026-02-28T19:08:30.2910266Z ##[endgroup]
2026-02-28T19:08:31.4745189Z ============================= test session starts ==============================
2026-02-28T19:08:31.4746299Z platform linux -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0
2026-02-28T19:08:31.4747002Z rootdir: /home/runner/work/isobar-cli/isobar-cli
2026-02-28T19:08:31.4747525Z configfile: pyproject.toml
2026-02-28T19:08:31.4747906Z testpaths: tests
2026-02-28T19:08:31.4748251Z plugins: cov-7.0.0, requests-mock-1.12.1
2026-02-28T19:08:31.4748690Z collected 14 items
2026-02-28T19:08:31.4748887Z 
2026-02-28T19:08:35.3999491Z tests/test_api.py ...                                                    [ 21%]
2026-02-28T19:08:35.4098658Z tests/test_location.py ...                                               [ 42%]
2026-02-28T19:08:35.5823835Z tests/test_main.py .F...                                                 [ 78%]
2026-02-28T19:08:35.7119603Z tests/test_ui.py ...                                                     [100%]
2026-02-28T19:08:35.7120194Z 
2026-02-28T19:08:35.7120444Z =================================== FAILURES ===================================
2026-02-28T19:08:35.7121216Z _________________________ test_main_metric_flag_exists _________________________
2026-02-28T19:08:35.7121751Z 
2026-02-28T19:08:35.7121940Z     def test_main_metric_flag_exists():
2026-02-28T19:08:35.7122852Z         result = runner.invoke(app, ["--help"])
2026-02-28T19:08:35.7123332Z >       assert "--metric" in result.output
2026-02-28T19:08:35.7125738Z E       AssertionError: assert '--metric' in '\x1b[1m                                                                                \x1b[0m\n\x1b[1m \x1b[0m\x1b[1...   \x1b[2m│\x1b[0m\n\x1b[2m╰──────────────────────────────────────────────────────────────────────────────╯\x1b[0m\n\n'
2026-02-28T19:08:35.7128123Z E        +  where '\x1b[1m                                                                                \x1b[0m\n\x1b[1m \x1b[0m\x1b[1...   \x1b[2m│\x1b[0m\n\x1b[2m╰──────────────────────────────────────────────────────────────────────────────╯\x1b[0m\n\n' = <Result okay>.output
2026-02-28T19:08:35.7129164Z 
2026-02-28T19:08:35.7129303Z tests/test_main.py:15: AssertionError
2026-02-28T19:08:35.7129774Z ================================ tests coverage ================================
2026-02-28T19:08:35.7130433Z _______________ coverage: platform linux, python 3.11.14-final-0 _______________
2026-02-28T19:08:35.7130894Z 
2026-02-28T19:08:35.7131074Z Name                         Stmts   Miss  Cover   Missing
2026-02-28T19:08:35.7131561Z ----------------------------------------------------------
2026-02-28T19:08:35.7132284Z src/isobar_cli/__init__.py       1      0   100%
2026-02-28T19:08:35.7132957Z src/isobar_cli/api.py           88     19    78%   25-31, 85-86, 114, 120-121, 126-127, 132-133, 178-180
2026-02-28T19:08:35.7133587Z src/isobar_cli/location.py      13      0   100%
2026-02-28T19:08:35.7134125Z src/isobar_cli/main.py          30     11    63%   64-74, 81-83, 91, 95
2026-02-28T19:08:35.7134861Z src/isobar_cli/ui.py           175     48    73%   110-113, 123-124, 150-157, 186, 188, 201-250, 259-260, 283-284
2026-02-28T19:08:35.7135549Z ----------------------------------------------------------
2026-02-28T19:08:35.7136002Z TOTAL                          307     78    75%
2026-02-28T19:08:35.7136978Z =========================== short test summary info ============================
2026-02-28T19:08:35.7139126Z FAILED tests/test_main.py::test_main_metric_flag_exists - AssertionError: assert '--metric' in '\x1b[1m                                                                                \x1b[0m\n\x1b[1m \x1b[0m\x1b[1...   \x1b[2m│\x1b[0m\n\x1b[2m╰──────────────────────────────────────────────────────────────────────────────╯\x1b[0m\n\n'
2026-02-28T19:08:35.7141613Z  +  where '\x1b[1m                                                                                \x1b[0m\n\x1b[1m \x1b[0m\x1b[1...   \x1b[2m│\x1b[0m\n\x1b[2m╰──────────────────────────────────────────────────────────────────────────────╯\x1b[0m\n\n' = <Result okay>.output
2026-02-28T19:08:35.7143207Z ========================= 1 failed, 13 passed in 4.56s =========================
2026-02-28T19:08:35.7985201Z ##[error]Process completed with exit code 1.
2026-02-28T19:08:35.8098179Z Post job cleanup.
2026-02-28T19:08:35.9089194Z [command]/usr/bin/git version
2026-02-28T19:08:35.9128894Z git version 2.53.0
2026-02-28T19:08:35.9181030Z Temporarily overriding HOME='/home/runner/work/_temp/dfec7606-f724-42fb-bb99-f6e25abee68a' before making global git config changes
2026-02-28T19:08:35.9183473Z Adding repository directory to the temporary git global config as a safe directory
2026-02-28T19:08:35.9189804Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/isobar-cli/isobar-cli
2026-02-28T19:08:35.9237369Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2026-02-28T19:08:35.9279441Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2026-02-28T19:08:35.9567325Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2026-02-28T19:08:35.9597041Z http.https://github.com/.extraheader
2026-02-28T19:08:35.9616203Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
2026-02-28T19:08:35.9657157Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2026-02-28T19:08:35.9909393Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
2026-02-28T19:08:35.9945687Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
2026-02-28T19:08:36.0309060Z Cleaning up orphan processes

