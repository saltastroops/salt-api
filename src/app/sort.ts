// Adapted from https://sankhadip.medium.com/how-to-sort-table-rows-according-column-in-angular-9-b04fdafb4140
/* eslint-disable @typescript-eslint/no-explicit-any */
export class Sort {
  private sortOrder = 1;
  private collator = new Intl.Collator(undefined, {
    sensitivity: "base",
  });

  public startSort(
    property: string | ((value: any) => any),
    // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
    order: any,
    isString: boolean,
  ): (a: any, b: any) => number {
    if (order === "desc") {
      this.sortOrder = -1;
    }
    if (typeof property === "string") {
      return (a: any, b: any) => {
        if (isString) {
          return (
            this.collator.compare(a[property], b[property]) * this.sortOrder
          );
        } else {
          return this.sortData(a[property], b[property]);
        }
      };
    } else {
      return (a: any, b: any) => {
        if (isString) {
          return (
            this.collator.compare(property(a), property(b)) * this.sortOrder
          );
        } else {
          return this.sortData(property(a), property(b));
        }
      };
    }
  }

  private sortData(a: any, b: any): number {
    if (a < b) {
      return -1 * this.sortOrder;
    } else if (a > b) {
      return this.sortOrder;
    } else {
      return 0;
    }
  }
}
/* eslint-enable @typescript-eslint/no-explicit-any */
