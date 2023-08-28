export const FINDER_CHART_VIEW_BASE_URL = "finder-chart-view";
export class FinderChartViewPage {
  static visit(finderChart: string, positionAngle: number): void {
    cy.visit(`${FINDER_CHART_VIEW_BASE_URL}/${finderChart}/${positionAngle}`);
  }
  static rotateLeft(): void {
    cy.get("[data-test='rotate-left']").click();
  }
  static rotateRight(): void {
    cy.get("[data-test='rotate-right']").click();
  }
  static zoomIn(): void {
    cy.get("[data-test='zoom-in']").click();
  }
  static zoomOut(): void {
    cy.get("[data-test='zoom-out']").click();
  }
  static typePositionAngle(positionAngle: string): void {
    cy.get("[data-test='position-angle']").type(positionAngle);
  }
  static removeFocus(): void {
    cy.get("[data-test='finder-chart-view']").click();
  }

  static mirrorX(): void {
    cy.get("[data-test='mirror-x']").click();
  }

  static mirrorY(): void {
    cy.get("[data-test='mirror-y']").click();
  }
}
