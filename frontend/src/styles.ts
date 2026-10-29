import { css } from "lit";

/** Shared look, built on Home Assistant's theme variables so every theme works. */
export const cardStyles = css`
  :host {
    display: block;
    container-type: inline-size;
  }
  ha-card {
    overflow: hidden;
  }
  .head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 0 16px 8px;
    color: var(--secondary-text-color);
    font-size: 0.9em;
  }
  .chip {
    border-radius: 12px;
    padding: 2px 10px;
    font-size: 0.8em;
    background: var(--secondary-background-color);
    color: var(--primary-text-color);
  }
  .chip.draft {
    background: var(--warning-color, #ffa600);
    color: var(--text-primary-color, #fff);
  }
  .chip.confirmed {
    background: var(--success-color, #43a047);
    color: var(--text-primary-color, #fff);
  }
  .banner {
    margin: 0 16px 8px;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 0.9em;
    background: var(--secondary-background-color);
  }
  .banner.error {
    background: var(--error-color, #db4437);
    color: var(--text-primary-color, #fff);
  }
  .banner.warning {
    border-left: 4px solid var(--warning-color, #ffa600);
  }
  .empty {
    padding: 8px 16px 16px;
    color: var(--secondary-text-color);
  }
  .day {
    display: grid;
    grid-template-columns: 56px minmax(0, 1fr) auto;
    gap: 4px 12px;
    align-items: center;
    padding: 10px 16px;
    border-top: 1px solid var(--divider-color);
  }
  .when {
    text-align: center;
    line-height: 1.2;
  }
  .when .wd {
    font-weight: 500;
    text-transform: capitalize;
  }
  .when .dt {
    font-size: 0.8em;
    color: var(--secondary-text-color);
  }
  .main {
    display: flex;
    gap: 12px;
    align-items: center;
    min-width: 0;
  }
  .main img {
    width: 48px;
    height: 48px;
    border-radius: 8px;
    object-fit: cover;
    flex: none;
  }
  .title {
    font-weight: 500;
    overflow-wrap: anywhere;
  }
  .title a {
    color: inherit;
    text-decoration: none;
  }
  .title a:hover {
    text-decoration: underline;
  }
  .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 4px 8px;
    margin-top: 2px;
    font-size: 0.85em;
    color: var(--secondary-text-color);
  }
  .tag {
    border-radius: 8px;
    padding: 0 6px;
    background: var(--secondary-background-color);
  }
  .badge {
    border-radius: 8px;
    padding: 0 6px;
    border: 1px solid var(--divider-color);
  }
  .badge.split {
    border-color: var(--primary-color);
    color: var(--primary-color);
  }
  .actions {
    display: flex;
    gap: 2px;
  }
  .more {
    grid-column: 1 / -1;
    display: grid;
    gap: 8px;
    min-width: 0;
    padding: 4px 0 4px 68px;
    font-size: 0.9em;
  }
  .more h4 {
    margin: 4px 0 2px;
    font-size: 0.9em;
    color: var(--secondary-text-color);
  }
  .more ul {
    margin: 0;
    padding-left: 18px;
  }
  .row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    min-width: 0;
  }
  .row input {
    flex: 1 1 140px;
  }
  .row select {
    flex: 1 1 100%;
  }
  .split-note {
    border-left: 3px solid var(--primary-color);
    padding-left: 8px;
  }
  button {
    font: inherit;
    cursor: pointer;
    border: none;
    border-radius: 8px;
    padding: 6px 12px;
    background: var(--secondary-background-color);
    color: var(--primary-text-color);
  }
  button.primary {
    background: var(--primary-color);
    color: var(--text-primary-color, #fff);
  }
  button.icon {
    padding: 6px;
    background: transparent;
    line-height: 0;
    color: var(--secondary-text-color);
  }
  button.icon.on {
    color: var(--primary-color);
  }
  button:disabled {
    opacity: 0.4;
    cursor: default;
  }
  input,
  select {
    max-width: 100%;
    box-sizing: border-box;
    font: inherit;
    padding: 6px 8px;
    border-radius: 8px;
    border: 1px solid var(--divider-color);
    background: var(--card-background-color);
    color: var(--primary-text-color);
    min-width: 0;
  }
  .foot {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: flex-end;
    padding: 12px 16px;
    border-top: 1px solid var(--divider-color);
  }

  /* A narrow card (a phone, or a small grid cell): give the text all the room. */
  @container (max-width: 440px) {
    .day {
      grid-template-columns: 44px minmax(0, 1fr) auto;
      gap: 4px 8px;
      padding: 10px 12px;
    }
    .main {
      gap: 8px;
    }
    .main img {
      width: 40px;
      height: 40px;
    }
    .more {
      padding-left: 0;
    }
    .head,
    .foot {
      padding-left: 12px;
      padding-right: 12px;
    }
    .banner {
      margin-left: 12px;
      margin-right: 12px;
    }
  }
`;
