#!/bin/bash

# Check if the project in the given folder has any changes.
# If there are changes, then the function returns 0, otherwise 1.
has_changes()  {
  folder=$1
  latest_tag=$2

  # If the latest tag is empty, then there are changes
  if [ -z "$latest_tag" ]; then
    return 0
  fi

  # If the latest tag is not empty, then check if there are any changes
  if [ -z "$(git diff "$latest_tag" --exit-code "$folder")" ]; then
    return 1
  else
    return 0
  fi
}

# Returns a list of all projects that could be released.
# The list is a space-separated string of all folders. Example "common/sdk common/types tools/kysor"
list_projects() {
  # List all subfolders of "common" (except proto)
  common=$(find common/* -maxdepth 0 -type d | grep -v proto)

  # List all subfolders of "protocol"
  protocol=$(find protocol/* -maxdepth 0 -type d)

  # List all subfolders of "runtime"
  runtime=$(find runtime/* -maxdepth 0 -type d)

  # List all subfolders of "tools"
  tools=$(find tools/* -maxdepth 0 -type d)

  # Merge all lists
  echo "$common $protocol $runtime $tools"
}

# Get the latest tag for a given branch name.
get_latest_tag() {
  branch_name=$1

  # Get all tags on main branch
  tags=$(git tag --list "$branch_name@*" --sort=-v:refname)

  # Filter tags to only include those that follow semantic versioning and exclude pre-release versions
  semver_tags=$(echo "$tags" | grep -P "^$branch_name@(\d+\.)?(\d+\.)?(\*|\d+)$")

  # If there are no tags, return an empty string
  if [ -z "$semver_tags" ]; then
    echo ""
    return
  fi

  # Get the latest semver tag
  latest_tag=$(echo "$semver_tags" | head -n 1)

  echo "$latest_tag"
}

# Get the current version
get_current_version() {
  tag=$1

  if [ -z "$tag" ]; then
    echo "0.0.0"
    return
  fi

  # Extract version from tag
  version=$(echo "$tag" | awk -F'@' '{print $2}')

  echo "$version"
}

# Get the next patch version for a given tag
get_next_patch_version() {
  tag=$1

  if [ -z "$tag" ]; then
    echo "0.0.1"
    return
  fi

  # Extract version from tag
  version=$(echo "$tag" | awk -F'@' '{print $2}')

  # Get the major, minor, and patch version
  major=$(echo "$version" | cut -d'.' -f1)
  minor=$(echo "$version" | cut -d'.' -f2)
  patch=$(echo "$version" | cut -d'.' -f3)

  echo "$major.$minor.$((patch + 1))"
}

# Only allow this script to be run on the main branch
check_if_main_branch() {
  branch=$(git branch --show-current)
  if [ "$branch" != "main" ]; then
    echo "Please run this script on the main branch"
    exit 1
  fi
}

# Check if there are any uncommitted changes
check_if_has_uncommitted_changes() {
  if [ -n "$(git status --porcelain -uno)" ]; then
    echo "Please commit or stash your changes before running this script"
    exit 1
  fi
}

# Create a release script and run it
create_and_run_release_script() {
  release_script="#!/bin/bash\n\n# HERE YOU CAN CHANGE THE VERSIONS!!!"
  release_script="$release_script$release_data\n\n"
  release_script="$release_script"'git push --follow-tags origin main'

  # Save the release script to a file
  echo -e "$release_script" > release.sh

  # Ask the user what to do
  printf "\n⚠️  If you want to change the versions, edit the release.sh file before continuing.\n"
  read -p "Do you want to continue? (y/N)" -r response
  printf "\n"
  if [[ $response =~ ^[Yy]$ ]]; then
    chmod +x release.sh
    ./release.sh
  else
    echo "Release aborted"
  fi

  # Remove the release script
  rm release.sh
}

# Release all projects that have changes (except node projects)
release() {
  local no_changes=true
  local release_data=""

  # List all projects and release them
  for project in $(list_projects); do
    # Get the latest tag for the branch
    latest_tag=$(get_latest_tag "$project")

    # Check if the project has any changes and if it does, then create a new tag
    if has_changes "$project" "$latest_tag"; then
      no_changes=false

      # Get current version
      current_version=$(get_current_version "$latest_tag")

      # Get next patch version
      next_version=$(get_next_patch_version "$latest_tag")

      # Create the branch name
      branch_name="$project@$next_version"

      # If the latest tag is the same as the branch name, then skip the release
      if [ "$latest_tag" = "$branch_name" ]; then
        continue
      fi

      # Print changes
      echo "$project: $current_version -> $next_version"

      # Add a git command to create a new tag to the release script
      tag_var_name=$(echo "$project" | tr / _ | tr '[:lower:]' '[:upper:]')
      release_data="$release_data\n# $tag_var_name\n$tag_var_name=$next_version\ngit tag -a \"$project@\$$tag_var_name\" -m \"Release \$$tag_var_name\""
    fi
  done

  if [ "$no_changes" = true ]; then
    echo "No changes detected in any module or package"
    exit 0
  fi

  create_and_run_release_script "$release_data"
}

check_if_main_branch
check_if_has_uncommitted_changes
release
