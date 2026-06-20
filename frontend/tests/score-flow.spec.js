import { expect, test } from "@playwright/test";

const winningHand = [
  "2m",
  "2m",
  "4m",
  "4m",
  "4m",
  "3p",
  "3p",
  "3p",
  "5p",
  "6p",
  "7p",
  "4s",
  "4s",
  "4s",
];

test("empty form explains why score cannot be calculated", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Score hand" }).click();

  await expect(page.getByRole("listitem").filter({ hasText: "Add 14 more tiles." })).toBeVisible();
  await expect(
    page.getByRole("listitem").filter({ hasText: "Choose which entered tile completed the hand." })
  ).toBeVisible();
});

test("scores a hand entered through visual tile buttons", async ({ page }) => {
  await page.goto("/");

  for (const tileId of winningHand) {
    await page.getByLabel(`Add ${tileId}`).click();
  }

  await page.getByLabel("Winning tile").selectOption("4s");
  await page.getByRole("button", { name: "Show advanced conditions" }).click();
  await page.getByRole("checkbox", { name: "Riichi", exact: true }).check();
  await page.getByRole("button", { name: "Score hand" }).click();

  await expect(page.getByText("Ready to score.")).toBeVisible();
  await expect(page.getByText("2 han · 40 fu · no limit")).toBeVisible();
  await expect(page.getByText("2600")).toBeVisible();
  await expect(page.getByText("Riichi · 1 han")).toBeVisible();
  await expect(page.getByText("Tanyao · 1 han")).toBeVisible();
});

test("example hand shortcut produces a valid score", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Example" }).click();
  await page.getByRole("button", { name: "Score hand" }).click();

  await expect(page.getByText("2 han · 40 fu · no limit")).toBeVisible();
  await expect(page.getByText("2600")).toBeVisible();
});
