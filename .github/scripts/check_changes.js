const util = require('util');
const exec = util.promisify(require('child_process').exec);
const fs = require('fs');
const path = require('path');

// Check if the project in the given folder has any changes.
async function has_changes(folder, latest_tag) {
  // If the latest tag is empty, then there are changes
  if (!latest_tag) {
    return true;
  }

  // Check for changes
  const { stdout } = await exec(`git diff "${latest_tag}" "${folder}"`);
  console.log(stdout.trim());
  return stdout.trim() !== '';
}

function list_projects() {
  const listFolders = (dir) => fs.readdirSync(dir, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => path.join(dir, dirent.name));

  const common = listFolders('common').filter(folder => !folder.endsWith('proto'));
  const protocol = listFolders('protocol');
  const runtime = listFolders('runtime');
  const tools = listFolders('tools');

  return [...common, ...protocol, ...runtime, ...tools];
}

async function get_latest_tag(branch_name) {
  // Get all tags on main branch
  const { stdout: tags } = await exec(`git tag --list "${branch_name}@*" --sort=-v:refname`);

  // Split tags by newline and filter by semantic versioning
  const semver_tags = tags.split('\n').filter(tag => /^.*@(\d+)\.(\d+)\.(\d+)$/.test(tag));

  // If there are no tags, return an empty string
  if (semver_tags.length === 0) {
    return '';
  }

  // Get the latest semver tag
  return  semver_tags[0];
}

async function main() {
  const projects = list_projects();
  for (const project of projects) {
    const latest_tag = await get_latest_tag(project);
    const changes = await has_changes(project, latest_tag.trim());
    console.log(`Project: ${project}, Has Changes: ${changes}`);
  }
}

main().catch(console.error);