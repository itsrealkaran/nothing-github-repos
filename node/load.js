"use strict";

const { ownedRepos } = require("./github");

async function load(login) {
  const owned = await ownedRepos(login);
  const visible = owned.repos.filter((repo) => !repo.private);
  visible.sort((a, b) => (b.stargazers_count || 0) - (a.stargazers_count || 0));
  const rows = visible.slice(0, 5).map((repo) => [repo.name, repo.stargazers_count || 0]);
  return { login, repos: rows.length ? rows : [["No public repos", 0]] };
}

module.exports = { load };
