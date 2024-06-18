# Contributing

## Request for changes / Pull Requests

You first need to create a fork of the [WDFAP](https://github.com/IsmaelMousa/WDFAP) repository to commit your changes
to it. Methods to fork a repository can be found in
the [GitHub Documentation](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

Then add your fork as a local project:

```sh
# Using HTTPS
git clone https://github.com/IsmaelMousa/WDFAP.git

# Using SSH
git clone git@github.com:IsmaelMousa/WDFAP.git
```

> [!TIP]
>
>[Which remote URL should be used ?](https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories)

Then, go to your local folder

```sh
cd WDFAP
```

Add git remote controls :

```sh
# Using HTTPS
git remote add fork https://github.com/YOUR-USERNAME/WDFAP.git
git remote add upstream https://github.com/IsmaelMousa/WDFAP.git


# Using SSH
git remote add fork git@github.com:YOUR-USERNAME/WDFAP.git
git remote add upstream git@github.com/IsmaelMousa/WDFAP.git
```

You can now verify that you have your two git remotes:

```sh
git remote -v
```

## Receive remote updates

In view of staying up to date with the central repository:

```sh
git pull upstream main
```

## Choose a base branch

Before starting development, you need to know which branch to base your modifications/additions on. When in doubt,
use `main`.

| Type of change |           | Branches |
|:---------------|:---------:|---------:|
| New feature    |           |   `main` |
| Bug fix        |           |   `main` |

```sh
# Switch to the desired branch
git switch main

# Pull down any upstream changes
git pull origin main

# Create a new branch to work on
# New feature
git switch --create development/Fs-1234-YOUR_NAME-issue
# Bug fix
git switch --create development/Bs-1234-YOUR_NAME-issue
```

Commit your changes, then push the branch to your fork with `git push -u fork` and open a pull request
on [The WDFAP Repository](https://github.com/IsmaelMousa/WDFAP) following the template
provided.

---

<div align="right">

**[Go Back ➡️](index.md)**

</div>