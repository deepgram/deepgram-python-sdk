# Branch and Release Process

- [Branch and Release Process](#branch-and-release-process)
  - [Branching Process](#branching-process)
    - [Branching Methods](#branching-methods)
    - [Branch Process for This Project](#branch-process-for-this-project)
      - [Why Pick This Strategy?](#why-pick-this-strategy)
  - [Release Process](#release-process)

## Branching Process

In software development, selecting an appropriate Git branch strategy is crucial for maintaining code integrity, fostering collaboration, and streamlining project management. A well-defined branch strategy helps teams manage code changes systematically, reducing the risk of conflicts and ensuring that features, bug fixes, and releases are properly isolated.

## Branching Methods

For open-source projects, three popular Git branching strategies are:

1. **Git Flow**:

   Git Flow is a robust branching strategy that uses multiple branches for feature development, releases, and hotfixes. The primary branches include:

   - `main`: Holds the production-ready code.
   - `develop`: Integrates all completed features and serves as the staging area for the next release.
   - `feature/*`: Branches off from `develop` for new features.
   - `release/*`: Branches off from `develop` when preparing a new release.
   - `hotfix/*`: Branches off from `main` for critical fixes that need to be deployed immediately.

   Git Flow is suitable for projects with regular release cycles and helps maintain a clear and structured workflow.

2. **GitHub Flow**:

   GitHub Flow is a simpler, more streamlined approach ideal for projects that deploy frequently. Its key principles include:

   - A single `main` branch always containing deployable code.
   - Branches for each feature or bug fix that branch off from `main` and merge back into `main` upon completion.
   - Continuous deployment from the `main` branch, allowing for fast iterations and rapid delivery of new features.

   This strategy emphasizes simplicity and continuous integration, making it well-suited for fast-paced development environments.

3. **Trunk-Based Development**:

   Trunk-Based Development focuses on keeping a single, stable branch (the "trunk") where all developers commit their code. Key practices include:

   - Small, frequent commits directly to the `main` branch.
   - Short-lived feature branches that are quickly merged back into `main`.
   - Emphasis on automated testing and continuous integration to ensure code stability.
   This strategy aims to minimize merge conflicts and maintain a high level of code quality, promoting rapid feedback and collaboration.

Each of these strategies has its own strengths and is chosen based on the specific needs and workflow of the project.

## Branch Process for This Project

This project's branch process sits between **GitHub Flow** and **Git Flow** by taking the best of both worlds. This projects branching strategy looks like:

Aspects used from **GitHub Flow**:

- A single `main` branch always containing deployable code.
- Branches for each feature or bug fix that branch off from `main` and merge back into `main` upon completion.
- Continuous deployment from the `main` branch, allowing for fast iterations and rapid delivery of new features.

Aspects used from **Git Flow**:

- `release-v[0-9]+/*`: Branches off from `main` when preparing a new release.
- `hotfix/*`: Branches off from `main` (or a release branch) for critical fixes that need to be deployed immediately.

### Why Pick This Strategy?

This is done in order to foster:

- maximum collaboration with external contributors
  - since we are on GitHub, it's the standard workflow by default. (its why `develop`, or `alpha`/`beta`/etc branches aren't created by default)
  - it's intuitively obvious where contributions (ie PRs) need to merge with zero background on the project
  - this puts all bespoke, project, and repo management on the project maintainers
- forces the project maintainers to embrace CI/CD
  - `main` must work at all times; therefore, main can be deployed or released at all times
- things don't always go according to plan
  - having the branching strategy for releases **Git Flow** helps support of concurrent versions
  - provides flexibilty to create release trains

## Release Process

The release process for this project is designed to balance the rapid iteration capabilities of **GitHub Flow** with the structured release management of **Git Flow**. Releases are typically created off `main` since we strive to keep backwards compatibility and prevent breaking any interfaces. This implies that releases are basically a single train pushing features out. In terms of new feature release health, you should consider the `main` branch unstable. Consumers of this SDK should **ONLY** ever consume a tagged release on the repo release page.

In the event of a breaking interface change, a `release-v[0-9]+` branch is created off the main branch or at the point of divergence. Additionally, according to semver best practices, the project is accompanied by a major version bump. It's implied that these different interfaces are to be supported until determined by the company SLA.

In scenarios where urgent issues arise, the `hotfix` branch comes into play. A hotfix branch is created off main or the relevant release branch to address critical issues that need immediate attention. After the hotfix is implemented and thoroughly tested, it is merged back into both the `main` and the `release-v[0-9]+` branches to ensure the fix is included in the current and future versions of the project.

This dual approach of leveraging both **GitHub Flow** and **Git Flow** ensures that the project can iterate quickly while maintaining high standards of code stability and release management.

### Creating a Release

Since the latest stable code is contained on `main` in a typical **GitHub Flow**, to create a release someone with write access to the repository needs to simply just `git tag` the release and then create a (draft) release using that tag in the [repository's release page](https://github.com/deepgram/deepgram-python-sdk/releases).

If you haven't done this before, these are the typicial commands to execute at the root of the repository assuming you are on your fork:

```bash
# get the latest everything and update your fork
git checkout main
git pull --rebase upstream main
git push
git fetch upstream --tags
git push origin --tags

# create a new tag following semver
git tag -m <version> <version>
git push upstream  <version>
```

If the release you want to create is `v3.9.0`, then this would look like:

```bash
# get the latest everything and update your fork
git checkout main
git pull --rebase upstream main
git push
git fetch upstream --tags
git push origin --tags

# create a new tag following semver
git tag -m v3.9.0 v3.9.0
git push upstream v3.9.0
```

#### Creating a Release from a Release Branch

While we don't have a formal requirement for supporting past releases (ie currently on `v3` but need a patch on `v2`), there are times when you need to provide a patch release for things like security fixes. To create that patch releases, you do something similar as you would have done on main, but on the `release-v[0-9]+/*` branch.

If this were the `release-v2` branch for version `v2.5.1` (note the `v2` matches the `release-v2`), this would look like (again, assuming you are on your fork):

```bash
# get the latest everything and update your fork
git checkout release-v2
git pull --rebase upstream release-v2
git push origin release-v2
git fetch upstream --tags
git push origin --tags

# create a new tag following semver
git tag -m v2.5.1 v2.5.1
git push upstream v2.5.1
```
