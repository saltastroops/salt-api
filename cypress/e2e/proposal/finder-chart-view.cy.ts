import { FinderChartViewPage } from "../../support/pages/finder-chart-view-page";
import { LoginPage } from "../../support/pages/login/login-page";
import { getApiUrl } from "../../support/utils";

describe("Finder chart view", () => {
  const apiUrl = getApiUrl();

  const USERNAME = "nhlavutelo";

  beforeEach(() => {
    cy.intercept(apiUrl + "/login").as("login");

    cy.task("updateUserPassword", USERNAME).then((password: string) => {
      // Login
      LoginPage.visit();
      LoginPage.login(USERNAME, password);
    });
  });

  it("should display the image", () => {
    FinderChartViewPage.visit("noun-missing-2181345.png", 0);
    cy.get('[data-test="image-wrapper"]').should("be.visible");
  });

  it("should load finder chart pre rotate by the position angle", () => {
    const positionAngle = 30;
    FinderChartViewPage.visit("noun-missing-2181345.png", positionAngle);
    cy.get('[data-test="image-wrapper"]')
      .should("have.attr", "style")
      .should("contain", `transform: rotate(${positionAngle}deg)`);
  });

  it("should rotate by the set position angle", () => {
    FinderChartViewPage.visit("noun-missing-2181345.png", 0);
    cy.get('[data-test="image-wrapper"]')
      .should("have.attr", "style")
      .should("contain", `rotate(${0}deg)`);
    const positionAngle = "123";
    FinderChartViewPage.typePositionAngle(positionAngle);
    FinderChartViewPage.removeFocus();
    cy.get('[data-test="image-wrapper"]')
      .should("have.attr", "style")
      .should("contain", `rotate(${positionAngle}deg)`);
  });

  it("should zoom in and out", () => {
    FinderChartViewPage.visit("noun-missing-2181345.png", 0);
    // Zoom will either increase or reduce image size by 10%
    FinderChartViewPage.zoomIn(); // +10 -> 110
    let expectedZoom = 1.1; // 110 represented as 1.1
    cy.get('[data-test="image-wrapper"]')
      .should("have.attr", "style")
      .should("contain", `scale(${expectedZoom})`);
    FinderChartViewPage.zoomOut(); // -10 -> 100
    FinderChartViewPage.zoomOut(); // -10 -> 90
    FinderChartViewPage.zoomOut(); // -10 -> 80
    expectedZoom = 0.8; // 80 represented as 0.8
    cy.get('[data-test="image-wrapper"]')
      .should("have.attr", "style")
      .should("contain", `scale(${expectedZoom})`);
  });

  it("should mirror image", () => {
    FinderChartViewPage.visit("noun-missing-2181345.png", 0);

    FinderChartViewPage.mirrorX(); // toggle scaleX between 1 and -1 initial value 1
    FinderChartViewPage.mirrorY(); // toggle scaleY between 1 and -1 initial value 1
    cy.get('[data-test="image-wrapper"]')
      .should("have.attr", "style")
      .should("contain", `scaleX(-1) scaleY(-1)`);

    FinderChartViewPage.mirrorY();
    cy.get('[data-test="image-wrapper"]')
      .should("have.attr", "style")
      .should("contain", `scaleX(-1) scaleY(1)`);
  });

  it("should zoom in and out on mouse scroll", () => {
    FinderChartViewPage.visit("noun-missing-2181345.png", 0);
    const scrollDelta = 100;

    cy.get('[data-test="image-wrapper"]').trigger("wheel", {
      deltaY: -scrollDelta,
    });
    cy.get('[data-test="image-wrapper"]').should(
      "have.css",
      "transform",
      "matrix(1.1, 0, 0, 1.1, 0, 0)",
    );

    cy.get('[data-test="image-wrapper"]').trigger("wheel", {
      deltaY: scrollDelta,
    });
    cy.get('[data-test="image-wrapper"]').should(
      "have.css",
      "transform",
      "matrix(1, 0, 0, 1, 0, 0)",
    );
  });
});
