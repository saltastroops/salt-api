// Taken from https://sankhadip.medium.com/how-to-sort-table-rows-according-column-in-angular-9-b04fdafb4140
export class Sort {
  private sortOrder = 1;
  private collator = new Intl.Collator(undefined, {
    numeric: true,
    sensitivity: "base",
  });

  constructor() {}

  // eslint-disable-next-line @typescript-eslint/no-explicit-any,@typescript-eslint/explicit-module-boundary-types
  public startSort(property: any, order: any, type = "") {
    if (order === "desc") {
      this.sortOrder = -1;
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return (a: any, b: any) => {
      if (type === "date") {
        return this.sortData(new Date(a[property]), new Date(b[property]));
      } else {
        return this.collator.compare(a[property], b[property]) * this.sortOrder;
      }
    };
  }
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private sortData(a: any, b: any) {
    if (a < b) {
      return -1 * this.sortOrder;
    } else if (a > b) {
      return this.sortOrder;
    } else {
      return 0;
    }
  }
}
