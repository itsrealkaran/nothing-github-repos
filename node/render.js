"use strict";

const { dots, label, openSvg } = require("./frame");
const { theme } = require("./nothing");
const { fixed } = require("./format");

function render(mode, size, data) {
  const colors = theme(mode);
  if (size === "mini") return mini(mode, colors, data);
  if (size === "compact") return compact(mode, colors, data);
  if (size === "wide") return list(mode, colors, data, 896, true);
  return list(mode, colors, data, 495, false);
}

function mini(mode, colors, data) {
  const [repo, stars] = data.repos[0];
  const [name] = dots("REPOS", 28, 12, colors.fg, 1.15);
  return [
    openSvg(mode, 220, 148, data.login + " repositories", 6, 14),
    name,
    label(16, 100, repo, colors.fg, 16, 0),
    label(16, 124, stars + " stars", colors.muted, 12, 0.2),
    "</svg>",
  ].join("\n");
}

function compact(mode, colors, data) {
  const [repo, stars] = data.repos[0];
  const [name] = dots("REPOS", 40, 16, colors.fg, 1.8);
  return [
    openSvg(mode, 495, 132, data.login + " repositories"),
    name,
    label(20, 96, repo, colors.fg, 22, 0),
    label(20, 118, stars + " stars · @" + data.login, colors.muted, 13, 0.2),
    "</svg>",
  ].join("\n");
}

function list(mode, colors, data, width, bars) {
  const rows = data.repos;
  const height = 72 + rows.length * 30 + 24;
  const [name] = dots("REPOS", 40, 16, colors.fg, 1.8);
  const parts = [openSvg(mode, width, height, data.login + " repositories"), name];
  const peak = Math.max(...rows.map((row) => row[1])) || 1;
  rows.forEach(([repo, stars], index) => {
    const y = 78 + index * 30;
    parts.push(label(20, y, repo, colors.fg, 15, 0.1));
    if (bars) {
      const bar = Math.max(4, 460 * (stars / peak));
      parts.push(`<rect x="280" y="${y - 11}" width="460" height="6" fill="${colors.rule}"/>`);
      parts.push(`<rect x="280" y="${y - 11}" width="${fixed(bar, 1)}" height="6" fill="${colors.figure}"/>`);
      parts.push(label(760, y, String(stars), colors.figure, 15, 0.2));
    } else {
      parts.push(label(width - 56, y, String(stars), colors.figure, 15, 0.2));
    }
  });
  parts.push("</svg>");
  return parts.join("\n");
}

module.exports = { render };
